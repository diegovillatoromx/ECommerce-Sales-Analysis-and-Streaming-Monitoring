import boto3
import json 
 
# Load configurations from the JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Create an AWS Data Analytics client
client = boto3.client('kinesisanalyticsv2', region_name=config['aws.region'])

# Define the application name and input/output table names
app_name = config['application_name']
input_stream_name = config['input_stream_name']
output_stream_name = config['output_stream_name']

# Create the Data Analytics application
response = client.create_application(
    ApplicationName=app_name,
    RuntimeEnvironment='FLINK-1_13',
    ApplicationConfiguration={
        'FlinkApplicationConfiguration': {
            'CheckpointConfiguration': {
                'ConfigurationType': 'DEFAULT'
            },
            'MonitoringConfiguration': {
                'ConfigurationType': 'DEFAULT'
            },
            'ParallelismConfiguration': {
                'ConfigurationType': 'CUSTOM',
                'Parallelism': 1,  # Adjust the value as needed
                'ParallelismPerKPU': 1,
                'AutoScalingEnabled': False
            },
            'JobPlan': '-- Define your Flink job plan here --'
        },
        'ApplicationCodeConfiguration': {
            'CodeContentType': 'ZIPFILE',
            'CodeContent': b'',
            'CodeContentS3Location': config['code_s3_location']  # Replace with your code location
        },
        'ApplicationSnapshotConfiguration': {
            'SnapshotsEnabled': False
        },
        'VpcConfigurations': [],
        'EnvironmentProperties': {
            'PropertyGroups': [
                {
                    'PropertyGroupId': 'Default',
                    'PropertyMap': {
                        'FLINK_PYTHON_REQUIREMENTS': config['requirements_s3_location'],  # Replace with your requirements file
                        'FLINK_PYTHON_VENV': config['venv_s3_location']  # Replace with your virtual environment
                    }
                }
            ]
        }
    }
)

# Get the application ID
app_id = response['ApplicationDetail']['ApplicationId']

# Define the input table schema
input_schema = {
    'RecordFormat': {
        'RecordFormatType': 'JSON',
        'MappingParameters': {
            'JSONMappingParameters': {
                'RecordRowPath': '$'
            }
        }
    },
    'RecordEncoding': 'UTF-8',
    'RecordColumns': config['input_columns']
}

# Create the input table
client.create_application_input(
    ApplicationName=app_name,
    CurrentApplicationVersionId=app_id,
    Input={
        'NamePrefix': 'SOURCE_SQL_STREAM',
        'KinesisStreamsInput': {
            'ResourceARN': config['input_stream_arn'],
            'RoleARN': config['input_role_arn']
        },
        'InputSchema': input_schema,
        'InputParallelism': {
            'Count': 1
        }
    }
)

# Define the output table schema
output_schema = {
    'RecordFormatType': 'JSON'
}

# Create the output table
client.create_application_output(
    ApplicationName=app_name,
    CurrentApplicationVersionId=app_id,
    Output={
        'Name': 'DESTINATION_SQL_STREAM',
        'KinesisStreamsOutput': {
            'ResourceARN': config['output_stream_arn'],
            'RoleARN': config['output_role_arn']
        },
        'DestinationSchema': output_schema
    }
)

# Start the application
client.start_application(
    ApplicationName=app_name,
    RunConfiguration={
        'FlinkRunConfiguration': {
            'AllowNonRestoredState': True
        }
    }
)

print(f"Application {app_name} created and running.")

