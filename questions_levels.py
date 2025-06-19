"""
AWS Trivia Questions organized by difficulty levels
Multi-level progression system for AWS knowledge assessment
"""

# Level 1: Beginner - Basic AWS Services and Concepts
level_1_questions = [
    {
        "question": "What does EC2 stand for?",
        "options": ["Elastic Compute Cloud", "Elastic Container Cloud", "Edge Control Compute", "Elastic Core Cluster"],
        "answer": 0,
        "difficulty": "beginner",
        "category": "Compute"
    },
    {
        "question": "Which AWS service is used for object storage?",
        "options": ["EBS", "S3", "EFS", "FSx"],
        "answer": 1,
        "difficulty": "beginner",
        "category": "Storage"
    },
    {
        "question": "What is AWS Lambda used for?",
        "options": ["Virtual machines", "Serverless computing", "Database management", "Content delivery"],
        "answer": 1,
        "difficulty": "beginner",
        "category": "Compute"
    },
    {
        "question": "Which AWS service provides a managed relational database?",
        "options": ["DynamoDB", "RDS", "ElastiCache", "Neptune"],
        "answer": 1,
        "difficulty": "beginner",
        "category": "Database"
    },
    {
        "question": "What is CloudFront used for?",
        "options": ["Database storage", "Content delivery", "Virtual networking", "Server monitoring"],
        "answer": 1,
        "difficulty": "beginner",
        "category": "Networking"
    },
    {
        "question": "Which service is AWS's Infrastructure as Code solution?",
        "options": ["CloudFormation", "OpsWorks", "Elastic Beanstalk", "CodeDeploy"],
        "answer": 0,
        "difficulty": "beginner",
        "category": "Management"
    },
    {
        "question": "What does VPC stand for?",
        "options": ["Virtual Private Cloud", "Virtual Public Cloud", "Virtual Protected Cloud", "Virtual Primary Cloud"],
        "answer": 0,
        "difficulty": "beginner",
        "category": "Networking"
    },
    {
        "question": "Which AWS service is used for DNS management?",
        "options": ["CloudFront", "Route 53", "API Gateway", "Load Balancer"],
        "answer": 1,
        "difficulty": "beginner",
        "category": "Networking"
    },
    {
        "question": "What is the AWS service for NoSQL databases?",
        "options": ["RDS", "DynamoDB", "Aurora", "Redshift"],
        "answer": 1,
        "difficulty": "beginner",
        "category": "Database"
    },
    {
        "question": "Which service provides AWS identity and access management?",
        "options": ["IAM", "Cognito", "Directory Service", "SSO"],
        "answer": 0,
        "difficulty": "beginner",
        "category": "Security"
    }
]

# Level 2: Intermediate - AWS Architecture and Best Practices
level_2_questions = [
    {
        "question": "What is the maximum timeout for an AWS Lambda function?",
        "options": ["5 minutes", "10 minutes", "15 minutes", "30 minutes"],
        "answer": 2,
        "difficulty": "intermediate",
        "category": "Compute"
    },
    {
        "question": "Which S3 storage class is most cost-effective for long-term archival?",
        "options": ["Standard", "Intelligent-Tiering", "Glacier Deep Archive", "One Zone-IA"],
        "answer": 2,
        "difficulty": "intermediate",
        "category": "Storage"
    },
    {
        "question": "What is the difference between Application Load Balancer and Network Load Balancer?",
        "options": ["ALB operates at Layer 7, NLB at Layer 4", "ALB is faster than NLB", "NLB supports HTTP/HTTPS only", "No significant difference"],
        "answer": 0,
        "difficulty": "intermediate",
        "category": "Networking"
    },
    {
        "question": "Which RDS engine supports read replicas across regions?",
        "options": ["MySQL only", "PostgreSQL only", "All engines", "MySQL and PostgreSQL only"],
        "answer": 3,
        "difficulty": "intermediate",
        "category": "Database"
    },
    {
        "question": "What is the purpose of AWS CloudTrail?",
        "options": ["Performance monitoring", "API call logging", "Cost optimization", "Resource provisioning"],
        "answer": 1,
        "difficulty": "intermediate",
        "category": "Management"
    },
    {
        "question": "Which EC2 instance type is optimized for memory-intensive applications?",
        "options": ["C5", "M5", "R5", "T3"],
        "answer": 2,
        "difficulty": "intermediate",
        "category": "Compute"
    },
    {
        "question": "What is the maximum number of VPCs per region by default?",
        "options": ["5", "10", "20", "100"],
        "answer": 0,
        "difficulty": "intermediate",
        "category": "Networking"
    },
    {
        "question": "Which AWS service provides managed Kubernetes?",
        "options": ["ECS", "EKS", "Fargate", "Batch"],
        "answer": 1,
        "difficulty": "intermediate",
        "category": "Containers"
    },
    {
        "question": "What is the purpose of AWS Systems Manager Parameter Store?",
        "options": ["Store application logs", "Store configuration data", "Store backup files", "Store user credentials only"],
        "answer": 1,
        "difficulty": "intermediate",
        "category": "Management"
    },
    {
        "question": "Which service is used for real-time data streaming?",
        "options": ["SQS", "SNS", "Kinesis", "EventBridge"],
        "answer": 2,
        "difficulty": "intermediate",
        "category": "Analytics"
    }
]

