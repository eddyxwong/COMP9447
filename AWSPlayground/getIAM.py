from http.client import ResponseNotReady
import boto3

iam = boto3.client("iam")

response = iam.list_policies(
    Scope = 'Local' # 'AWS'|'Local'|'All'
)


for policy in response['Policies']:
    print(policy['PolicyName'])




# print(response)