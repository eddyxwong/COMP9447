import boto3



s3 = boto3.client("s3")
response = s3.list_buckets()

# Output the bucket names
print("Existing buckets:")
for bucket in response['Buckets']:
    print(f'{bucket["Name"]}')


s3.create_bucket(Bucket='franksu-9447-testbucket')


response = s3.list_buckets()

# print(response)

for bucket in response['Buckets']:
    if(bucket["Name"] =='franksu-9447-testbucket'):
        print("Successfully created s3 bucket")

s3.delete_bucket(Bucket='franksu-9447-testbucket')


response = s3.list_buckets()

for bucket in response['Buckets']:
    if(bucket["Name"] =='franksu-9447-testbucket'):
        print("Error bucket not deleted")
        quit()

print("Bucket deleted successfully")






