---
name: aws-service-reference
description: Comprehensive knowledge of all AWS services including purpose, use cases, key features, integration points, pricing models, and service limits
version: 1.0.0
---

# AWS Service Reference

## Overview

This skill provides comprehensive reference knowledge for AWS's 200+ services across compute, storage, database, networking, security, analytics, machine learning, integration, and management categories.

**When this skill activates**: When Claude detects questions about AWS services, service selection, service capabilities, service integration, or "what AWS service should I use?"

## AWS Service Categories

### 1. **Compute Services**

#### EC2 (Elastic Compute Cloud)
- **Purpose**: Resizable virtual machines in the cloud
- **Use Cases**: Web servers, application servers, batch processing, gaming servers, HPC
- **Key Features**: Multiple instance types, On-demand/Reserved/Spot pricing, Auto Scaling, EBS volumes
- **Integration Points**: VPC, ELB, Auto Scaling, CloudWatch, IAM
- **Pricing**: Per-hour, varies by instance type and region
- **Limits**: Default 20 on-demand instances per account (adjustable)

#### Lambda (AWS Lambda)
- **Purpose**: Serverless compute - run code without provisioning servers
- **Use Cases**: API backends, data processing, scheduled tasks, event handlers, microservices
- **Key Features**: Event-driven, automatic scaling, multiple runtimes, 15-minute execution limit
- **Integration Points**: API Gateway, S3, DynamoDB, SNS, SQS, EventBridge
- **Pricing**: Per-invocation + memory/duration
- **Limits**: 15-minute max execution, 10GB RAM, 512MB /tmp storage

#### ECS (Elastic Container Service)
- **Purpose**: Container orchestration - run Docker containers at scale
- **Use Cases**: Microservices, batch processing, long-running applications
- **Key Features**: Task definitions, services, auto-scaling, Fargate (serverless)
- **Integration Points**: ECR, CloudWatch, Load Balancers, IAM
- **Pricing**: Per task hour (or per second with Fargate)
- **Limits**: Scalable, constrained by account resources

#### EKS (Elastic Kubernetes Service)
- **Purpose**: Managed Kubernetes - run and scale containerized applications
- **Use Cases**: Large-scale container orchestration, complex deployments, multi-service systems
- **Key Features**: Managed control plane, worker node management, Kubernetes ecosystem
- **Integration Points**: ECR, VPC, CloudWatch, IAM, Prometheus
- **Pricing**: Cluster management fee + worker node costs
- **Limits**: Scalable cluster size, specific to node types

#### AppRunner
- **Purpose**: Simple container deployment without infrastructure management
- **Use Cases**: Web applications, APIs, background jobs from containers/code
- **Key Features**: Automatic scaling, load balancing, HTTPS
- **Integration Points**: Source control, CloudWatch, IAM
- **Pricing**: Per vCPU-hour and memory-hour
- **Limits**: Simpler than ECS/EKS but less control

### 2. **Storage Services**

#### S3 (Simple Storage Service)
- **Purpose**: Object storage - store and retrieve any amount of data
- **Use Cases**: Data backup, static websites, data lakes, application attachments, archives
- **Key Features**: Buckets, versioning, encryption, lifecycle policies, replication, CloudFront integration
- **Integration Points**: CloudFront, Lambda, Glacier, Athena, Redshift
- **Pricing**: Per-GB stored, per request, data transfer
- **Limits**: Unlimited storage, 5TB single object limit

#### EBS (Elastic Block Store)
- **Purpose**: Block storage for EC2 instances - like virtual hard drives
- **Use Cases**: EC2 root volumes, database storage, high-IOPS applications
- **Key Features**: Snapshots, encryption, volume types (gp2/gp3, io1, st1)
- **Integration Points**: EC2, Auto Scaling, CloudWatch
- **Pricing**: Per-GB-month, snapshot storage, IOPS (if provisioned)
- **Limits**: Max volume size 64TB, Max 40 volumes per account (adjustable)

#### EFS (Elastic File System)
- **Purpose**: Shared file system accessible across EC2 instances
- **Use Cases**: Shared application data, home directories, containerized applications
- **Key Features**: NFS protocol, automatic scaling, encryption, multiple availability zones
- **Integration Points**: EC2, ECS, Lambda
- **Pricing**: Per-GB stored, per-request
- **Limits**: Scales automatically, throughput mode limits

#### Glacier
- **Purpose**: Long-term archival storage with lower cost
- **Use Cases**: Data archives, compliance/regulatory data, disaster recovery backups
- **Key Features**: Very low cost, retrieval times 1-12 hours (based on tier)
- **Integration Points**: S3 lifecycle, S3 Batch Operations
- **Pricing**: Extremely low per-GB (±$0.004/GB), retrieval costs
- **Limits**: No immediate retrieval, designed for infrequent access

