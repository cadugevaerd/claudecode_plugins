---
name: aws-best-practices
description: AWS Well-Architected Framework best practices for security, cost optimization, performance efficiency, reliability, and operational excellence
version: 1.0.0
---

# AWS Best Practices

## Overview

This skill provides comprehensive knowledge of AWS best practices based on the Well-Architected Framework, security hardening, cost optimization, performance tuning, and operational excellence patterns.

**When this skill activates**: When Claude detects questions about "AWS best practices", "how to secure AWS", "reduce AWS costs", "improve AWS performance", "AWS architecture recommendations", or Well-Architected Framework pillars.

## AWS Well-Architected Framework

The Well-Architected Framework provides a consistent approach to evaluate architectures based on five pillars:

### 1. Operational Excellence

**Focus**: Run and monitor systems to deliver business value and continually improve processes.

#### Design Principles
- Perform operations as code (Infrastructure as Code)
- Make frequent, small, reversible changes
- Refine operations procedures frequently
- Anticipate failure and learn from failures
- Improve using operational insights

#### Best Practices

**Organization**
- Define operational priorities based on business needs
- Use runbooks for routine procedures
- Use playbooks for incident response
- Have clear escalation paths

**Prepare**
```yaml
# CloudFormation for automated deployments
AWSTemplateFormatVersion: '2010-09-09'
Description: Infrastructure as Code example
Resources:
  # Define infrastructure declaratively
```

**Operate**
- Use CloudWatch for metrics and dashboards
- Set up alarms for critical thresholds
- Implement centralized logging with CloudWatch Logs
- Use AWS Config for configuration compliance

**Evolve**
- Conduct post-incident reviews
- Share learnings across teams
- Continuously improve based on metrics
- Automate repetitive tasks

### 2. Security

**Focus**: Protect data, systems, and assets through risk assessment and mitigation strategies.

#### Design Principles
- Implement a strong identity foundation
- Enable traceability
- Apply security at all layers
- Automate security best practices
- Protect data in transit and at rest
- Keep people away from data
- Prepare for security events

#### Best Practices

**Identity and Access Management (IAM)**

