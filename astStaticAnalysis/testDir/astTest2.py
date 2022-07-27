import boto3

s3 = boto3.client('s3')



def listBuckets():
    response = s3.list_buckets()
    return response