from datetime import datetime
import boto3


def getAllS3() -> dict:
    
    s3 = boto3.client("s3")

    response = s3.list_buckets()
    
    return response


def getLastModified(bucketName: str) -> datetime:

    ## If last modified time is too long ago, move s3 bucket data into a glacier?

    buckets = getAllS3()

    for bucket in buckets:
        if(bucket["Name"] == bucketName):
            objects = list(bucket.objects.all())
            return max(obj.last_modified for obj in objects)


def getLastAccess(bucketName: str) -> datetime:
    #To get last access time of a s3 bucket logging needs to be avaliable for that bucket

    return None
            






