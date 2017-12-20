import boto3
import os

def lambda_handler(event, context):

    # Pull relevant env
    tag_key = os.environ['tag_key']
    db = os.environ['athena_db']
    table = os.environ['athena_table']
    
    # Get info from event
    key = event['Records'][0]['s3']['object']['key']
    print(key)
    year, month, tag_value = key.split('/')[1:4]
    bucket = event['Records'][0]['s3']['bucket']['name']
    
    # Init boto clients
    s3 = boto3.client('s3')
    
    # Move file
    s3.copy_object(
        Bucket=bucket,
        CopySource='{bucket}/{key}'.format(**locals()),
        Key='reports/{tag_value}/{year}-{month}-cur.csv'.format(**locals())
    )

    return True
