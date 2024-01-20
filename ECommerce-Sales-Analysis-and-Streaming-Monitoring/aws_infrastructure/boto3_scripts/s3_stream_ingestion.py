import boto3

# Read S3 configuration from the JSON file
config_file = 'config/s3_config.json'

with open(config_file, 'r') as f:
    s3_config = json.load(f)

bucket_name = s3_config['bucket_name']
region_name = s3_config['region_name']
aws_access_key_id = s3_config['aws_access_key_id']
aws_secret_access_key = s3_config['aws_secret_access_key']

# Create an S3 client with the provided credentials
s3_client = boto3.client(
    's3',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Define the bucket name and versioning configuration
bucket_name = 'data_stream_ingestion_useast1'

# Create the S3 bucket with versioning enabled
s3_client.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': region_name
    }
)

# Enable versioning for the bucket
s3_client.put_bucket_versioning(
    Bucket=bucket_name,
    VersioningConfiguration={
        'Status': 'Enabled'
    }
)

print(f"S3 bucket '{bucket_name}' created successfully with versioning enabled in the '{region_name}' region.")
