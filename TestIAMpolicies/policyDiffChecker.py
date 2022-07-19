import jsondiff as jd
from jsondiff import diff
import json
import jsondiff
import parliament
import os
import pandas as pd
import subprocess
import shlex

#From the policies, map it to the functions and list out what they can do

json_files = [pos_json for pos_json in os.listdir() if pos_json.endswith('.json')]

response = {'Policies': []}

for jsonfile_name in json_files:
    response['Policies'].append(jsonfile_name)
    file = open(jsonfile_name)
    jsonfile = json.load(file)
    jsonobj = json.dumps(jsonfile)
    policyobj = parliament.analyze_policy_string(jsonobj)
    shellresponse = subprocess.getoutput('parliament --file {}'.format(shlex.quote(jsonfile_name)))
    print(shellresponse)
    if 'Unknown' not in shellresponse:
        policy_actions= policyobj.get_allowed_actions()
        print('policy actions for file :')
        for y in policy_actions:
            print(y)

print(response)
print("hello")