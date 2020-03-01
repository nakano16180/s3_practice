from __future__ import print_function

import os
import json
import urllib
import boto3
import pprint

print('Loading function')

print('AWS_ACCESS_KEY_ID: ', os.environ.get('AWS_ACCESS_KEY_ID'))
print('AWS_SECRET_ACCESS_KEY: ', os.environ.get('AWS_SECRET_ACCESS_KEY'))
#print('AWS_S3_ENDPOINT_URL: ', os.environ.get('AWS_S3_ENDPOINT_URL'))
#s3_endpoint_url = os.environ.get('AWS_S3_ENDPOINT_URL')

#s3_endpoint_url = 'http://minio:9000'
#http://boto3.readthedocs.io/en/latest/reference/services/s3.html#client
#s3 = boto3.client('s3', endpoint_url=s3_endpoint_url)


def lambda_handler(event, context):

    pprint.pprint(event)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    print('==== bucket information =====')
    print(bucket_name)
    print('=============================')

    print('==== uploaded file ====')
    for rec in event['Records']:
        print(rec['s3']['object']['key'])
    print('=============================')

    print("Received event: " + json.dumps(event, indent=2))

