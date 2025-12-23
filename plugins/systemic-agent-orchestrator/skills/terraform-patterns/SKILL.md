---
description: "This skill activates when the user asks about Terraform infrastructure, AWS resource provisioning, IaC patterns, Terraform workspaces, modules, or deployment automation. Trigger on: 'Terraform', 'infrastructure as code', 'AWS resources', 'deploy infrastructure', 'terraform apply', 'IaC'."
---

# Terraform Patterns for Agent Infrastructure

## Overview

All agent infrastructure lives in `/infra` folder at project root with Terraform.

---

## Project Structure

```
my-agent/
├── infra/
│   ├── main.tf              # Root module
│   ├── variables.tf         # Input variables
│   ├── outputs.tf           # Output values
│   ├── versions.tf          # Provider versions
│   ├── backend.tf           # State backend (S3)
│   ├── locals.tf            # Local values
│   │
│   ├── modules/
│   │   ├── agent-runtime/   # ECS/Lambda for agent
│   │   ├── database/        # Aurora Serverless
│   │   ├── api/             # API Gateway
│   │   └── monitoring/      # CloudWatch
│   │
│   └── environments/
│       ├── dev.tfvars
│       ├── homolog.tfvars
│       └── prod.tfvars
│
├── src/                     # Agent code
└── tests/
```

---

## Tagging Standards (CRITICAL)

**All tags MUST be in UPPERCASE**:

```hcl
locals {
  common_tags = {
    PROJETO   = "AGENT-ORCHESTRATOR"
    AMBIENTE  = upper(var.environment)  # PRD, HMLG, DEV
    PRODUTO   = "AI-AGENTS"
    MANAGED   = "TERRAFORM"
  }
}

resource "aws_ecs_cluster" "agent" {
  name = "${var.project_name}-${var.environment}"
  
  tags = local.common_tags
}
```

**Required tags**:
- `PROJETO` - Project name
- `AMBIENTE` - Environment (PRD, HMLG, DEV)

**Optional tags**:
- `PRODUTO` - Product name (use `|` separator for shared: `"A|B"`)
- `MANAGED` - "TERRAFORM"

---

## Backend Configuration

**S3 state storage is REQUIRED**:

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-state-{account-id}"
    key            = "agents/my-agent/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

---

## Core Resources

### 1. Aurora Serverless v2

```hcl
# modules/database/main.tf
resource "aws_rds_cluster" "agent_db" {
  cluster_identifier = "${var.project_name}-${var.environment}"
  engine             = "aurora-postgresql"
  engine_mode        = "provisioned"
  engine_version     = "15.4"
  database_name      = "agent_db"
  master_username    = "admin"
  master_password    = random_password.db_password.result
  
  # DATA API REQUIRED
  enable_http_endpoint = true
  
  serverlessv2_scaling_configuration {
    min_capacity = var.environment == "prod" ? 0.5 : 0.5
    max_capacity = var.environment == "prod" ? 8 : 2
  }
  
  skip_final_snapshot = var.environment != "prod"
  
  tags = var.common_tags
}

resource "aws_rds_cluster_instance" "agent_db" {
  cluster_identifier   = aws_rds_cluster.agent_db.id
  instance_class       = "db.serverless"
  engine               = aws_rds_cluster.agent_db.engine
  engine_version       = aws_rds_cluster.agent_db.engine_version
  publicly_accessible  = false
  
  tags = var.common_tags
}
```

### 2. SSM Parameter Store (Secrets)

```hcl
# modules/secrets/main.tf
resource "aws_ssm_parameter" "db_connection" {
  name  = "/${var.environment}/agent/${var.project_name}/aurora_cluster_arn"
  type  = "SecureString"
  value = var.aurora_cluster_arn
  
  tags = var.common_tags
}

resource "aws_ssm_parameter" "langsmith_key" {
  name  = "/${var.environment}/agent/${var.project_name}/langsmith_api_key"
  type  = "SecureString"
  value = var.langsmith_api_key
  
  tags = var.common_tags
}
```

### 3. API Gateway v2

```hcl
# modules/api/main.tf
resource "aws_apigatewayv2_api" "agent" {
  name          = "${var.project_name}-${var.environment}"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = var.allowed_origins
    allow_methods = ["POST", "GET", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 300
  }
  
  tags = var.common_tags
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.agent.id
  name        = "$default"
  auto_deploy = true
  
  default_route_settings {
    throttling_burst_limit = var.throttling_burst
    throttling_rate_limit  = var.throttling_rate
  }
  
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      responseLength = "$context.responseLength"
    })
  }
  
  tags = var.common_tags
}
```

### 4. CloudWatch Logs with Retention

