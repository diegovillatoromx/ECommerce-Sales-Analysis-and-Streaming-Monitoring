#!/bin/bash

# Lambda function name
function_name="YourLambdaFunctionName"

# Python file name (without extension)
python_file="lambda_function"

# Resulting ZIP file name
zip_file="$python_file.zip"

# Path to the configuration JSON file
config_file="aws_infrastructure/cli_scripts/config/lambda_config.json"

# Path to the Python file
python_code="$python_file.py"

# Directory path where the ZIP file will be stored
output_dir="./"

# Compress the Python file into a ZIP
zip -j $output_dir$zip_file $python_code

# Create the Lambda function
aws lambda create-function \
  --function-name $function_name \
  --runtime python3.8 \
  --handler $python_file.lambda_handler \
  --role YourLambdaExecutionRoleARN \
  --zip-file fileb://$output_dir$zip_file

# Configure the Data Stream trigger
aws lambda create-event-source-mapping \
  --function-name $function_name \
  --event-source-arn arn:aws:kinesis:us-east-1:YOUR_ACCOUNT_ID:stream/data_stream_pipeline_processing_useast1 \
  --batch-size 10 \
  --starting-position LATEST

# Load environment variables from the JSON file
source $config_file

# Configure Lambda environment variables
aws lambda update-function-configuration \
  --function-name $function_name \
  --environment "Variables={cloudwatch_namespace=$cloudwatch_namespace,cloudwatch_metric=$cloudwatch_metric,topic_arn=$topic_arn}"

echo "Lambda function created and configured successfully."
