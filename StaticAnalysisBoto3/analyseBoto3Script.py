
import json
from typing import Dict


def analysePythonScript(filepath: str) -> json:

    respDict = getUsedServices(filepath)  

    newPolicy = {"Version": "2012-10-17",
                "Statement": [] }


    newStatement = createAllowStatement()

    for service in respDict:
        if("service" == "lambda"):
            for method in respDict[service]:
                newAction = createAction(service, method)
                newStatement["Action"].append(newAction)

    return newPolicy


def createAllowStatement() ->json:
    newStatement = {"Effect": "Allow",
                    "Action": [],
                    "Resource": "*"}
    
    return newStatement


def createAction(service: str, method: str) -> str:
    return "\""+ service+":"+method + "\""




'''
{"s3": [list_buckets], 
"cloudtrail": [list_event_data_stores, list_trails]}


'''
def getUsedServices(filepath: str) -> Dict[str, str]:
    file = open(filepath, 'r')
    # for line in file:






    




