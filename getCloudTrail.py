import boto3

#specify cloudtrail client
client = boto3.client('cloudtrail')

def list_event_stores():
    response = client.list_event_data_stores(
    NextToken='string',
    MaxResults=500
    )
    print(response)

def list_trails():
    response = client.list_trails(
    NextToken='string'
    )
    print(response)

def get_trail(trail_name):
    response = client.get_trail(
    Name=trail_name
    )
    print(response)

list_event_stores()
list_trails()
get_trail('frankTest')