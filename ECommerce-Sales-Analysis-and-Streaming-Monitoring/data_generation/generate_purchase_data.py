import json  
import boto3    
from purchase_data_generation import generate_purchase_data

stream_name = 'YOUR_DATA_STREAM_NAME'  
region = 'us-east-1'
KinesisClient = boto3.client('kinesis', region_name=region) 

# Generate purchase data
purchase_data = generate_purchase_data(1000)  # Generate 100 purchase records
 
for purchase in purchase_data:
    record_value = json.dumps(purchase).encode('utf-8')
    records = KinesisClient.put_record(StreamName=stream_name, Data=record_value, PartitionKey='USER_ID')
    print("Total data ingested:" + str(x) + ",ReqID:" + records['ResponseMetadata']['RequestId'] + ",HTTPStatusCode:" + str(records['ResponseMetadata']['HTTPStatusCode']))