# Level 3: Advanced - Complex AWS Architectures and Optimization
level_3_questions = [
    {
        "question": "What is the most efficient way to transfer 100TB of data to AWS?",
        "options": ["Direct Connect", "VPN", "AWS Snowball Edge", "Internet upload"],
        "answer": 2,
        "difficulty": "advanced",
        "category": "Migration"
    },
    {
        "question": "Which DynamoDB feature provides point-in-time recovery?",
        "options": ["Global Tables", "DynamoDB Streams", "Backup and Restore", "DAX"],
        "answer": 2,
        "difficulty": "advanced",
        "category": "Database"
    },
    {
        "question": "What is the maximum duration for STS temporary credentials?",
        "options": ["1 hour", "12 hours", "24 hours", "36 hours"],
        "answer": 3,
        "difficulty": "advanced",
        "category": "Security"
    },
    {
        "question": "Which Lambda deployment configuration provides the safest rollout?",
        "options": ["All at once", "Linear10PercentEvery1Minute", "Canary10Percent5Minutes", "Blue/Green"],
        "answer": 2,
        "difficulty": "advanced",
        "category": "Deployment"
    },
    {
        "question": "What is the purpose of AWS PrivateLink?",
        "options": ["VPC peering", "Private connectivity to AWS services", "Internet gateway", "NAT gateway"],
        "answer": 1,
        "difficulty": "advanced",
        "category": "Networking"
    },
    {
        "question": "Which CloudFormation feature allows conditional resource creation?",
        "options": ["Parameters", "Mappings", "Conditions", "Outputs"],
        "answer": 2,
        "difficulty": "advanced",
        "category": "Infrastructure"
    },
    {
        "question": "What is the maximum message retention period for SQS?",
        "options": ["7 days", "14 days", "30 days", "1 year"],
        "answer": 1,
        "difficulty": "advanced",
        "category": "Messaging"
    },
    {
        "question": "Which EC2 placement group type provides the lowest latency?",
        "options": ["Cluster", "Partition", "Spread", "All are equal"],
        "answer": 0,
        "difficulty": "advanced",
        "category": "Compute"
    },
    {
        "question": "What is the purpose of AWS Config Rules?",
        "options": ["Cost optimization", "Compliance monitoring", "Performance tuning", "Security scanning"],
        "answer": 1,
        "difficulty": "advanced",
        "category": "Governance"
    },
    {
        "question": "Which service provides the most granular billing information?",
        "options": ["Cost Explorer", "Billing Dashboard", "Cost and Usage Reports", "Budgets"],
        "answer": 2,
        "difficulty": "advanced",
        "category": "Billing"
    }
]

# Level 4: Expert - AWS Specialty Services and Edge Cases
level_4_questions = [
    {
        "question": "What is the maximum number of Lambda layers per function?",
        "options": ["3", "5", "10", "15"],
        "answer": 1,
        "difficulty": "expert",
        "category": "Serverless"
    },
    {
        "question": "Which AWS service provides quantum computing capabilities?",
        "options": ["SageMaker", "Braket", "DeepRacer", "Comprehend"],
        "answer": 1,
        "difficulty": "expert",
        "category": "Emerging Tech"
    },
    {
        "question": "What is the maximum size of a CloudFormation template?",
        "options": ["51,200 bytes", "460,800 bytes", "1 MB", "10 MB"],
        "answer": 1,
        "difficulty": "expert",
        "category": "Infrastructure"
    },
    {
        "question": "Which DynamoDB operation is most cost-effective for large scans?",
        "options": ["Scan", "Query", "BatchGetItem", "ParallelScan"],
        "answer": 3,
        "difficulty": "expert",
        "category": "Database"
    },
    {
        "question": "What is the purpose of AWS Outposts?",
        "options": ["Edge computing", "Hybrid cloud infrastructure", "IoT management", "Content delivery"],
        "answer": 1,
        "difficulty": "expert",
        "category": "Hybrid"
    },
    {
        "question": "Which service provides the lowest latency for real-time ML inference?",
        "options": ["SageMaker Endpoints", "Lambda", "EC2 with GPU", "SageMaker Multi-Model Endpoints"],
        "answer": 2,
        "difficulty": "expert",
        "category": "Machine Learning"
    },
    {
        "question": "What is the maximum number of rules per AWS Config rule?",
        "options": ["50", "100", "150", "200"],
        "answer": 2,
        "difficulty": "expert",
        "category": "Governance"
    },
    {
        "question": "Which AWS service provides blockchain capabilities?",
        "options": ["QLDB", "Managed Blockchain", "Both A and B", "Neither"],
        "answer": 2,
        "difficulty": "expert",
        "category": "Blockchain"
    },
    {
        "question": "What is the maximum concurrent executions limit for Lambda by default?",
        "options": ["100", "500", "1000", "10000"],
        "answer": 2,
        "difficulty": "expert",
        "category": "Serverless"
    },
    {
        "question": "Which AWS service provides the most comprehensive security posture management?",
        "options": ["Security Hub", "GuardDuty", "Inspector", "Macie"],
        "answer": 0,
        "difficulty": "expert",
        "category": "Security"
    }
]