### 3. **Database Services**

#### RDS (Relational Database Service)
- **Purpose**: Managed relational databases (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server)
- **Use Cases**: Structured data, ACID transactions, complex queries, traditional applications
- **Key Features**: Automated backups, multi-AZ failover, read replicas, encryption
- **Integration Points**: EC2, Lambda, DMS, CloudWatch
- **Pricing**: Per-hour for instance + storage + backup
- **Limits**: Varies by DB engine, max storage 64TB

#### DynamoDB
- **Purpose**: NoSQL key-value database with millisecond latency
- **Use Cases**: Real-time applications, sessions, IoT data, mobile backends, gaming leaderboards
- **Key Features**: Automatic scaling, global tables, encryption, streams
- **Integration Points**: Lambda, S3, Kinesis, DMS, CloudWatch
- **Pricing**: Per-request or provisioned capacity
- **Limits**: 400KB item limit, 10GB partition limit

#### ElastiCache
- **Purpose**: In-memory caching - Redis or Memcached
- **Use Cases**: Session storage, caching database queries, real-time analytics
- **Key Features**: Managed Redis/Memcached, automatic failover, encryption
- **Integration Points**: RDS, DynamoDB, EC2, CloudWatch
- **Pricing**: Per-hour for instance
- **Limits**: Max instance size varies by type

#### RedShift
- **Purpose**: Data warehouse - analyze large datasets quickly
- **Use Cases**: Business intelligence, analytics, data warehousing, historical analysis
- **Key Features**: Columnar storage, compression, distributed processing, SQL interface
- **Integration Points**: S3, Athena, QuickSight, DMS
- **Pricing**: Per-hour for nodes + storage
- **Limits**: Scalable to petabytes

### 4. **Networking Services**

#### VPC (Virtual Private Cloud)
- **Purpose**: Isolated network environment for AWS resources
- **Use Cases**: Every AWS deployment needs a VPC for network isolation
- **Key Features**: Subnets, route tables, security groups, network ACLs, gateways
- **Integration Points**: EC2, RDS, Lambda, ELB
- **Pricing**: Free for VPC itself (some components like NAT Gateway charge)
- **Limits**: 5 VPCs per account (adjustable)

#### Route 53
- **Purpose**: DNS (Domain Name System) service and domain registration
- **Use Cases**: Domain routing, health checks, multi-region failover, traffic policies
- **Key Features**: Health checks, routing policies (latency, geolocation, weighted), domain registration
- **Integration Points**: ELB, CloudFront, API Gateway, health checks
- **Pricing**: Per-hosted zone, per-query, per-health check
- **Limits**: Unlimited domains after registration

#### CloudFront
- **Purpose**: CDN (Content Delivery Network) - distribute content globally with low latency
- **Use Cases**: Website acceleration, media delivery, API acceleration, DDoS protection
- **Key Features**: Edge locations worldwide, caching, compression, WAF integration
- **Integration Points**: S3, ELB, custom origins, Lambda@Edge
- **Pricing**: Per-GB transferred, per-request, per-origin
- **Limits**: Unlimited distributions

#### ELB (Elastic Load Balancing)
- **Purpose**: Distribute incoming traffic across targets (ALB, NLB, CLB)
- **Use Cases**: High availability, scaling, traffic distribution
- **Key Features**: Auto-scaling, health checks, stickiness, multi-AZ
- **Integration Points**: EC2, ECS, Lambda, Auto Scaling, CloudWatch
- **Pricing**: Per-hour + per-LCU (processed bytes/connections)
- **Limits**: Multiple load balancers per account

### 5. **Security Services**

#### IAM (Identity and Access Management)
- **Purpose**: Control access to AWS resources - who can do what
- **Use Cases**: User management, service permissions, cross-account access, API authentication
- **Key Features**: Users, roles, policies, temporary credentials, MFA
- **Integration Points**: All AWS services
- **Pricing**: Free
- **Limits**: 5000 IAM users per account

#### KMS (Key Management Service)
- **Purpose**: Encryption key management and data encryption
- **Use Cases**: Encrypt data at rest (S3, RDS, EBS), application data encryption
- **Key Features**: Customer master keys (CMK), automatic rotation, audit logging
- **Integration Points**: S3, RDS, EBS, Lambda, Secrets Manager
- **Pricing**: Per-key-month, per-request
- **Limits**: 1000 CMKs per account (adjustable)

