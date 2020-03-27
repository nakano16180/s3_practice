from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

endpoint = '127.0.0.1:9000'
ACCESS_KEY = 'minioadmin'
SECRET_KEY = 'minioadmin'

minioClient = Minio(endpoint,
                  access_key=ACCESS_KEY,
                  secret_key=SECRET_KEY,
                  secure=False)

buckets = minioClient.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)
print("-------------------------")

# Make a bucket with the make_bucket API call.
try:
    if not minioClient.bucket_exists("mybucket"):
        minioClient.make_bucket("mybucket", location="us-east-1")
    
    minioClient.remove_all_bucket_notification('mybucket')
    notification = minioClient.get_bucket_notification('mybucket')
    print(notification)

    notification = {
        'QueueConfigurations': [
            {
                'Id': '1',
                'Arn': 'arn1',
                'Events': ['s3:ObjectCreated:*'],
                'Filter': {
                    'Key': {
                        'FilterRules': [
                            {
                                'Name': 'suffix',
                                'Value': '.mp4'
                            }
                        ]
                    }
                }
            }
        ]
    }
    minioClient.set_bucket_notification('mybucket', notification)

except BucketAlreadyOwnedByYou as err:
    pass
except BucketAlreadyExists as err:
    pass
except ResponseError as err:
    raise