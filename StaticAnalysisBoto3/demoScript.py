import boto3


clientLambda = boto3.client('lambda')
s3 = boto3.client('s3')

def doSomething():
    b = 1+1
    return True

def doAnotherthing():
    c = 1+1
    return True


def createS3Bucket():
    s3.create_bucket(Bucket='zachbucket222')
    s3.delete_bucket(Bucket='zachbucket222')

def listBuckets():
    return s3.list_buckets()



response = clientLambda.get_function( 
    FunctionName='arn:aws:lambda:us-east-1:221094580673:function:testFunction',
)

response = clientLambda.get_function(
    FunctionName='testFunction',
)
