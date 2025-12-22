---
description: Search AWS documentation for a specific service and get detailed information
argument-hint: "[service-name] (optional: search query)"
allowed-tools: mcp__aws-knowledge-mcp-server__*, Read, Write
---

# AWS Documentation Search

Search the AWS Knowledge MCP Server for comprehensive documentation on a specific service.

## 🎯 Purpose

Provides instant access to official AWS service documentation including:
- Service overview and capabilities
- Configuration options and parameters
- API reference and CLI commands
- Integration patterns
- Pricing and limits
- Related services

## 📖 How To Use This Command

Use this command when you need detailed information about a specific AWS service.

### With Service Name (Recommended)

```bash
/aws-docs ec2
/aws-docs s3
/aws-docs lambda
/aws-docs dynamodb
/aws-docs vpc
```

### With Search Query

Get more specific information:

```bash
/aws-docs ec2 auto-scaling
/aws-docs s3 versioning
/aws-docs lambda performance
/aws-docs dynamodb throughput
```

### Without Arguments

If no service is specified:

```bash
/aws-docs
```

List available AWS services and let user select.

## 🔄 Execution Steps

### Step 1: Parse Arguments

- If service name provided: use it
- If search query provided: append to service search
- If no arguments: list available AWS services (EC2, S3, Lambda, RDS, DynamoDB, VPC, IAM, CloudWatch, etc.)

### Step 2: Search AWS Documentation

Using the MCP tools, search for:

```
AWS service documentation for [service-name]
Include: overview, key features, configuration, pricing, limits
```

### Step 3: Format Results

Present information in clear sections:

```markdown
## [Service Name] Documentation

### Overview
[Service description and primary use cases]

### Key Features
- Feature 1
- Feature 2
- Feature 3

### Common Configuration
[Common parameters and settings]

### Integration Points
[How it connects with other services]

### Pricing & Limits
[Relevant cost and limit information]

### Getting Started
[Links to quickstart guides]
```

### Step 4: Provide Related Services

Suggest related services that might be relevant:

```
💡 **Related Services:**
- [Service A] - Description
- [Service B] - Description
```

### Step 5: Offer Next Steps

```
📌 **Next Steps:**
- Use `/aws-compare` to compare with similar services
- Use `/aws-examples` for implementation patterns
- Ask the AWS Knowledge Agent for specific questions
```

## ✅ Success Criteria

- [ ] Service name identified or list displayed
- [ ] AWS documentation retrieved from MCP
- [ ] Information clearly formatted and organized
- [ ] Related services suggested
- [ ] Next steps offered to user

## 📚 Example Outputs

### Example 1: EC2 Service

```
/aws-docs ec2

## EC2 (Elastic Compute Cloud) Documentation

### Overview
Amazon EC2 provides resizable compute capacity in the cloud...

### Key Features
- On-demand instances
- Spot instances for cost savings
- Auto Scaling capabilities
- Multiple instance types

### Common Configuration
- Instance type selection
- Security groups
- Key pairs
- VPC association

### Pricing & Limits
- On-demand pricing varies by region and instance type
- Default limit: 20 on-demand instances per account
- Spot instances 60-90% cheaper than on-demand

💡 Related Services:
- Auto Scaling - Automatically scale EC2 fleet
- Elastic Load Balancing - Distribute traffic
- VPC - Network isolation for instances

📌 Next Steps:
- Compare with Lambda for serverless workloads
- View scaling and optimization examples
- Ask AWS Agent about best practices
```

### Example 2: S3 with Query

```
/aws-docs s3 versioning

## S3 (Simple Storage Service) - Versioning

### Versioning Overview
Enables keeping multiple versions of an object in the same bucket...

### How Versioning Works
- Default: No versioning (disabled)
- Enabled: All objects get version IDs
- Suspended: New objects not versioned

### Configuration Steps
1. Enable versioning on bucket
2. Set object retention if needed
3. Configure lifecycle rules

### Costs
- Charged for all versions stored
- Data transfer costs apply
- Storage class pricing per version

💡 Related Features:
- Object Lock - Compliance retention
- Lifecycle Policies - Automatic archiving
- Replication - Cross-region backup
```

## 🔍 Service Categories

Organize documentation by service categories:

**Compute**: EC2, Lambda, ECS, EKS, AppRunner
**Storage**: S3, EBS, EFS, Backup, DataSync
**Database**: RDS, DynamoDB, ElastiCache, Neptune, Redshift
**Networking**: VPC, Route 53, CloudFront, Direct Connect, VPN
**Security**: IAM, KMS, Secrets Manager, Security Hub, GuardDuty
**Analytics**: Athena, Glue, EMR, Kinesis, Redshift
**ML/AI**: SageMaker, Rekognition, Textract, Translate, Polly
**Integration**: SNS, SQS, EventBridge, Step Functions, AppSync
**Management**: CloudFormation, CloudWatch, Systems Manager, Config
**Development**: CodePipeline, CodeBuild, CodeDeploy, CodeCommit

---

**Note**: For complex questions or comparisons, use the AWS Knowledge Agent or the `/aws-compare` command.
