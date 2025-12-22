---
description: Compare two AWS services to understand differences, use cases, and trade-offs
argument-hint: "<service1> <service2>"
allowed-tools: mcp__aws-knowledge-mcp-server__*, Read, Write
---

# AWS Service Comparison

Compare two AWS services side-by-side to understand their differences and determine which is best for your use case.

## 🎯 Purpose

Provides comparative analysis between AWS services including:
- Architecture and design patterns
- Performance characteristics
- Scaling capabilities
- Cost models
- Integration options
- Use case suitability
- Migration considerations

## 📖 How To Use This Command

Use this command when deciding between similar AWS services.

### Examples

```bash
/aws-compare ec2 lambda
/aws-compare s3 ebs
/aws-compare rds dynamodb
/aws-compare kinesis eventbridge
/aws-compare farce ecs
/aws-compare elasticache memorydb
```

### Common Comparisons

**Compute**:
- EC2 vs Lambda
- ECS vs EKS
- AppRunner vs ECS

**Storage**:
- S3 vs EBS
- EBS vs EFS
- S3 vs Glacier

**Database**:
- RDS vs DynamoDB
- DynamoDB vs ElastiCache
- Aurora vs RDS

**Messaging**:
- SNS vs SQS
- SQS vs Kinesis
- EventBridge vs SNS

## 🔄 Execution Steps

### Step 1: Validate Services

Ensure both services exist in AWS documentation:
- Check service1 exists
- Check service2 exists
- If invalid: suggest correct service names

### Step 2: Retrieve Service Details

Search AWS documentation for both services:
- Architecture
- Key features
- Performance specs
- Pricing model
- Use cases
- Limitations

### Step 3: Create Comparison Table

Build a comprehensive comparison with key dimensions:

```markdown
## [Service1] vs [Service2] Comparison

| Aspect | [Service1] | [Service2] |
|--------|-----------|-----------|
| **Type** | ... | ... |
| **Compute Model** | ... | ... |
| **Scaling** | ... | ... |
| **Cost Model** | ... | ... |
| **Latency** | ... | ... |
| **Setup Complexity** | ... | ... |
```

### Step 4: Detailed Analysis

For each key dimension:

```markdown
### Architecture

**[Service1]**: Description and diagram concept

**[Service2]**: Description and diagram concept

### Performance & Scaling

**[Service1]**: Details on performance, scaling mechanisms

**[Service2]**: Details on performance, scaling mechanisms
```

### Step 5: Use Case Analysis

```markdown
### When to Use [Service1]
- Use case 1
- Use case 2
- Specific requirements
- Example: ...

### When to Use [Service2]
- Use case 1
- Use case 2
- Specific requirements
- Example: ...
```

### Step 6: Cost Comparison

```markdown
### Cost Model Comparison

**[Service1]**
- Pricing dimension 1: ...
- Pricing dimension 2: ...
- Typical cost range: $X-$Y

**[Service2]**
- Pricing dimension 1: ...
- Pricing dimension 2: ...
- Typical cost range: $X-$Y
```

### Step 7: Migration & Interoperability

```markdown
### Migration Considerations

- Can you migrate from one to the other?
- Data transfer requirements
- Downtime considerations
- Tools and processes

### Integration Points

- How do they work together?
- Common architectural patterns
- Complementary services
```

## ✅ Success Criteria

- [ ] Both services validated
- [ ] Comparison table created with key dimensions
- [ ] Use case analysis provided
- [ ] Cost models clearly explained
- [ ] Migration paths discussed (if applicable)
- [ ] Clear recommendation guidance offered

## 📚 Example Outputs

### Example 1: EC2 vs Lambda

```
/aws-compare ec2 lambda

## EC2 vs Lambda Comparison

| Aspect | EC2 | Lambda |
|--------|-----|--------|
| **Type** | IaaS - Full VM | FaaS - Functions |
| **Compute Model** | Always running | Event-driven |
| **Scaling** | Manual/Auto Scaling | Automatic |
| **Minimum Cost** | ~$3-10/month | Free tier + pay per execution |
| **Execution Limit** | No limit | 15 minutes max |
| **Startup Time** | Minutes | Milliseconds (cold start) |
| **Infrastructure** | You manage OS & runtime | AWS manages |

### When to Use EC2
- Long-running applications (web servers, databases)
- Need full OS control
- Complex software dependencies
- Constant resource needs
- Cost-sensitive continuous workloads

### When to Use Lambda
- Event-driven workloads
- Sporadic, unpredictable traffic
- Microservices and APIs
- Data processing and transformations
- Short-duration tasks (<15 min)

### Cost Comparison

**EC2**: Fixed monthly cost ~$10-100+ depending on instance type
**Lambda**: ~$0.0000002 per function invocation + memory/duration charges
- Small, infrequent workloads: Lambda 90% cheaper
- Constant 24/7 workload: EC2 10-100x cheaper

### Architecture Pattern

Many applications use both:
```
API Gateway → Lambda (API layer)
           ↓
      EC2 (backend services)
```

💡 **Recommendation**: Choose based on workload pattern:
- Bursty/event-driven → Lambda
- Constant/long-running → EC2
- Hybrid → Use both
```

### Example 2: RDS vs DynamoDB

```
/aws-compare rds dynamodb

## RDS vs DynamoDB Comparison

| Aspect | RDS | DynamoDB |
|--------|-----|----------|
| **Type** | Relational SQL | NoSQL KeyValue |
| **Schema** | Fixed schema | Flexible schema |
| **Queries** | Complex SQL joins | Simple key lookups |
| **Consistency** | ACID transactions | Eventual consistency |
| **Scaling** | Vertical (read replicas) | Horizontal (auto) |
| **Throughput Model** | Capacity-based | On-demand or provisioned |
| **Learning Curve** | Low (SQL familiar) | Medium (NoSQL concepts) |

### Data Model Comparison

**RDS**: Structured tables with relationships
- Customer, Orders, Products tables
- Foreign keys enforce integrity
- ACID transactions across tables

**DynamoDB**: Flat key-value documents
- Store complete order with items
- No joins, denormalized data
- Single partition key queries

### When to Use RDS
- Complex relationships between data
- ACID transactions required
- Ad-hoc queries and reporting
- Existing SQL skills
- Traditional business apps

### When to Use DynamoDB
- Real-time applications (gaming, IoT)
- Massive scale (millions req/sec)
- Simple queries on single entity
- Flexible schema needed
- Cost-conscious at scale

### Real-World Example

**E-commerce Site**:
- RDS: Catalog, orders, inventory (complex queries)
- DynamoDB: User sessions, activity feed (high-speed reads)
```

## 🎯 Common Comparison Pairs

**By Category**:

**Compute**: EC2, Lambda, ECS, EKS, AppRunner, Lightsail
**Storage**: S3, EBS, EFS, Glacier, Snowball
**Database**: RDS, DynamoDB, ElastiCache, Neptune, Redshift
**Messaging**: SQS, SNS, Kinesis, EventBridge, MQ
**Container**: ECS, EKS, Fargate, Lightsail

---

**For questions about specific use cases, ask the AWS Knowledge Agent.**

**For code examples, use `/aws-examples`.**
