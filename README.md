# ECommerce-Sales-Analysis-and-Streaming-Monitoring
This repository hosts a suite of tools for real-time sales data analysis and monitoring for an e-commerce platform. It includes AWS-powered data pipeline scripts for data ingestion, processing, and storage, along with Grafana dashboards for visual insights.  


```graphql
ECommerce-Sales-Analysis-and-Streaming-Monitoring/
├── data_generation/
│   ├── app_simulation.py             # Python script to simulate sales data generation
│   └── requirements.txt              # Python dependencies required for the data generation script
├── aws_infrastructure/
│   ├── boto3_scripts/
│   │   ├── create_kinesis_stream.py  # Boto3 script to create Kinesis Data Stream
│   │   ├── create_firehose.py        # Boto3 script to create Kinesis Firehose Delivery Stream
│   │   ├── create_kinesis_analytics.py # Boto3 script to create Kinesis Data Analytics
│   │   ├── create_s3_bucket.py       # Boto3 script to create S3 Bucket
│   │   └── create_lambda_function.py  # Boto3 script to create Lambda function
│   └── cli_scripts/
│       └── setup_infrastructure.sh    # AWS CLI scripts to set up resources that cannot be done with Boto3
├── data_processing/
│   ├── glue_jobs/
│   │   └── data_transformation.py    # AWS Glue script for data transformation
│   └── athena_queries/
│       └── query_definitions.sql     # SQL query definitions for Athena
├── monitoring/
│   ├── cloudwatch/
│   │   └── monitoring_config.json    # Configuration for CloudWatch monitoring
│   └── grafana/
│       └── dashboards/
│           └── sales_dashboard.json  # Grafana dashboard definition for data visualization
├── aws_services/
│   ├── sns/
│   │   └── send_sns_message.py       # Python script to send SNS messages from Lambda
├── config/
│   ├── credentials.json              # AWS credentials and regional configuration
│   ├── kinesis_ingestion_config.json # Configuration for Kinesis Data Stream ingestion
│   ├── kinesis_processed_config.json # Configuration for Kinesis Data Stream processed
│   ├── kinesis_analytics_config.json # Configuration for Kinesis Data Analytics
│   ├── firehose_config.json          # Configuration for Kinesis Firehose Delivery Stream
│   ├── s3_config.json                # Configuration for S3 bucket
│   ├── lambda_config.json            # Configuration for Lambda function
│   ├── athena_config.json            # Configuration for AWS Athena
│   └── sns_config.json               # Configuration for Amazon SNS
├── .gitignore                        # File to exclude files and folders from Git
└── README.md                         # Project documentation, setup, and deployment information

```
