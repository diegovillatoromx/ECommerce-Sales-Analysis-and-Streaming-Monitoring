import boto3
import json

# Read configuration from the JSON file
config_file = 'config/kinesis_ingestion_config.json'

with open(config_file, 'r') as f:
    config = json.load(f)

stream_name = config['stream_name']
region_name = config['region_name']
aws_access_key_id = config['aws_access_key_id']
aws_secret_access_key = config['aws_secret_access_key']

# Create a Kinesis client with the provided credentials
kinesis_client = boto3.client(
    'kinesis',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Data stream configuration parameters
shard_count = 1  # You can adjust the shard count according to your needs

# Create the data stream
response = kinesis_client.create_stream(
    StreamName=stream_name,
    ShardCount=shard_count
)

# Check if the data stream was created successfully
if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    print(f"Kinesis Data Stream '{stream_name}' created successfully in the '{region_name}' region.")
else:
    print("Failed to create the data stream.")
