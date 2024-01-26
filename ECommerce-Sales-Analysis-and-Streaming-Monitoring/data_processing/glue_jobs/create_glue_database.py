import boto3
import json

# Read configuration from JSON file
config_file = 'config/glue_config.json' 
with open(config_file, 'r') as f:
    config = json.load(f)

# Initialize Glue client
glue_client = boto3.client('glue', 
    region_name=config['region_name'], 
    aws_access_key_id=config['aws_access_key_id'], 
    aws_secret_access_key=config['aws_secret_access_key']
)

# Define database name
database_name = config['database_name']

# Create the database
response = glue_client.create_database(
    DatabaseInput={
        'Name': database_name,
        'Description': 'Database for storing Ecommerce data from Kinesis'
    }
)

if 'Database' in response:
    print(f"Database '{database_name}' created successfully.")
else:
    print(f"Failed to create database '{database_name}'.")

# Define table details
table_name = config['table_name']
table_description = 'Table for storing Ecommerce data from Kinesis'
location = config['location']
table_input_format = config['table_input_format']
table_output_format = config['table_output_format']
serde_library = config['serde_library']

# Create the table
response = glue_client.create_table(
    DatabaseName=database_name,
    TableInput={
        'Name': table_name,
        'Description': table_description,
        'StorageDescriptor': {
            'Columns': [
                {
                    'Name': 'purchase_ID',
                    'Type': 'string'
                },
                {
                    'Name': 'Product_name',
                    'Type': 'string'
                },
                {
                    'Name': 'Pricing',
                    'Type': 'decimal'
                },
                {
                    'Name': 'Commission',
                    'Type': 'decimal'
                },
                {
                    'Name': 'Revenue',
                    'Type': 'decimal'
                },
                {
                    'Name': 'Payment_Method',
                    'Type': 'string'
                },
                {
                    'Name': 'Status',
                    'Type': 'string'
                },
                {
                    'Name': 'Order_Type',
                    'Type': 'string'
                },
                {
                    'Name': 'City',
                    'Type': 'string'
                },
                {
                    'Name': 'Latitude',
                    'Type': 'decimal'
                },
                {
                    'Name': 'Longitude',
                    'Type': 'decimal'
                },
                {
                    'Name': 'Source',
                    'Type': 'string'
                },
                {
                    'Name': 'Brand',
                    'Type': 'string'
                },
                {
                    'Name': 'Category',
                    'Type': 'string'
                },
                {
                    'Name': 'Created_at',
                    'Type': 'timestamp'
                }
            ],
            'Location': location,
            'InputFormat': table_input_format,
            'OutputFormat': table_output_format,
            'SerdeInfo': {
                'Name': 'EcommerceSerde',
                'SerializationLibrary': serde_library
            }
        },
        'TableType': 'EXTERNAL_TABLE',
        'Parameters': {
            'classification': 'parquet',
            'typeOfData': 'file'
        }
    }
)

if 'Table' in response:
    print(f"Table '{table_name}' created successfully in database '{database_name}'.")
else:
    print(f"Failed to create table '{table_name}' in database '{database_name}'.")
