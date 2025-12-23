---
description: "This skill activates when the user asks about CI/CD pipelines, GitHub Actions, automated deployment, testing pipelines, or continuous integration for agents. Trigger on: 'CI/CD', 'GitHub Actions', 'deploy pipeline', 'automated tests', 'continuous deployment', 'build pipeline'."
---

# CI/CD Patterns for Agent Deployment

## Overview

Automated deployment pipeline for LangGraph agents using GitHub Actions.

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CI/CD PIPELINE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Push to main/PR                                                 │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │    LINT/TEST    │ ◀─── ruff, pytest, coverage                │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │  TERRAFORM PLAN │ ◀─── Validate infrastructure               │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼ (main branch only)                                  │
│  ┌─────────────────┐                                            │
│  │   BUILD IMAGE   │ ◀─── Docker build, push to ECR            │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │ TERRAFORM APPLY │ ◀─── Deploy infrastructure                 │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │  DEPLOY AGENT   │ ◀─── Update ECS service                    │
│  └─────────────────┘                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## GitHub Actions Workflow

### Main Workflow: `.github/workflows/deploy.yml`

```yaml
name: Deploy Agent

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: {project_name}-agent
  ECS_CLUSTER: {project_name}-prod
  ECS_SERVICE: {project_name}-agent

permissions:
  id-token: write
  contents: read
  pull-requests: write

jobs:
  lint-and-test:
    name: Lint and Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "0.5.0"
      
      - name: Set up Python
        run: uv python install 3.11
      
      - name: Install dependencies
        run: uv sync --all-extras
      
      - name: Lint with ruff
        run: uv run ruff check src/ tests/
      
      - name: Run tests
        run: |
          uv run pytest tests/ -v --cov=src --cov-report=xml
      
      - name: Check coverage
        run: |
          uv run coverage report --fail-under=70
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
          fail_ci_if_error: false

  terraform-plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    needs: lint-and-test
    defaults:
      run:
        working-directory: infra
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Validate
        run: terraform validate
      
      - name: Terraform Plan
        id: plan
        run: |
          terraform plan -var-file=environments/prod.tfvars -no-color -out=tfplan
        continue-on-error: true
      
      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const output = `#### Terraform Plan 📖
            
            <details><summary>Show Plan</summary>
            
            \`\`\`terraform
            ${{ steps.plan.outputs.stdout }}
            \`\`\`
            
            </details>`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            })

  build-and-push:
    name: Build and Push Image
    runs-on: ubuntu-latest
    needs: terraform-plan
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    outputs:
      image_tag: ${{ steps.build.outputs.image_tag }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to ECR
        id: ecr-login
        uses: aws-actions/amazon-ecr-login@v2
      
      - name: Build and push image
        id: build
        env:
          ECR_REGISTRY: ${{ steps.ecr-login.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
          echo "image_tag=$IMAGE_TAG" >> $GITHUB_OUTPUT

  terraform-apply:
    name: Terraform Apply
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    defaults:
      run:
        working-directory: infra
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Apply
        run: |
          terraform apply -var-file=environments/prod.tfvars -auto-approve

  deploy-agent:
    name: Deploy Agent
    runs-on: ubuntu-latest
    needs: [build-and-push, terraform-apply]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Update ECS service
        run: |
          aws ecs update-service \
            --cluster $ECS_CLUSTER \
            --service $ECS_SERVICE \
            --force-new-deployment
      
      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster $ECS_CLUSTER \
            --services $ECS_SERVICE
      
      - name: Notify success
        run: |
          echo "✅ Deployment successful!"
          echo "Image: ${{ needs.build-and-push.outputs.image_tag }}"
```

---

## Environment-Specific Workflows

### Development: `.github/workflows/deploy-dev.yml`

```yaml
name: Deploy to Dev

on:
  push:
    branches: [develop]

# Similar to main workflow but:
# - Uses dev.tfvars
# - Deploys to dev ECS cluster
# - No approval required
```

### Homologation: `.github/workflows/deploy-homolog.yml`

```yaml
name: Deploy to Homolog

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Image tag to deploy'
        required: true

# Manual trigger with version selection
# Uses homolog.tfvars
```

---

## Required Secrets

Configure in GitHub repository settings:

| Secret | Description |
|--------|-------------|
| `AWS_ACCOUNT_ID` | AWS account ID |
| `LANGSMITH_API_KEY` | Langsmith API key |

**Note**: AWS authentication uses OIDC (role assumption), not access keys.

---

## IAM Role for GitHub Actions

```hcl
# github-actions-role.tf
resource "aws_iam_role" "github_actions" {
  name = "github-actions"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_org}/${var.github_repo}:*"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "github_actions" {
  role       = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.github_actions.arn
}
```

---

## Branch Protection Rules

Configure for `main` branch:

```yaml
# Required for merge:
- ✅ Require status checks to pass
  - lint-and-test
  - terraform-plan
- ✅ Require branches to be up to date
- ✅ Require review from code owners
- ✅ Do not allow bypassing
```

---

## Rollback Procedure

### Quick Rollback (Previous Image)

```bash
# Get previous image tag
aws ecr describe-images \
  --repository-name {project_name}-agent \
  --query 'sort_by(imageDetails,& imagePushedAt)[-2].imageTags[0]' \
  --output text

# Update to previous image
aws ecs update-service \
  --cluster {project_name}-prod \
  --service {project_name}-agent \
  --force-new-deployment \
  --task-definition {project_name}-agent:PREVIOUS_REVISION
```

### Full Rollback (Terraform)

```bash
cd infra

# Revert to previous state
git revert HEAD
git push origin main

# Or restore specific state
terraform state pull > current.tfstate.backup
terraform state push previous.tfstate
```

---

## Testing Coverage Requirements

```yaml
# Minimum 70% coverage for merge
- name: Check coverage
  run: |
    uv run coverage report --fail-under=70
```

---

## DO and DON'T

### DO:
- Use OIDC for AWS authentication
- Require status checks for merges
- Run terraform plan on PRs
- Wait for ECS service stability
- Keep secrets in GitHub Secrets
- Test with 70%+ coverage

### DON'T:
- Store AWS access keys in code
- Skip terraform plan
- Deploy without tests passing
- Merge without review
- Use force push on main
