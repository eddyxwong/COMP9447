import json
import parliament
import os
import subprocess
import shlex

json_files = []

# Getting the current work directory (cwd)
thisdir = os.getcwd()
# r=root, d=directories, f = files
for r, d, f in os.walk(thisdir):
    for file in f:
        if file.endswith(".json"):
            abspath = os.path.join(r, file)
            json_files.append(str(os.path.relpath(abspath).replace(os.path.sep, '/')))

#From the policies, map it to the functions and list out what they can do
response = {'Policies': []}

for jsonfile_name in json_files:
    shellresponse = subprocess.getoutput('parliament --file {}'.format(shlex.quote(jsonfile_name)))
    if 'Unknown' not in shellresponse:
        response['Policies'].append({
            'Policy Name': jsonfile_name,
            'Allowed Actions': [],
            'Findings': ''
        })
    elif 'Unknown' in shellresponse:
        print('Erorr: Json file ' +jsonfile_name+ ' is not a IAM policy file\nExiting...')
        exit()

for dict in response['Policies']:
    jsonfile_name = dict['Policy Name']
    file = open(jsonfile_name)
    print(jsonfile_name)
    print(type(file))
    jsonfile = json.load(file)
    jsonobj = json.dumps(jsonfile)
    policyobj = parliament.analyze_policy_string(jsonobj)
    shellresponse = subprocess.getoutput('parliament --file {}'.format(shlex.quote(jsonfile_name)))
    policy_actions= policyobj.get_allowed_actions()
    for action in policy_actions:
        dict['Allowed Actions'].append(action)
    dict['Findings'] = list(shellresponse.split("\n"))

print(json.dumps(response, sort_keys=False, indent=4))