#### Secrets Manager
- **Purpose**: Store and rotate secrets (passwords, API keys, database credentials)
- **Use Cases**: Database credentials, API keys, OAuth tokens, certificate management
- **Key Features**: Automatic rotation, encryption, audit logging, version management
- **Integration Points**: RDS, Lambda, ECS, Databases
- **Pricing**: Per-secret per-month, per-API-call
- **Limits**: No limit on number of secrets

#### Security Hub
- **Purpose**: Central security findings and compliance status
- **Use Cases**: Security monitoring, compliance checking, vulnerability assessment
- **Key Features**: Findings aggregation, standards compliance (CIS, PCI-DSS), automated remediation
- **Integration Points**: GuardDuty, Inspector, Config, third-party tools
- **Pricing**: Per-finding-month
- **Limits**: Configurable

### 6. **Analytics Services**

#### Athena
- **Purpose**: Query data in S3 using SQL without loading into database
- **Use Cases**: Log analysis, data exploration, ad-hoc queries, cost-effective analytics
- **Key Features**: SQL (Presto), serverless, works with S3 directly
- **Integration Points**: S3, Glue, QuickSight
- **Pricing**: Per-TB scanned
- **Limits**: Concurrency and partition limits

#### Glue
- **Purpose**: Data integration - ETL (Extract, Transform, Load) service
- **Use Cases**: Data transformation, crawling, cataloging, pipeline orchestration
- **Key Features**: Crawlers, jobs (Spark/Python), data catalog
- **Integration Points**: S3, RDS, Redshift, Athena, Lambda
- **Pricing**: Per-DPU-hour, per-ETL-job
- **Limits**: Configurable by job type

#### Kinesis
- **Purpose**: Real-time data streaming and processing
- **Use Cases**: IoT data, application logs, metrics, live analytics
- **Key Features**: Streams (data), Firehose (delivery), Analytics (SQL)
- **Integration Points**: Lambda, S3, Redshift, Splunk, CloudWatch
- **Pricing**: Per-shard hour or per-GB ingested (Firehose)
- **Limits**: Per-shard throughput limits

#### QuickSight
- **Purpose**: BI (Business Intelligence) and data visualization
- **Use Cases**: Dashboards, reports, analytics, business insights
- **Key Features**: Data connectivity, visualization, Q&A, embedded analytics
- **Integration Points**: Athena, Redshift, RDS, S3
- **Pricing**: Per-user or enterprise edition
- **Limits**: Per-session API limits

### 7. **ML/AI Services**

#### SageMaker
- **Purpose**: Build, train, and deploy ML models
- **Use Cases**: Predictive analytics, image recognition, recommendation engines
- **Key Features**: Built-in algorithms, notebooks, automatic model tuning, hosting
- **Integration Points**: S3, Lambda, ECR, CloudWatch
- **Pricing**: Per-instance-hour (training/hosting)
- **Limits**: Instance type and number limits

#### Rekognition
- **Purpose**: Image and video analysis using pre-trained ML models
- **Use Cases**: Object detection, face recognition, text recognition, content moderation
- **Key Features**: Serverless, no ML expertise needed, highly accurate
- **Integration Points**: S3, Lambda, Kinesis, CloudWatch
- **Pricing**: Per-image or per-minute-of-video
- **Limits**: Request rate throttling

#### Textract
- **Purpose**: Extract text and data from scanned documents
- **Use Cases**: Document processing, form analysis, invoice processing
- **Key Features**: OCR, form recognition, table extraction, identity document processing
- **Integration Points**: S3, SNS, SQS, Textract
- **Pricing**: Per-document-page
- **Limits**: Async job limits

### 8. **Integration Services**

#### SNS (Simple Notification Service)
- **Purpose**: Publish-subscribe messaging - send messages to multiple subscribers
- **Use Cases**: Notifications, event broadcasting, alerts
- **Key Features**: Topics, subscriptions (HTTP, email, Lambda, SQS), mobile push
- **Integration Points**: Lambda, SQS, EC2, CloudWatch
- **Pricing**: Per-million-requests
- **Limits**: Large message limits

#### SQS (Simple Queue Service)
- **Purpose**: Message queuing service - decouple components
- **Use Cases**: Asynchronous processing, buffering, job queues
- **Key Features**: Standard and FIFO queues, visibility timeout, message retention
- **Integration Points**: Lambda, EC2, SNS, CloudWatch
- **Pricing**: Per-million-requests
- **Limits**: 120k messages per queue per second

