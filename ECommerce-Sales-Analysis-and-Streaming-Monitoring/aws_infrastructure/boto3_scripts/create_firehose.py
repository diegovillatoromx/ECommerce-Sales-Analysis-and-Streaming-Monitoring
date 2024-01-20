import boto3
import json

# Load variables from the JSON configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Create a client for Kinesis Data Firehose
firehose_client = boto3.client('firehose', 
                               aws_access_key_id=config['aws_access_key_id'], 
                               aws_secret_access_key=config['aws_secret_access_key'], 
                               region_name=config['region_name'])

# Define the delivery stream name
firehose_name = config['firehose_name']

# Define the delivery stream configuration
firehose_config = config['firehose_config']

# Define the schema for source records
schema_config = config['schema_config']

# Define the S3 destination configuration
s3_destination_config = config['s3_destination_config']

# Define the buffer interval in seconds
buffer_interval = config['buffer_interval']

# Create the Kinesis Data Firehose delivery stream
response = firehose_client.create_delivery_stream(
    DeliveryStreamName=firehose_name,
    S3DestinationConfiguration={
        'RoleARN': 'arn:aws:iam::YOUR_ACCOUNT_ID:role/firehose_delivery_role',
        'BucketARN': s3_destination_config['BucketARN'],
        'Prefix': s3_destination_config['Prefix'],
        'ErrorOutputPrefix': s3_destination_config['ErrorOutputPrefix'],
        'BufferingHints': {
            'SizeInMBs': 5,
            'IntervalInSeconds': buffer_interval
        },
        'CompressionFormat': 'UNCOMPRESSED',
        'EncryptionConfiguration': {
            'NoEncryptionConfig': 'NoEncryption'
        }
    },
    ExtendedS3DestinationConfiguration={
        'RoleARN': 'arn:aws:iam::YOUR_ACCOUNT_ID:role/firehose_delivery_role',
        'BucketARN': s3_destination_config['BucketARN'],
        'Prefix': s3_destination_config['Prefix'],
        'ErrorOutputPrefix': s3_destination_config['ErrorOutputPrefix'],
        'BufferingHints': {
            'SizeInMBs': 5,
            'IntervalInSeconds': buffer_interval
        },
        'CompressionFormat': 'UNCOMPRESSED',
        'EncryptionConfiguration': {
            'NoEncryptionConfig': 'NoEncryption'
        },
        'DataFormatConversionConfiguration': {
            'Enabled': True,
            'InputFormatConfiguration': {
                'Deserializer': {
                    'OpenXJsonSerDe': {
                        'CaseInsensitive': False
                    }
                }
            },
            'OutputFormatConfiguration': {
                'Serializer': {
                    'ParquetSerDe': {
                        'Compression': 'SNAPPY'
                    }
                }
            },
            'SchemaConfiguration': {
                'CatalogId': 'AWS::Athena::Catalog',
                'DatabaseName': schema_config['DatabaseName'],
                'TableName': schema_config['TableName'],
                'Region': schema_config['Region']
            }
        }
    }
)

print("Kinesis Data Firehose delivery stream created successfully.")
