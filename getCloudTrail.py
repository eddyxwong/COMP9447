import boto3
from datetime import datetime
#specify cloudtrail client
client = boto3.client('cloudtrail')

#List all event stores in the current region for this account
def list_event_stores():
    response = client.list_event_data_stores(
    NextToken='string',
    MaxResults=500
    )
    print(response)

#List all trails in the current region for this account
def list_trails():
    response = client.list_trails(
    NextToken='string'
    )
    print(response)

#Get specific trail 
def get_trail(trail_name):
    response = client.get_trail(
    Name=trail_name
    )
    print(response)

def delete_trail(name):
    response = client.delete_trail(
        Name=name
    )
    print("success")


# to do
# Create Trail


# Delete Trail
# Create event data store
# delete data store
list_event_stores()
list_trails()
get_trail('frankTest')