import boto3
import os

def lambda_handler(event, context):
    
    # Pull relevant env
    tag_key = os.environ['tag_key']
    db = os.environ['athena_db']
    table = os.environ['athena_table']
    
    # Get info from event
    key = event['Records'][0]['s3']['object']['key']
    year, month = key.split('/')[1:3]
    bucket = event['Records'][0]['s3']['bucket']['name']
    
    # Init boto clients
    athena = boto3.client('athena')
    s3 = boto3.resource('s3')
    
    # Read tags out of S3
    obj = s3.Object(bucket, key)
    raw_tag_list = obj.get()['Body'].read().decode('utf-8')
    tag_list = [t.strip('"') for t in raw_tag_list.split()[1:]]
    
    # Query for each tag and month
    for tag_value in tag_list:
        
        # Build query
        query = "SELECT * FROM {table} WHERE resourcetags_user_{tag_key}='{tag_value}' AND year='{year}' AND month='{month}';".format(**locals())

        # Query athena
        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': db,},
            ResultConfiguration={'OutputLocation': 's3://{bucket}/athena_out/{year}/{month}/{tag_value}'.format(**locals()),}
        )
    
    return True
