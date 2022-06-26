'''
This will be the test script to be passed into analyseBoto3Script.py to 
extract the information we need
'''
#import neccessary modules
import logging
import boto3
from botocore.exceptions import ClientError
import os

# Set a global variable for s3
s3 = boto3.client('s3')



def createBucket(bucketName, region=None):
    #create new bucket
    newBucket=s3.create_bucket(Bucket=bucketName)
    #list all buckets to check if creation was successful
    response = s3.list_buckets()
    #iterate through list to check if bucket exists
    for bucket in response['Buckets']:
        if(bucket["Name"] ==bucketName):
            print("Successfully created s3 bucket")
            break


def createBucket2(bucketName):
    #create new bucket
    newBucket=s3.create_bucket(Bucket=bucketName)
    #list all buckets to check if creation was successful
    response = s3.list_buckets()
    #iterate through list to check if bucket exists
    for bucket in response['Buckets']:
        if(bucket["Name"] ==bucketName):
            print("Successfully created s3 bucket")
            break

def deleteBucket(bucketName):
    s3.delete_bucket(Bucket=bucketName)
    # check if deletion was successful
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        if(bucket["Name"]==bucketName):
            print("Error bucket not deleted")
            quit()
    print("Deletion successful")


# Function that allows file uploads to s3 bucket
def uploadToBucket(file_name, bucket, object_name=None):
    """
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    # Upload the file
    try:
        response = s3.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    print('Successfully uploaded'+file_name+'to'+bucket)
    return True



if(True):
    clientLambda = boto3.client('lambda')
    clientS3 = boto3.client('s3')



# At the same time we want to extract the functions used by the script for example, calling a cloudtrail function
# createBucket('zachbooket','None')
# deleteBucket('zachbooket')

# createBucket('zachbooket123')
# deleteBucket('zachbooket123')

# createBucket2('toosting')
# deleteBucket('toosting')



# s3.create_bucket(Bucket='zachbucket222')
# s3.delete_bucket(Bucket='zachbucket222')

# s3.create_bucket(Bucket='zachbucket2388742')
# s3.delete_bucket(Bucket='zachbucket2388742')
'''
create a function that extracts the name of the arn function from the method, i only have the line number, need the arn function name
create a function that gets the user defined function and translates it to the arn function name
'''


def doSomething():
    response = clientLambda.get_function( 
        FunctionName='arn:aws:lambda:us-east-1:221094580673:function:AnotherTestFunction',
    )

    response = clientLambda.list_functions(
        FunctionVersion='ALL',
        MaxItems=123
    )



response = clientLambda.get_function( 
    FunctionName='arn:aws:lambda:us-east-1:221094580673:function:testFunction2',
)

# print(response)
response = clientLambda.get_function(
    FunctionName='testFunction',
)

response = clientLambda.get_function( 
    FunctionName='arn:aws:lambda:us-east-1:221094580673:function:testFunction',
)

# print(response)