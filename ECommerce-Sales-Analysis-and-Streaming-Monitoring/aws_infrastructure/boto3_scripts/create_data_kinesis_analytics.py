import boto3
import json

# Load configuration from the JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Initialize the AWS client
client = boto3.client('kinesisanalyticsv2')

# Create a Data Analytics application
response = client.create_application(
    ApplicationName=config["application_name"],
    RuntimeEnvironment='FLINK-1_13',
    ApplicationConfiguration={
        'FlinkApplicationConfiguration': {
            'CheckpointConfiguration': {
                'ConfigurationType': 'DEFAULT',
            },
            'MonitoringConfiguration': {
                'ConfigurationType': 'CUSTOM',
                'LogLevel': 'INFO',
                'MetricsLevel': 'APPLICATION',
            },
        },
        'SqlApplicationConfiguration': {
            'Inputs': [
                {
                    'NamePrefix': 'SOURCE_SQL_STREAM',
                    'KinesisStreamsInput': {
                        'ResourceARN': config["input_stream_arn"],
                        'RoleARN': config["input_role_arn"],
                    },
                    'InputSchema': {
                        'RecordFormat': {
                            'RecordFormatType': 'JSON',
                            'MappingParameters': {
                                'JSONMappingParameters': {
                                    'RecordRowPath': '$',
                                },
                            },
                        },
                        'RecordEncoding': 'UTF-8',
                    },
                },
            ],
            'Outputs': [
                {
                    'NamePrefix': 'DESTINATION_SQL_STREAM',
                    'KinesisStreamsOutput': {
                        'ResourceARN': config["output_stream_arn"],
                        'RoleARN': config["output_role_arn"],
                    },
                    'DestinationSchema': {
                        'RecordFormatType': 'JSON',
                    },
                },
            ],
        },
    },
)

# Print the result
print("Application ARN:", response['ApplicationDetail']['ApplicationARN'])
