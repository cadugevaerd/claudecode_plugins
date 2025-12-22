# AWS Documentation Helper

A comprehensive Claude Code plugin that integrates AWS Knowledge MCP Server to provide instant access to AWS documentation, service comparisons, best practices, and troubleshooting guides.

## 🎯 Features

- ✅ **AWS Service Search** - Find detailed documentation for any AWS service
- ✅ **Service Comparison** - Compare features, pricing, and use cases between services
- ✅ **Code Examples** - Access practical examples and code snippets
- ✅ **Best Practices** - Get recommendations for security, cost-optimization, and performance
- ✅ **Troubleshooting** - Find solutions to common AWS issues
- ✅ **Intelligent Agent** - Natural language assistant for AWS-related questions

## 📦 Installation

### Add the Marketplace

```bash
/plugin marketplace add seu-usuario/claudecode-plugins
```

### Install the Plugin

```bash
/plugin install aws-documentation-helper
```

## 🚀 Usage

### Commands

#### `/aws-docs <service>`
Search for documentation of a specific AWS service.

**Examples:**
```bash
/aws-docs ec2
/aws-docs s3
/aws-docs lambda
/aws-docs rds
```

#### `/aws-compare <service1> <service2>`
Compare two AWS services to understand their differences and use cases.

**Examples:**
```bash
/aws-compare ec2 lambda
/aws-compare s3 ebs
/aws-compare rds dynamodb
```

#### `/aws-examples <topic>`
Find code examples and practical implementations for a topic.

**Examples:**
```bash
/aws-examples auto-scaling
/aws-examples vpc-setup
/aws-examples iam-policies
```

### Using the AWS Knowledge Agent

Ask questions about AWS in natural language:

- "What's the best practice for S3 security?"
- "How do I set up a VPC for high availability?"
- "Compare RDS and DynamoDB for my use case"
- "Troubleshoot Lambda cold start issues"

The agent automatically searches AWS documentation and provides comprehensive answers.

## 🔧 Components

### Commands
- `/aws-docs` - Service documentation lookup
- `/aws-compare` - Service comparison
- `/aws-examples` - Code examples and patterns

### Agent
- **aws-knowledge-agent** - Autonomous AWS knowledge assistant
  - Understands natural language AWS queries
  - Searches documentation via MCP
  - Provides contextual recommendations
  - Suggests best practices proactively

### Skills
- **aws-service-reference** - Knowledge about all AWS services
- **aws-best-practices** - Security, cost, performance patterns

### MCP Integration
- **aws-knowledge-mcp-server** - Real-time access to AWS documentation
  - HTTP endpoint: `https://knowledge-mcp.global.api.aws`
  - Covers 200+ AWS services
  - No authentication required

## 📚 AWS Services Covered

The plugin provides access to documentation for all AWS services including:

- **Compute**: EC2, Lambda, ECS, EKS, AppRunner
- **Storage**: S3, EBS, EFS, Backup
- **Database**: RDS, DynamoDB, ElastiCache, Neptune
- **Networking**: VPC, Route 53, CloudFront, Direct Connect
- **Security**: IAM, KMS, Secrets Manager, Security Hub
- **Analytics**: Athena, Glue, EMR, Kinesis
- **ML/AI**: SageMaker, Rekognition, Textract, Polly
- **Integration**: SNS, SQS, EventBridge, Step Functions
- **Management**: CloudFormation, Terraform, AWS Config
- And many more...

## 🛡️ Best Practices Guidance

The plugin covers:

- **Security**: IAM policies, encryption, VPC security, secrets management
- **Cost Optimization**: Reserved instances, spot pricing, rightsizing
- **Performance**: Scaling strategies, caching, database optimization
- **High Availability**: Multi-region, disaster recovery, failover
- **Monitoring**: CloudWatch, logging, alerting, performance metrics

## 🤔 FAQ

### Q: Do I need AWS credentials to use this plugin?
A: No, the AWS Knowledge MCP Server is public and doesn't require authentication. It provides read-only access to documentation.

### Q: Can I get pricing information?
A: Yes, the plugin can access pricing details and cost estimation guides from AWS documentation.

### Q: What if I need service-specific tutorials?
A: The agent can search documentation and provide step-by-step guides for configuration and setup.

### Q: How recent is the documentation?
A: The AWS Knowledge MCP Server is updated with the latest AWS documentation.

## 📝 Examples

### Example 1: Understanding Services

```
You: "Tell me about S3"

Agent: Searches AWS documentation and provides:
- Service overview and key features
- Common use cases
- Pricing model
- Security considerations
- Integration options
- Best practices
```

### Example 2: Troubleshooting

```
You: "My Lambda function is slow. What could be the issue?"

Agent: Analyzes and suggests:
- Cold start optimization
- Memory allocation impact
- Concurrency limits
- VPC configuration effects
- Monitoring recommendations
```

### Example 3: Architecture Planning

```
You: "Compare RDS and DynamoDB for a real-time analytics platform"

Agent: Provides:
- Use case comparison
- Performance characteristics
- Scaling capabilities
- Cost models
- Migration considerations
```

## 🔄 MCP Server Details

**Server Name**: aws-knowledge-mcp-server
**Type**: HTTP
**URL**: https://knowledge-mcp.global.api.aws
**Authentication**: None required
**Status**: Active (disabled: false)

The server provides tools for:
- Document search and retrieval
- Service information lookup
- Code example access
- Best practices guidance
- Related content discovery

## 🤝 Contributing

Contributions are welcome! Please note:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 👥 Author

**Carlos Araujo**
- Email: cadu.gevaerd@gmail.com
- GitHub: [@cadugevaerd](https://github.com/cadugevaerd)

## 🙏 Acknowledgments

This plugin integrates with the AWS Knowledge MCP Server, providing seamless access to comprehensive AWS documentation.

---

**Developed with ❤️ for the Claude Code Community**

⭐ If this plugin is helpful, consider giving it a star!
