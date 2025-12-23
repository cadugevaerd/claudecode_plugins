#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Hook: Run tests and validate coverage when Claude stops responding.
Blocks if tests fail or coverage < 70%.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

MIN_COVERAGE = 70


def find_project_root() -> Path | None:
    """Find project root by looking for pyproject.toml or src/ directory."""
    cwd = Path.cwd()

    # Look for pyproject.toml
    for parent in [cwd, *cwd.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
        if (parent / "src").is_dir() and (parent / "tests").is_dir():
            return parent

    return None


def run_python_tests(project_root: Path) -> tuple[bool, str, float | None]:
    """Run pytest with coverage. Returns (passed, output, coverage_percent)."""
    tests_dir = project_root / "tests"
    src_dir = project_root / "src"

    if not tests_dir.exists():
        return True, "No tests/ directory found, skipping Python tests", None

    if not src_dir.exists():
        return True, "No src/ directory found, skipping coverage", None

    try:
        result = subprocess.run(
            [
                "uv", "run", "pytest",
                "--cov=src",
                f"--cov-fail-under={MIN_COVERAGE}",
                "--cov-report=term-missing:skip-covered",
                "tests/",
                "-q",
                "--tb=short"
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout + result.stderr

        # Extract coverage percentage
        coverage = None
        for line in output.split("\n"):
            if "TOTAL" in line and "%" in line:
                parts = line.split()
                for part in parts:
                    if part.endswith("%"):
                        try:
                            coverage = float(part.rstrip("%"))
                        except ValueError:
                            pass

        passed = result.returncode == 0
        return passed, output, coverage

    except FileNotFoundError:
        return True, "pytest not found, skipping tests", None
    except subprocess.TimeoutExpired:
        return False, "Tests timed out after 120 seconds", None
    except Exception as e:
        return True, f"Error running tests: {e}", None


def run_terraform_tests(project_root: Path) -> tuple[bool, str]:
    """Run Terraform validation. Returns (passed, output)."""
    infra_dir = project_root / "infra"

    if not infra_dir.exists():
        return True, "No infra/ directory found, skipping Terraform tests"

    outputs = []
    all_passed = True

    # terraform fmt check
    try:
        result = subprocess.run(
            ["terraform", "fmt", "-check", "-recursive"],
            cwd=infra_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            all_passed = False
            outputs.append(f"[FAIL] terraform fmt: Files not formatted\n{result.stdout}")
        else:
            outputs.append("[PASS] terraform fmt")
    except FileNotFoundError:
        outputs.append("[SKIP] terraform not found")
    except Exception as e:
        outputs.append(f"[WARN] terraform fmt error: {e}")

    # terraform validate
    try:
        # Init first (without backend)
        subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=infra_dir,
            capture_output=True,
            timeout=60
        )

        result = subprocess.run(
            ["terraform", "validate"],
            cwd=infra_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            all_passed = False
            outputs.append(f"[FAIL] terraform validate:\n{result.stderr}")
        else:
            outputs.append("[PASS] terraform validate")
    except Exception as e:
        outputs.append(f"[WARN] terraform validate error: {e}")

    # tflint
    try:
        result = subprocess.run(
            ["tflint", "--recursive"],
            cwd=infra_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            all_passed = False
            outputs.append(f"[FAIL] tflint:\n{result.stdout}")
        else:
            outputs.append("[PASS] tflint")
    except FileNotFoundError:
        outputs.append("[SKIP] tflint not installed")
    except Exception as e:
        outputs.append(f"[WARN] tflint error: {e}")

    # tfsec
    try:
        result = subprocess.run(
            ["tfsec", ".", "--minimum-severity", "HIGH", "--format", "text"],
            cwd=infra_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0 and "No problems detected" not in result.stdout:
            all_passed = False
            outputs.append(f"[FAIL] tfsec (HIGH/CRITICAL issues):\n{result.stdout[:500]}")
        else:
            outputs.append("[PASS] tfsec")
    except FileNotFoundError:
        outputs.append("[SKIP] tfsec not installed")
    except Exception as e:
        outputs.append(f"[WARN] tfsec error: {e}")

    return all_passed, "\n".join(outputs)


def main() -> None:
    """Run tests on Stop event. Block if failures."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    # Only run on Stop event
    hook_event = input_data.get("hook_event_name", "")
    if hook_event != "Stop":
        print(json.dumps({}))
        return

    project_root = find_project_root()
    if not project_root:
        print(json.dumps({}))
        return

    # Check if we have tests to run
    has_python_tests = (project_root / "tests").exists()
    has_terraform = (project_root / "infra").exists()

    if not has_python_tests and not has_terraform:
        print(json.dumps({}))
        return

    failures = []
    report_lines = ["", "=== Stop Hook: Test Validation ===", ""]

    # Run Python tests
    if has_python_tests:
        py_passed, py_output, coverage = run_python_tests(project_root)

        if coverage is not None:
            if coverage >= MIN_COVERAGE:
                report_lines.append(f"[PASS] Python Coverage: {coverage:.1f}% (min: {MIN_COVERAGE}%)")
            else:
                report_lines.append(f"[FAIL] Python Coverage: {coverage:.1f}% (min: {MIN_COVERAGE}%)")
                failures.append(f"Coverage {coverage:.1f}% < {MIN_COVERAGE}% minimum")

        if not py_passed:
            report_lines.append(f"[FAIL] Python Tests:\n{py_output[:800]}")
            failures.append("Python tests failed")
        elif coverage is None or coverage >= MIN_COVERAGE:
            report_lines.append("[PASS] Python Tests")

    # Run Terraform tests
    if has_terraform:
        tf_passed, tf_output = run_terraform_tests(project_root)
        report_lines.append("")
        report_lines.append("Terraform Validation:")
        report_lines.append(tf_output)

        if not tf_passed:
            failures.append("Terraform validation failed")

    report_lines.append("")

    # Decide whether to block
    if failures:
        report_lines.append("=== BLOCKED ===")
        report_lines.append("Fix the following issues before proceeding:")
        for f in failures:
            report_lines.append(f"  - {f}")
        report_lines.append("")
        report_lines.append("Run tests manually with:")
        report_lines.append(f"  uv run pytest --cov=src --cov-fail-under={MIN_COVERAGE} tests/")
        if has_terraform:
            report_lines.append("  terraform validate && tflint && tfsec")

        result = {
            "decision": "block",
            "reason": "\n".join(report_lines)
        }
    else:
        report_lines.append("=== All Tests Passed ===")
        result = {}

    print(json.dumps(result))


if __name__ == "__main__":
    main()
