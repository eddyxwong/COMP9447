import boto3


clientLambda = boto3.client('lambda')
s3 = boto3.client('s3')

def doSomething():
    response = clientLambda.get_function( 
            FunctionName='arn:aws:lambda:us-east-1:221094580673:function:testFunction',
    )

    print(response)

def listBuckets():
    response = s3.list_buckets()
    return response

response = s3.create_bucket(Bucket='zachbucket222')

response = s3.delete_bucket(Bucket='zachbucket222')

response = clientLambda.list_functions()