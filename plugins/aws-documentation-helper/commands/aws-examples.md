---
description: Find practical code examples, templates, and implementation patterns for AWS services
argument-hint: "[topic] (optional: language)"
allowed-tools: mcp__aws-knowledge-mcp-server__*, Read, Write, Bash
---

# AWS Code Examples & Patterns

Find practical code examples, CloudFormation templates, Terraform modules, and implementation patterns for AWS.

## 🎯 Purpose

Provides working code examples including:
- CloudFormation templates
- Terraform modules
- AWS SDK code (Python, JavaScript, Java, Go, etc.)
- CLI command examples
- Architecture diagrams
- Best practice implementations
- Complete application examples

## 📖 How To Use This Command

Use this command when you need to implement AWS solutions.

### By Topic

```bash
/aws-examples auto-scaling
/aws-examples vpc-setup
/aws-examples iam-policies
/aws-examples s3-encryption
/aws-examples lambda-api
/aws-examples rds-backup
/aws-examples dynamodb-table
/aws-examples cloudformation-stack
```

### By Service

```bash
/aws-examples ec2
/aws-examples s3
/aws-examples lambda
/aws-examples rds
/aws-examples dynamodb
/aws-examples vpc
```

### By Language

```bash
/aws-examples s3 python
/aws-examples lambda javascript
/aws-examples dynamodb java
/aws-examples ec2 terraform
/aws-examples cloudformation yaml
```

### Complete Patterns

```bash
/aws-examples web-application
/aws-examples microservices
/aws-examples data-pipeline
/aws-examples ci-cd-pipeline
/aws-examples serverless-api
```

## 🔄 Execution Steps

### Step 1: Parse Request

- Identify topic or service
- Identify language (Python, JS, Go, Java, etc.) or tool (Terraform, CloudFormation, CLI)
- If not specified: provide examples in popular languages

### Step 2: Search for Examples

Query AWS documentation for code samples:
- Official AWS examples
- Best practice implementations
- Complete working projects
- Detailed comments and explanations

### Step 3: Format Examples

Present code with clear structure:

```markdown
## [Topic] Example

### Cloudformation Template
\`\`\`yaml
AWSTemplateFormatVersion: 2010-09-09
Description: [Description]
Resources:
  # ... template content
\`\`\`

### AWS SDK - Python
\`\`\`python
import boto3

# ... implementation
\`\`\`

### Terraform Module
\`\`\`hcl
resource "aws_instance" "example" {
  # ... configuration
}
\`\`\`

### AWS CLI
\`\`\`bash
aws ec2 run-instances --image-id ami-xxx ...
\`\`\`
```

### Step 4: Add Explanations

For each code example:

```markdown
### Explanation

**What this does:**
- Describes the key functionality

**Key parameters:**
- Parameter 1: Description
- Parameter 2: Description

**Before running:**
- Prerequisite 1
- Prerequisite 2

**Customization points:**
- Point 1: How to modify
- Point 2: How to modify
```

### Step 5: Provide Complete Examples

When relevant, provide:
- **Single service**: Basic example
- **Multi-service**: Complete application
- **Production-ready**: With error handling, logging, monitoring

### Step 6: Link to Resources

```markdown
### Related Resources
- AWS Documentation: [link]
- GitHub Examples: [link]
- AWS Sample Projects: [link]
- Hands-on Lab: [link]
```

## ✅ Success Criteria

- [ ] Topic/service identified
- [ ] Code examples provided (at least 2-3 formats)
- [ ] Examples include working, runnable code
- [ ] Explanations provided for each example
- [ ] Prerequisites clearly documented
- [ ] Customization guidance provided
- [ ] Related resources linked

## 📚 Example Outputs

### Example 1: Lambda API

```
/aws-examples lambda-api python

## Lambda API Gateway Example

### Architecture
```
Client → API Gateway → Lambda → DynamoDB
```

### CloudFormation Template

\`\`\`yaml
AWSTemplateFormatVersion: 2010-09-09
Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.11
      Handler: index.lambda_handler
      Code:
        ZipFile: |
          def lambda_handler(event, context):
              return {
                  'statusCode': 200,
                  'body': 'Hello from Lambda!'
              }

  ApiGateway:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: MyAPI
  # ... rest of template
\`\`\`

### AWS SDK - Python

\`\`\`python
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('items')

def lambda_handler(event, context):
    try:
        # Parse request
        body = json.loads(event.get('body', '{}'))

        # Store in DynamoDB
        response = table.put_item(
            Item={
                'id': event['pathParameters']['id'],
                'data': body,
                'created_at': str(datetime.now())
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item created'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
\`\`\`

### Before Running

1. Create DynamoDB table named 'items'
2. Create IAM role with DynamoDB permissions
3. Create API Gateway with Lambda integration
4. Test with sample JSON payload

### Customization

- Change Runtime: Update to python3.12, node.js, etc.
- Add Database: Switch DynamoDB to RDS, S3, etc.
- Add Authentication: Add API key, Cognito
- Add Logging: CloudWatch Logs integration
```

### Example 2: Auto Scaling Group

```
/aws-examples auto-scaling terraform

## Auto Scaling Group - Terraform

### Terraform Module

\`\`\`hcl
provider "aws" {
  region = "us-east-1"
}

# Launch Template
resource "aws_launch_template" "app" {
  name_prefix = "app-"

  image_id      = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type = "t3.micro"

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "app-instance"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name                = "app-asg"
  vpc_zone_identifier = ["subnet-12345", "subnet-67890"]

  min_size         = 1
  max_size         = 5
  desired_capacity = 2

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "app-asg"
    propagate_at_launch = true
  }
}

# Load Balancer
resource "aws_lb" "app" {
  name               = "app-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = ["subnet-12345", "subnet-67890"]
}

# Target Group
resource "aws_lb_target_group" "app" {
  name        = "app-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = "vpc-12345"

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    path                = "/"
  }
}

# Attach ASG to Target Group
resource "aws_autoscaling_attachment" "app" {
  autoscaling_group_name = aws_autoscaling_group.app.id
  lb_target_group_arn    = aws_lb_target_group.app.arn
}
\`\`\`

### How It Works

1. **Launch Template**: Defines instance configuration
2. **Auto Scaling Group**: Creates/destroys instances (1-5 instances, 2 desired)
3. **Load Balancer**: Distributes traffic across instances
4. **Health Check**: Automatically replaces unhealthy instances

### Deployment

\`\`\`bash
# Initialize Terraform
terraform init

# Plan changes
terraform plan

# Apply configuration
terraform apply

# Get Load Balancer DNS
terraform output lb_dns
\`\`\`

### Customization

- **Change instance count**: Update min_size, max_size, desired_capacity
- **Different AMI**: Update image_id
- **Different instance type**: Update instance_type
- **Add scaling policies**: Create aws_autoscaling_policy resources
```

## 🎯 Example Categories

**Infrastructure**:
- VPC setup, subnets, security groups
- Load balancing, auto-scaling
- Database setup, backup/restore

**Applications**:
- Web server setup
- API backend
- Microservices
- Serverless APIs

**Data**:
- S3 bucket configuration
- Data pipeline setup
- ETL with Glue
- Analytics with Athena

**CI/CD**:
- CodePipeline setup
- CodeBuild integration
- Infrastructure as Code
- Deployment automation

**Security**:
- IAM policies
- KMS encryption
- Secrets management
- Network security

---

**For explanations of services, use `/aws-docs`.**

**For service comparisons, use `/aws-compare`.**

**For complex architectures, ask the AWS Knowledge Agent.**
