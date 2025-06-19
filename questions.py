"""
AWS Trivia Questions for Multiplayer Terminal Game
Contains 100 multiple-choice questions about AWS services and concepts
"""

questions = [
    {
        "question": "What does EC2 stand for?",
        "options": ["Elastic Compute Cloud", "Elastic Container Cloud", "Edge Control Compute", "Elastic Core Cluster"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for object storage?",
        "options": ["EBS", "S3", "EFS", "FSx"],
        "answer": 1
    },
    {
        "question": "What is the default timeout for an AWS Lambda function?",
        "options": ["1 minute", "3 seconds", "3 minutes", "15 minutes"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for serverless computing?",
        "options": ["EC2", "ECS", "Lambda", "Lightsail"],
        "answer": 2
    },
    {
        "question": "What is the maximum size of an S3 object?",
        "options": ["1 GB", "5 TB", "10 TB", "Unlimited"],
        "answer": 1
    },
    {
        "question": "Which AWS service provides a managed relational database?",
        "options": ["DynamoDB", "RDS", "ElastiCache", "Neptune"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for Infrastructure as Code?",
        "options": ["CloudFormation", "OpsWorks", "Elastic Beanstalk", "CodeDeploy"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for content delivery?",
        "options": ["Route 53", "CloudFront", "Global Accelerator", "API Gateway"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for container orchestration?",
        "options": ["ECR", "ECS", "Batch", "Fargate"],
        "answer": 1
    },
    {
        "question": "Which AWS service provides NoSQL database capabilities?",
        "options": ["RDS", "Redshift", "DynamoDB", "DocumentDB"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for virtual private cloud?",
        "options": ["VPC", "Direct Connect", "Transit Gateway", "PrivateLink"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for DNS management?",
        "options": ["CloudFront", "Route 53", "Global Accelerator", "API Gateway"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for message queuing?",
        "options": ["SNS", "SQS", "EventBridge", "Kinesis"],
        "answer": 1
    },
    {
        "question": "Which AWS service provides a managed Kubernetes service?",
        "options": ["ECS", "EKS", "Fargate", "Batch"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for data warehousing?",
        "options": ["RDS", "DynamoDB", "Redshift", "Neptune"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for identity and access management?",
        "options": ["Cognito", "IAM", "Directory Service", "SSO"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for monitoring and observability?",
        "options": ["CloudWatch", "CloudTrail", "Config", "Trusted Advisor"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed Elasticsearch service?",
        "options": ["ElastiCache", "OpenSearch Service", "MemoryDB", "DocumentDB"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for API management?",
        "options": ["AppSync", "API Gateway", "App Mesh", "App Runner"],
        "answer": 1
    },
    {
        "question": "Which AWS service is used for data migration?",
        "options": ["Storage Gateway", "DataSync", "Transfer Family", "All of the above"],
        "answer": 3
    },
    {
        "question": "What is the AWS service for machine learning?",
        "options": ["SageMaker", "Comprehend", "Rekognition", "Polly"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed Redis service?",
        "options": ["RDS", "ElastiCache", "MemoryDB", "DynamoDB Accelerator"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for serverless application repository?",
        "options": ["CodeCommit", "CodeArtifact", "Serverless Application Repository", "ECR"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for container registry?",
        "options": ["ECR", "ECS", "EKS", "App Runner"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for data streaming?",
        "options": ["Kinesis", "SQS", "SNS", "EventBridge"],
        "answer": 0
    },
    {
        "question": "Which AWS region has the code us-east-1?",
        "options": ["US East (Ohio)", "US East (N. Virginia)", "US West (Oregon)", "US West (N. California)"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for hybrid cloud storage?",
        "options": ["S3", "EFS", "Storage Gateway", "FSx"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed Apache Kafka service?",
        "options": ["Kinesis", "MSK", "EventBridge", "SQS"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for serverless data integration?",
        "options": ["Glue", "Data Pipeline", "AppFlow", "Lake Formation"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for cost management?",
        "options": ["Budgets", "Cost Explorer", "Trusted Advisor", "All of the above"],
        "answer": 3
    },
    {
        "question": "What is the AWS service for disaster recovery?",
        "options": ["Backup", "CloudEndure Disaster Recovery", "Site Recovery", "All of the above"],
        "answer": 3
    },
    {
        "question": "Which AWS service provides a managed MySQL and PostgreSQL service?",
        "options": ["RDS", "Aurora", "DocumentDB", "Neptune"],
        "answer": 1
    },
    {
        "question": "What is the AWS service for IoT?",
        "options": ["IoT Core", "IoT Greengrass", "IoT Analytics", "All of the above"],
        "answer": 3
    },
    {
        "question": "Which AWS service is used for event-driven computing?",
        "options": ["Lambda", "EventBridge", "SNS", "All of the above"],
        "answer": 3
    },
    {
        "question": "What is the AWS service for blockchain?",
        "options": ["Managed Blockchain", "Quantum Ledger Database", "Both A and B", "None of the above"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed graph database?",
        "options": ["RDS", "DynamoDB", "Neptune", "DocumentDB"],
        "answer": 2
    }
]

# Adding more questions to reach 100
more_questions = [
    {
        "question": "What is the AWS service for container orchestration without managing servers?",
        "options": ["ECS", "EKS", "Fargate", "App Runner"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed MongoDB-compatible database?",
        "options": ["RDS", "DynamoDB", "DocumentDB", "Neptune"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for data lake formation?",
        "options": ["Lake Formation", "Glue", "Athena", "EMR"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for serverless application development?",
        "options": ["Amplify", "App Runner", "Elastic Beanstalk", "Lightsail"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for private 5G networks?",
        "options": ["Private 5G", "Wavelength", "Outposts", "Local Zones"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed time series database?",
        "options": ["Timestream", "DynamoDB", "RDS", "MemoryDB"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for quantum computing?",
        "options": ["Braket", "Ground Station", "Quantum Ledger Database", "None of the above"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for satellite ground stations?",
        "options": ["Ground Station", "Direct Connect", "Global Accelerator", "Outposts"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for robotic application development?",
        "options": ["RoboMaker", "IoT Greengrass", "IoT Core", "IoT Analytics"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed Apache Cassandra service?",
        "options": ["Keyspaces", "DynamoDB", "DocumentDB", "Neptune"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for game development?",
        "options": ["GameLift", "Lumberyard", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for voice, text, and chat interfaces?",
        "options": ["Lex", "Polly", "Transcribe", "All of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for media transcoding?",
        "options": ["Elemental MediaConvert", "Elastic Transcoder", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed Kafka service?",
        "options": ["MSK", "Kinesis", "SQS", "SNS"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for contact center?",
        "options": ["Connect", "Chime", "WorkMail", "WorkDocs"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for business intelligence?",
        "options": ["QuickSight", "Athena", "Glue", "EMR"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for data migration to the cloud?",
        "options": ["Snow Family", "DataSync", "Transfer Family", "All of the above"],
        "answer": 3
    },
    {
        "question": "Which AWS service provides a managed Microsoft Active Directory?",
        "options": ["Directory Service", "IAM", "Cognito", "SSO"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for end-user computing?",
        "options": ["WorkSpaces", "AppStream 2.0", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for cloud development kits?",
        "options": ["CDK", "CloudFormation", "SAM", "All of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for security assessment?",
        "options": ["Inspector", "GuardDuty", "Macie", "Security Hub"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed Prometheus service?",
        "options": ["Managed Service for Prometheus", "CloudWatch", "X-Ray", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud map?",
        "options": ["Cloud Map", "Route 53", "Global Accelerator", "Transit Gateway"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for cloud HSM?",
        "options": ["CloudHSM", "KMS", "Secrets Manager", "Certificate Manager"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud directory?",
        "options": ["Cloud Directory", "Directory Service", "IAM", "Cognito"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed Grafana service?",
        "options": ["Managed Service for Grafana", "CloudWatch", "X-Ray", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud search?",
        "options": ["CloudSearch", "OpenSearch Service", "Kendra", "All of the above"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for cloud formation guard?",
        "options": ["CloudFormation Guard", "Config", "Security Hub", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud control API?",
        "options": ["Cloud Control API", "CloudFormation", "CDK", "None of the above"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed Apache Flink service?",
        "options": ["Kinesis Data Analytics", "MSK", "EMR", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud WAN?",
        "options": ["Cloud WAN", "Transit Gateway", "Direct Connect", "VPC"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for cloud shell?",
        "options": ["CloudShell", "Systems Manager", "Cloud9", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud front functions?",
        "options": ["CloudFront Functions", "Lambda@Edge", "Both A and B", "None of the above"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed Apache HBase service?",
        "options": ["EMR", "MSK", "DynamoDB", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud trail?",
        "options": ["CloudTrail", "CloudWatch", "Config", "None of the above"],
        "answer": 0
    },
    {
        "question": "Which AWS service is used for cloud formation drift detection?",
        "options": ["CloudFormation", "Config", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation registry?",
        "options": ["CloudFormation Registry", "Service Catalog", "Both A and B", "None of the above"],
        "answer": 0
    },
    {
        "question": "Which AWS service provides a managed Apache Airflow service?",
        "options": ["MWAA", "Step Functions", "Batch", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud formation stack sets?",
        "options": ["CloudFormation StackSets", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for cloud formation custom resources?",
        "options": ["CloudFormation", "Lambda", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation macros?",
        "options": ["CloudFormation Macros", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed Apache Spark service?",
        "options": ["EMR", "Glue", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation hooks?",
        "options": ["CloudFormation Hooks", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for cloud formation change sets?",
        "options": ["CloudFormation Change Sets", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation templates?",
        "options": ["CloudFormation Templates", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed Apache Hadoop service?",
        "options": ["EMR", "Glue", "Both A and B", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud formation designer?",
        "options": ["CloudFormation Designer", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for cloud formation exports?",
        "options": ["CloudFormation Exports", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation imports?",
        "options": ["CloudFormation Imports", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed Apache Zookeeper service?",
        "options": ["MSK", "EMR", "Both A and B", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud formation nested stacks?",
        "options": ["CloudFormation Nested Stacks", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for cloud formation parameters?",
        "options": ["CloudFormation Parameters", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation outputs?",
        "options": ["CloudFormation Outputs", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed Apache Hive service?",
        "options": ["EMR", "Glue", "Both A and B", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud formation conditions?",
        "options": ["CloudFormation Conditions", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for cloud formation mappings?",
        "options": ["CloudFormation Mappings", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation resources?",
        "options": ["CloudFormation Resources", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed Apache Pig service?",
        "options": ["EMR", "Glue", "Both A and B", "None of the above"],
        "answer": 0
    },
    {
        "question": "What is the AWS service for cloud formation metadata?",
        "options": ["CloudFormation Metadata", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for cloud formation transform?",
        "options": ["CloudFormation Transform", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation wait conditions?",
        "options": ["CloudFormation Wait Conditions", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service provides a managed Apache Presto service?",
        "options": ["Athena", "EMR", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation deletion policy?",
        "options": ["CloudFormation Deletion Policy", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "Which AWS service is used for cloud formation update policy?",
        "options": ["CloudFormation Update Policy", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    },
    {
        "question": "What is the AWS service for cloud formation creation policy?",
        "options": ["CloudFormation Creation Policy", "CloudFormation", "Both A and B", "None of the above"],
        "answer": 2
    }
]

questions.extend(more_questions)