✅ **DO:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::my-bucket/*",
    "Condition": {
      "IpAddress": {"aws:SourceIp": "10.0.0.0/8"}
    }
  }]
}
```
- Use least privilege principle
- Enable MFA for all users
- Use IAM roles instead of long-term credentials
- Rotate credentials regularly
- Use AWS Organizations for multi-account strategy

❌ **DON'T:**
- Use root account for daily operations
- Share credentials between users
- Embed credentials in code
- Use wildcard (*) in resource ARNs

**Network Security**

```hcl
# Terraform - Security Group best practice
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Web server security group"
  vpc_id      = aws_vpc.main.id

  # Only allow specific ports
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Explicit egress rules
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-sg"
  }
}
```

- Use VPCs with private subnets for sensitive workloads
- Implement security groups as allowlists
- Use NACLs for additional defense
- Enable VPC Flow Logs
- Use AWS PrivateLink for service access

**Data Protection**

```python
# Encrypt data at rest with KMS
import boto3

kms = boto3.client('kms')
s3 = boto3.client('s3')

# Server-side encryption with KMS
s3.put_object(
    Bucket='my-bucket',
    Key='sensitive-data.txt',
    Body=data,
    ServerSideEncryption='aws:kms',
    SSEKMSKeyId='alias/my-key'
)
```

- Encrypt data at rest (S3, EBS, RDS)
- Encrypt data in transit (TLS/SSL)
- Use AWS KMS for key management
- Enable versioning for critical data
- Implement backup and recovery procedures

**Detection and Response**

- Enable CloudTrail in all regions
- Use GuardDuty for threat detection
- Set up Security Hub for central findings
- Create SNS alerts for security events
- Have an incident response plan

### 3. Reliability

**Focus**: Ensure workloads perform their intended function correctly and consistently.

#### Design Principles
- Automatically recover from failure
- Test recovery procedures
- Scale horizontally to increase availability
- Stop guessing capacity
- Manage change in automation

#### Best Practices

**Foundations**

```yaml
# Multi-AZ deployment for high availability
Resources:
  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      AvailabilityZones:
        - us-east-1a
        - us-east-1b
        - us-east-1c
      HealthCheckType: ELB
      HealthCheckGracePeriod: 300
```

- Request service quota increases proactively
- Use multiple Availability Zones
- Design for failure at every layer
- Implement circuit breakers

**Workload Architecture**

```python
# Retry with exponential backoff
import time
import random

def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = (2 ** attempt) + random.random()
            time.sleep(wait)
```

- Use loosely coupled, distributed systems
- Implement graceful degradation
- Make services stateless when possible
- Use queues to decouple components

**Change Management**

- Use blue/green deployments
- Implement canary releases
- Automate rollback procedures
- Test changes in staging environments

**Failure Management**

```bash
# Health check script
#!/bin/bash
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)
if [ "$RESPONSE" != "200" ]; then
    echo "Health check failed"
    exit 1
fi
```

- Implement health checks at all layers
- Use Auto Scaling for automatic recovery
- Set up cross-region disaster recovery
- Regularly test backup restoration

### 4. Performance Efficiency

**Focus**: Use computing resources efficiently and maintain efficiency as demand changes.

#### Design Principles
- Democratize advanced technologies
- Go global in minutes
- Use serverless architectures
- Experiment more often
- Consider mechanical sympathy

#### Best Practices

**Selection**

| Workload Type | Recommended Service |
|---------------|---------------------|
| Stateless API | Lambda + API Gateway |
| Stateful web app | ECS/EKS on Fargate |
| Batch processing | AWS Batch or Step Functions |
| Real-time streaming | Kinesis + Lambda |
| ML inference | SageMaker endpoints |

**Compute Optimization**

```yaml
# Right-sizing with Auto Scaling
Resources:
  ScalingPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      AutoScalingGroupName: !Ref AutoScalingGroup
      PolicyType: TargetTrackingScaling
      TargetTrackingConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: ASGAverageCPUUtilization
        TargetValue: 70
```

- Right-size instances based on actual usage
- Use Compute Optimizer recommendations
- Consider Graviton processors for cost/performance
- Use Spot Instances for fault-tolerant workloads

**Storage Optimization**

```python
# S3 Intelligent-Tiering for automatic optimization
s3.put_bucket_intelligent_tiering_configuration(
    Bucket='my-bucket',
    Id='AutoArchive',
    IntelligentTieringConfiguration={
        'Id': 'AutoArchive',
        'Status': 'Enabled',
        'Tierings': [
            {'Days': 90, 'AccessTier': 'ARCHIVE_ACCESS'},
            {'Days': 180, 'AccessTier': 'DEEP_ARCHIVE_ACCESS'}
        ]
    }
)
```

- Use appropriate storage class for access patterns
- Enable S3 Intelligent-Tiering
- Use EBS gp3 for cost-effective performance
- Implement caching with ElastiCache or CloudFront

**Database Optimization**

- Use read replicas for read-heavy workloads
- Enable RDS Performance Insights
- Use DynamoDB DAX for microsecond latency
- Consider Aurora for MySQL/PostgreSQL workloads

**Network Optimization**

- Use CloudFront for static content
- Enable compression
- Place resources close to users
- Use VPC endpoints for AWS services

### 5. Cost Optimization

**Focus**: Avoid unnecessary costs and understand spending patterns.

#### Design Principles
- Implement Cloud Financial Management
- Adopt a consumption model
- Measure overall efficiency
- Stop spending money on undifferentiated heavy lifting
- Analyze and attribute expenditure

#### Best Practices

**Expenditure Awareness**

```bash
# AWS CLI - Get cost breakdown
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics "BlendedCost" \
    --group-by Type=DIMENSION,Key=SERVICE
```

- Use AWS Cost Explorer for visibility
- Set up billing alerts with CloudWatch
- Tag resources for cost allocation
- Use AWS Organizations for consolidated billing

**Cost-Effective Resources**

| Strategy | Savings | Commitment |
|----------|---------|------------|
| On-Demand | 0% | None |
| Savings Plans | 30-72% | 1-3 years |
| Reserved Instances | 40-75% | 1-3 years |
| Spot Instances | 60-90% | None (interruptible) |

```python
# Request Spot Instances
ec2.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification={
        'ImageId': 'ami-12345678',
        'InstanceType': 't3.large',
        'KeyName': 'my-key'
    },
    SpotPrice='0.05',
    Type='one-time'
)
```

**Right-Sizing**

- Review AWS Compute Optimizer recommendations
- Use CloudWatch metrics to identify underutilized resources
- Implement auto-scaling to match demand
- Delete unused resources (EBS volumes, EIPs, snapshots)

**Waste Elimination**

```yaml
# Auto-delete old snapshots
Resources:
  SnapshotLifecyclePolicy:
    Type: AWS::DLM::LifecyclePolicy
    Properties:
      Description: Delete snapshots older than 30 days
      State: ENABLED
      PolicyDetails:
        Schedules:
          - Name: Weekly
            RetainRule:
              Count: 4
```

- Implement lifecycle policies for S3 and EBS
- Use AWS Instance Scheduler to stop dev/test instances
- Delete unattached EBS volumes
- Remove unused Elastic IPs
- Clean up old AMIs and snapshots

## Security Hardening Checklist

### Account Level
- [ ] Enable MFA on root account
- [ ] Create IAM users (don't use root)
- [ ] Enable CloudTrail in all regions
- [ ] Set up billing alerts
- [ ] Enable GuardDuty
- [ ] Configure AWS Config rules

### Network Level
- [ ] Use VPC with private subnets
- [ ] Enable VPC Flow Logs
- [ ] Restrict security group rules
- [ ] Use NACLs for additional control
- [ ] Enable AWS Shield (DDoS protection)
- [ ] Configure WAF for web applications

### Data Level
- [ ] Enable encryption at rest (S3, EBS, RDS)
- [ ] Enable encryption in transit (TLS)
- [ ] Use AWS KMS for key management
- [ ] Enable S3 versioning for critical data
- [ ] Configure cross-region replication for DR
- [ ] Implement backup procedures

### Application Level
- [ ] Use Secrets Manager for credentials
- [ ] Implement least privilege IAM roles
- [ ] Enable application logging
- [ ] Use Parameter Store for configuration
- [ ] Implement input validation
- [ ] Enable AWS X-Ray for tracing

## Cost Optimization Checklist

### Quick Wins
- [ ] Delete unused EBS volumes
- [ ] Release unused Elastic IPs
- [ ] Remove old snapshots and AMIs
- [ ] Stop dev/test instances off-hours
- [ ] Right-size underutilized instances
- [ ] Use S3 lifecycle policies

### Medium-Term Savings
- [ ] Purchase Savings Plans for steady workloads
- [ ] Use Spot Instances for fault-tolerant workloads
- [ ] Migrate to Graviton instances
- [ ] Implement auto-scaling
- [ ] Use Reserved Capacity for databases
- [ ] Optimize data transfer costs

### Long-Term Strategy
- [ ] Implement tagging strategy for cost allocation
- [ ] Set up Cost Anomaly Detection
- [ ] Review architecture for serverless opportunities
- [ ] Consider multi-region cost optimization
- [ ] Implement FinOps practices
- [ ] Regular Well-Architected Reviews

## Common Anti-Patterns to Avoid

### Security Anti-Patterns
❌ Using root credentials for daily operations
❌ Hardcoding credentials in code
❌ Overly permissive IAM policies (*)
❌ Public S3 buckets with sensitive data
❌ Disabled CloudTrail logging
❌ Unencrypted sensitive data

### Cost Anti-Patterns
❌ Running instances 24/7 for dev/test
❌ Over-provisioning "just in case"
❌ Ignoring Reserved Instance recommendations
❌ Not using lifecycle policies
❌ Untagged resources
❌ Not monitoring costs regularly

### Reliability Anti-Patterns
❌ Single AZ deployments for production
❌ No health checks or auto-recovery
❌ Manual deployments without rollback
❌ Untested backup procedures
❌ No circuit breakers for dependencies
❌ Tightly coupled architectures

### Performance Anti-Patterns
❌ Wrong storage class for access pattern
❌ No caching strategy
❌ Synchronous processing for async workloads
❌ Not using CDN for static content
❌ Unoptimized database queries
❌ No performance monitoring

## Next Steps

- Use `/aws-docs` for specific service documentation
- Use `/aws-compare` to evaluate service options
- Use `/aws-examples` for implementation patterns
- Ask AWS Knowledge Agent for architecture reviews