# Level 5: Master - AWS Architect Professional Level
level_5_questions = [
    {
        "question": "What is the optimal strategy for cross-region disaster recovery with RTO < 1 hour?",
        "options": ["Backup and Restore", "Pilot Light", "Warm Standby", "Multi-Site Active/Active"],
        "answer": 2,
        "difficulty": "master",
        "category": "Disaster Recovery"
    },
    {
        "question": "Which combination provides the most cost-effective data lake architecture?",
        "options": ["S3 + Athena + Glue", "Redshift + Spectrum", "EMR + S3", "All are equally cost-effective"],
        "answer": 0,
        "difficulty": "master",
        "category": "Analytics"
    },
    {
        "question": "What is the most secure way to provide cross-account access to S3?",
        "options": ["Bucket policies", "IAM roles with trust policies", "Access Control Lists", "Pre-signed URLs"],
        "answer": 1,
        "difficulty": "master",
        "category": "Security"
    },
    {
        "question": "Which architecture pattern best handles unpredictable traffic spikes?",
        "options": ["Auto Scaling + ALB", "Lambda + API Gateway", "ECS Fargate + ALB", "All can handle spikes equally"],
        "answer": 1,
        "difficulty": "master",
        "category": "Architecture"
    },
    {
        "question": "What is the most efficient way to migrate a 500TB database with minimal downtime?",
        "options": ["AWS DMS", "AWS SCT + DMS", "Database native replication + DMS", "Snowball + DMS"],
        "answer": 2,
        "difficulty": "master",
        "category": "Migration"
    },
    {
        "question": "Which service combination provides the best observability for microservices?",
        "options": ["CloudWatch + X-Ray", "CloudTrail + Config", "Systems Manager + CloudWatch", "All provide equal observability"],
        "answer": 0,
        "difficulty": "master",
        "category": "Monitoring"
    },
    {
        "question": "What is the most cost-effective way to process 1PB of data monthly?",
        "options": ["EMR with Spot instances", "Athena with partitioning", "Redshift with RA3 nodes", "Depends on query patterns"],
        "answer": 3,
        "difficulty": "master",
        "category": "Big Data"
    },
    {
        "question": "Which networking design provides the best security for multi-tier applications?",
        "options": ["Public subnets only", "Private subnets with NAT", "Transit Gateway with route tables", "VPC endpoints with private subnets"],
        "answer": 3,
        "difficulty": "master",
        "category": "Networking"
    },
    {
        "question": "What is the optimal Lambda memory configuration for CPU-intensive tasks?",
        "options": ["128 MB", "512 MB", "1008 MB", "3008 MB"],
        "answer": 3,
        "difficulty": "master",
        "category": "Performance"
    },
    {
        "question": "Which approach provides the best compliance for financial services?",
        "options": ["AWS Config + CloudTrail", "Security Hub + GuardDuty", "Control Tower + Organizations", "All are required together"],
        "answer": 3,
        "difficulty": "master",
        "category": "Compliance"
    }
]

# Organize all levels
levels = {
    1: {
        "name": "AWS Fundamentals",
        "description": "Basic AWS services and core concepts",
        "questions": level_1_questions,
        "pass_percentage": 100,
        "unlock_message": "🎉 Perfect score! You've mastered AWS Fundamentals. Ready for Intermediate level?"
    },
    2: {
        "name": "AWS Intermediate",
        "description": "AWS architecture patterns and best practices",
        "questions": level_2_questions,
        "pass_percentage": 100,
        "unlock_message": "🚀 Excellent! You're ready for Advanced AWS concepts. Continue your journey!"
    },
    3: {
        "name": "AWS Advanced",
        "description": "Complex architectures and optimization strategies",
        "questions": level_3_questions,
        "pass_percentage": 100,
        "unlock_message": "⭐ Outstanding! You've reached Expert level. Time for specialty services!"
    },
    4: {
        "name": "AWS Expert",
        "description": "Specialty services and edge cases",
        "questions": level_4_questions,
        "pass_percentage": 100,
        "unlock_message": "🏆 Incredible! You're now at Master level - the ultimate AWS challenge!"
    },
    5: {
        "name": "AWS Master",
        "description": "Architect Professional level expertise",
        "questions": level_5_questions,
        "pass_percentage": 100,
        "unlock_message": "👑 CONGRATULATIONS! You are an AWS MASTER! You've conquered all levels!"
    }
}

def get_level_info(level_number):
    """Get information about a specific level"""
    return levels.get(level_number, None)

def get_questions_for_level(level_number):
    """Get questions for a specific level"""
    level_info = levels.get(level_number)
    if level_info:
        return level_info["questions"]
    return []

def get_max_level():
    """Get the maximum available level"""
    return max(levels.keys())

def get_level_names():
    """Get all level names"""
    return {level: info["name"] for level, info in levels.items()}

# Backward compatibility - default questions for existing functionality
questions = level_1_questions  # Default to level 1 for existing code