#### EventBridge
- **Purpose**: Event-driven architecture - route events from sources to targets
- **Use Cases**: Serverless event routing, third-party integrations, cross-service communication
- **Key Features**: Event bus, rules, cross-account, 90+ event sources
- **Integration Points**: Lambda, SNS, SQS, Kinesis, Step Functions
- **Pricing**: Per-million-events
- **Limits**: Event size 256KB

#### Step Functions
- **Purpose**: Orchestrate distributed services into workflows
- **Use Cases**: Complex workflows, conditional logic, parallel processing, error handling
- **Key Features**: State machines, visual workflows, error handling, timeouts
- **Integration Points**: Lambda, EC2, ECS, DynamoDB, SNS
- **Pricing**: Per-state-transition
- **Limits**: Execution history, concurrent executions

### 9. **Management Services**

#### CloudWatch
- **Purpose**: Monitor applications and infrastructure - metrics, logs, alarms
- **Use Cases**: Application monitoring, log analysis, performance tracking, alerting
- **Key Features**: Metrics, logs, alarms, dashboards, anomaly detection
- **Integration Points**: All AWS services
- **Pricing**: Per-metric, per-log-ingested, per-alarm
- **Limits**: Custom metrics, log retention

#### CloudFormation
- **Purpose**: Infrastructure as Code - define AWS infrastructure as templates
- **Use Cases**: Automated infrastructure creation, stack management, disaster recovery
- **Key Features**: JSON/YAML templates, parameter management, change sets, deletion protection
- **Integration Points**: All AWS services
- **Pricing**: Free (pay for resources created)
- **Limits**: Template size, stack limits

#### AWS Config
- **Purpose**: Track resource configuration and compliance
- **Use Cases**: Compliance monitoring, configuration tracking, change auditing
- **Key Features**: Configuration items, rules, aggregation, remediation
- **Integration Points**: CloudTrail, CloudWatch, SNS, Lambda
- **Pricing**: Per-rule evaluation, per-config-item
- **Limits**: Config rules, aggregators

#### Systems Manager
- **Purpose**: Central operations for managing infrastructure
- **Use Cases**: Patch management, run commands, session manager, document automation
- **Key Features**: Parameter Store, Patch Manager, Session Manager, Document Builder
- **Integration Points**: EC2, CloudWatch, IAM, SNS
- **Pricing**: Per-resource (for some features)
- **Limits**: Parameter storage limits

## Service Selection Guide

### By Use Case

**Web Application**:
- Compute: EC2, ECS, or Lambda
- Database: RDS or DynamoDB
- Storage: S3
- CDN: CloudFront
- DNS: Route 53

**Data Analytics Pipeline**:
- Ingestion: Kinesis or S3
- Processing: Glue or EMR
- Storage: S3 or Redshift
- Query: Athena
- Visualization: QuickSight

**Real-Time Application**:
- Compute: Lambda or ECS
- Database: DynamoDB
- Messaging: Kinesis or SQS
- Caching: ElastiCache
- API: API Gateway

**Microservices Architecture**:
- Compute: ECS/EKS
- API Gateway: API Gateway
- Messaging: SNS/SQS
- Observability: CloudWatch
- Orchestration: Step Functions

## Integration Patterns

**Common Architectural Patterns**:

1. **Synchronous API**: API Gateway → Lambda → DynamoDB
2. **Asynchronous Processing**: S3 → Lambda → SQS → EC2/ECS
3. **Event-Driven**: EventBridge → Multiple targets (Lambda, SNS, SQS)
4. **Data Pipeline**: S3 → Glue → Redshift → QuickSight
5. **Stream Processing**: Kinesis → Lambda → DynamoDB
6. **Workflow Orchestration**: EventBridge → Step Functions → Multiple services

## Pricing Considerations

**Free Services**: VPC, CloudFormation, IAM, Systems Manager (basic features)

**Pay-Per-Use**: Lambda, DynamoDB, SNS, SQS, Kinesis, Athena

**Hourly**: EC2, RDS, ElastiCache, Redshift

**Hybrid**: CloudWatch (free tier + pay for extras), S3 (storage + requests)

**Enterprise**: Security Hub, Inspector, GuardDuty (per-finding)

## Common Limits & Quotas

Always check service quotas for:
- Account limits (adjustable through Support)
- Regional limits
- Rate limits (requests per second)
- Size limits (payload, storage)
- Concurrent limits (executions, connections)

Use AWS Service Quotas console to view and request increases.

## Next Steps

- Use `/aws-docs` for specific service documentation
- Use `/aws-compare` to compare two services
- Use `/aws-examples` for implementation code
- Ask AWS Knowledge Agent for architecture guidance
