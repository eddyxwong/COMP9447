import boto3
if(True):
    clientLambda = boto3.client('lambda')

    clientS3 = boto3.client('s3')


response = clientLambda.list_functions(
    FunctionVersion='ALL',
    MaxItems=123
)





print(response["Functions"])

temp = {"yo": 1, "ho": 2}


print(temp["yo"])


for key in temp:
    print(key)