from aws_kinesis_agg.deaggregator import iter_deaggregate_records
import base64 
import json
import boto3 
import os 
 
# OS input variables:
cloudwatch_namespace = os.environ['cloudwatch_namespace']
cloudwatch_metric = os.environ['cloudwatch_metric']
topic_arn = os.environ['topic_arn']

# AWS Services
cloudwatch = boto3.client('cloudwatch', region_name='eu-west-1')
sns = boto3.client('sns', region_name='eu-west-1')

def extract_dimensions(json_document):
    # Extract data from the JSON payload and build dimensions dynamically
    dimensions = []
    for key, value in json_document.items():
        dimensions.append({'Name': key, 'Value': str(value)})
    return dimensions

def lambda_handler(event, context):
    raw_kinesis_records = event['Records']
    record_count = 0

    # Deaggregate all records using a generator function
    for record in iter_deaggregate_records(raw_kinesis_records):

        try:
            # Kinesis data in Python Lambdas is base64 encoded
            payload = base64.b64decode(record['kinesis']['data'])
            json_document = json.loads(payload.decode('utf-8'))

            # Extract dimensions dynamically from the JSON payload
            dimensions = extract_dimensions(json_document)

            # Push metrics to CloudWatch for 'SalesByProduct'
            if json_document.get('EventType') == 'SalesByProduct':
                cloudwatch_response = cloudwatch.put_metric_data(
                    MetricData=[
                        {
                            'MetricName': 'TotalSalesByProduct',
                            'Dimensions': dimensions,
                            'Unit': 'Count',
                            'Value': 1,
                            'StorageResolution': 1
                        },
                    ],
                    Namespace=cloudwatch_namespace
                )

            # Send SNS for 'ConversionRate'
            elif json_document.get('EventType') == 'ConversionRate':
                conversion_rate = json_document.get('ConversionRate', 0)
                if conversion_rate < 0.10:
                    sns.publish(TopicArn=topic_arn, Message="Alert! Conversion Rate less than 10%: {}".format(conversion_rate),
                                Subject="Conversion Rate Alert")
                    print('Email notification sent due to low conversion rate')

            # Print CloudWatch response:
            print(cloudwatch_response)

        except Exception as e:
            print('Error when processing stream:')
            print(e)

        # Print response and increment counter
        record_count += 1

    return 'Successfully processed {} records.'.format(record_count)
