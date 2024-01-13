# ECommerce-Sales-Analysis-and-Streaming-Monitoring
This repository hosts a suite of tools for real-time sales data analysis and monitoring for an e-commerce platform. It includes AWS-powered data pipeline scripts for data ingestion, processing, and storage, along with Grafana dashboards for visual insights. 


```css
ECommerce-Sales-Analysis-and-Streaming-Monitoring/
├── data_generation/
│   ├── app_simulation.py             # Script de Python para simular la generación de datos de ventas
│   └── requirements.txt              # Dependencias de Python necesarias para el script de generación de datos
├── aws_infrastructure/
│   ├── boto3_scripts/
│   │   ├── create_kinesis_stream.py  # Script de boto3 para crear Kinesis Data Stream
│   │   ├── create_firehose.py        # Script de boto3 para crear Kinesis Firehose Delivery Stream
│   │   └── create_s3_bucket.py       # Script de boto3 para crear S3 Bucket
│   ├── cli_scripts/
│   │   └── setup_infrastructure.sh    # AWS CLI scripts para configurar recursos que no se pueden hacer con boto3
│   └── config/
│       ├── credentials.json          # Credenciales de AWS y configuración regional
│       ├── kinesis_config.json       # Configuración para Kinesis Data Stream
│       ├── firehose_config.json      # Configuración para Kinesis Firehose Delivery Stream
│       └── s3_config.json            # Configuración para S3 bucket
├── data_processing/
│   ├── glue_jobs/
│   │   └── data_transformation.py    # Script de AWS Glue para la transformación de datos
│   └── athena_queries/
│       └── query_definitions.sql     # Definiciones de consultas SQL para Athena
├── monitoring/
│   ├── cloudwatch/
│   │   └── monitoring_config.json    # Configuración de monitoreo para CloudWatch
│   └── grafana/
│       └── dashboards/
│           └── sales_dashboard.json  # Definición del dashboard de Grafana para visualización de datos
├── .gitignore                        # Archivo para excluir archivos y carpetas de git
└── README.md                         # Documentación sobre el proyecto, configuración y despliegue

```
