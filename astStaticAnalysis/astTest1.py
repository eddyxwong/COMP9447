import boto3


clientLambda = boto3.client('lambda')

def doSomething():
    response = clientLambda.get_function( 
            FunctionName='arn:aws:lambda:us-east-1:221094580673:function:testFunction',
    )

    print(response)