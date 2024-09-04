#!/bin/bash
  
# Load configuration variables from lambda_config.json
config_file="aws_infrastructure/cli_scripts/config/lambda_config.json"

if [ -f $config_file ]; then
  source $config_file
else
  echo "Error: lambda_config.json not found. Make sure the file exists and is correctly configured."
  exit 1
fi

# Python file name (without extension)
python_file="lambda_function"

# Resulting ZIP file name
zip_file="$python_file.zip"

# Directory path where the ZIP file will be stored
output_dir="./"

# Lambda execution role ARN (from lambda_config.json)
lambda_execution_role_arn=$lambda_execution_role_arn

# Data Stream ARN (from lambda_config.json)
data_stream_arn=$data_stream_arn

# Compress the Python file into a ZIP
zip -j $output_dir$zip_file $python_file.py

# Create the Lambda function
aws lambda create-function \
  --function-name $function_name \
  --runtime python3.8 \
  --handler $python_file.lambda_handler \
  --role $lambda_execution_role_arn \
  --zip-file fileb://$output_dir$zip_file

# Configure the Data Stream trigger
aws lambda create-event-source-mapping \
  --function-name $function_name \
  --event-source-arn $data_stream_arn \
  --batch-size 10 \
  --starting-position LATEST

# Load environment variables from the JSON file
source $config_file

# Configure Lambda environment variables
aws lambda update-function-configuration \
  --function-name $function_name \
  --environment "Variables={cloudwatch_namespace=$cloudwatch_namespace,cloudwatch_metric=$cloudwatch_metric,topic_arn=$topic_arn}"

echo "Lambda function created and configured successfully."
