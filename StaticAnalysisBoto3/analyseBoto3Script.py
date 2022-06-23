
import json
from typing import Dict, List


def analyseScript(filepath: str) -> json:
    getUsedServices(filepath)  




'''
{"s3": [list_buckets], 
"cloudtrail": [list_event_data_stores, list_trails]}


'''
def getUsedServices(filepath: str) -> Dict[str]:
    file = open(filepath, 'r')

    # for line in file:





    




