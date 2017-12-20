import boto3
import re
import os

def lambda_handler(event, context):
    
    # Pull relevant env
    tag_key = os.environ['tag_key']
    db = os.environ['athena_db']
    table = os.environ['athena_table']
    bucket = os.environ['output_bucket']
    
    # Get year and month
    key = event['Records'][0]['s3']['object']['key']
    date_match = re.match(r'^year=(\d{4})/month=(\d{1,2})/.*\.csv$', key)
    if not date_match:
        print('Error: Invalid Athena partition key: {}'.format(key))
        return False
    year, month = date_match.groups()

    # Init boto clients 
    athena = boto3.client('athena')
    
    # Build query
    query = "SELECT DISTINCT resourcetags_user_{tag_key} FROM {table} WHERE resourcetags_user_{tag_key} != '';".format(**locals())
    
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': db,},
        ResultConfiguration={'OutputLocation': 's3://{bucket}/tags/{year}/{month}'.format(**locals()),}
    )
    
    return True