```hcl
# modules/monitoring/main.tf
locals {
  log_retention = {
    dev     = 1   # 1 day
    homolog = 3   # 3 days
    prod    = 7   # 7 days
  }
}

resource "aws_cloudwatch_log_group" "agent" {
  name              = "/agent/${var.project_name}/${var.environment}"
  retention_in_days = local.log_retention[var.environment]
  
  tags = var.common_tags
}

resource "aws_cloudwatch_log_group" "api" {
  name              = "/api/${var.project_name}/${var.environment}"
  retention_in_days = local.log_retention[var.environment]
  
  tags = var.common_tags
}
```

### 5. ECR Repository

```hcl
# modules/agent-runtime/ecr.tf
resource "aws_ecr_repository" "agent" {
  name                 = "${var.project_name}-agent"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
  
  tags = var.common_tags
}

resource "aws_ecr_lifecycle_policy" "agent" {
  repository = aws_ecr_repository.agent.name
  
  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
```

### 6. ECS Fargate (Agent Runtime)

```hcl
# modules/agent-runtime/ecs.tf
resource "aws_ecs_cluster" "agent" {
  name = "${var.project_name}-${var.environment}"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = var.common_tags
}

resource "aws_ecs_task_definition" "agent" {
  family                   = "${var.project_name}-${var.environment}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn
  
  container_definitions = jsonencode([
    {
      name  = "agent"
      image = "${aws_ecr_repository.agent.repository_url}:latest"
      
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        },
        {
          name  = "LANGCHAIN_TRACING_V2"
          value = "true"
        }
      ]
      
      secrets = [
        {
          name      = "LANGCHAIN_API_KEY"
          valueFrom = aws_ssm_parameter.langsmith_key.arn
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.agent.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "agent"
        }
      }
    }
  ])
  
  tags = var.common_tags
}
```

---

## Environment Variables

```hcl
# environments/dev.tfvars
environment = "dev"
project_name = "my-agent"

# Aurora
aurora_min_capacity = 0.5
aurora_max_capacity = 2

# ECS
cpu    = 256
memory = 512

# API Gateway
throttling_burst = 100
throttling_rate  = 50

# Allowed CORS origins
allowed_origins = ["http://localhost:3000"]
```

```hcl
# environments/prod.tfvars
environment = "prod"
project_name = "my-agent"

# Aurora
aurora_min_capacity = 0.5
aurora_max_capacity = 8

# ECS
cpu    = 1024
memory = 2048

# API Gateway
throttling_burst = 500
throttling_rate  = 200

# Allowed CORS origins
allowed_origins = ["https://app.example.com"]
```

---

## IAM Policies (Least Privilege)

```hcl
# modules/agent-runtime/iam.tf
data "aws_iam_policy_document" "agent_task" {
  # Bedrock
  statement {
    effect = "Allow"
    actions = [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream"
    ]
    resources = ["*"]
  }
  
  # Aurora Data API
  statement {
    effect = "Allow"
    actions = [
      "rds-data:ExecuteStatement",
      "rds-data:BatchExecuteStatement",
      "rds-data:BeginTransaction",
      "rds-data:CommitTransaction",
      "rds-data:RollbackTransaction"
    ]
    resources = [var.aurora_cluster_arn]
  }
  
  # Secrets Manager (for Aurora)
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue"
    ]
    resources = [var.aurora_secret_arn]
  }
  
  # SSM Parameters
  statement {
    effect = "Allow"
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters"
    ]
    resources = [
      "arn:aws:ssm:${var.region}:${var.account_id}:parameter/${var.environment}/agent/${var.project_name}/*"
    ]
  }
  
  # CloudWatch Logs
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["${aws_cloudwatch_log_group.agent.arn}:*"]
  }
}
```

---

## Validation Commands

```bash
# Validate syntax
terraform validate

# Plan for environment
terraform plan -var-file=environments/dev.tfvars

# Apply
terraform apply -var-file=environments/prod.tfvars -auto-approve
```

---

## Testing Requirements

Terraform tests are **REQUIRED**:

```hcl
# tests/agent_test.tftest.hcl
run "validate_tags" {
  command = plan
  
  assert {
    condition     = aws_ecs_cluster.agent.tags["AMBIENTE"] != null
    error_message = "AMBIENTE tag is required"
  }
  
  assert {
    condition     = aws_ecs_cluster.agent.tags["PROJETO"] != null
    error_message = "PROJETO tag is required"
  }
}

run "validate_log_retention" {
  command = plan
  
  assert {
    condition     = aws_cloudwatch_log_group.agent.retention_in_days <= 7
    error_message = "Log retention must not exceed 7 days"
  }
}
```

---

## DO and DON'T

### DO:
- Use S3 backend for state
- Apply UPPERCASE tags
- Set log retention by environment
- Use least-privilege IAM
- Store secrets in SSM
- Enable Data API for Aurora
- Test with `terraform validate` and `plan`

### DON'T:
- Hardcode credentials
- Skip tags
- Use default log retention
- Grant excessive IAM permissions
- Store state locally
- Skip Terraform tests
