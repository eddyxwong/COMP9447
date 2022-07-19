import json
import parliament
import os
import subprocess
import shlex
import pkg_resources


iam_definition_path = pkg_resources.resource_filename(__name__, "iam_definition.json")
iam_definition = json.load(open(iam_definition_path, "r"))


def get_privilege_info(service, action):
    """
    Given a service, like "s3"
    and an action, like "ListBucket"
    return the info from the docs about that action, along with some of the info from the docs
    """
    for service_info in iam_definition:
        if service_info["prefix"] == service:
            for privilege_info in service_info["privileges"]:
                if privilege_info["privilege"] == action:
                    privilege_info["service_resources"] = service_info["resources"]
                    privilege_info["service_conditions"] = service_info["conditions"]
                    return privilege_info



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
    jsonfile = json.load(file)
    jsonobj = json.dumps(jsonfile)
    policyobj = parliament.analyze_policy_string(jsonobj)
    shellresponse = subprocess.getoutput('parliament --file {}'.format(shlex.quote(jsonfile_name)))
    policy_actions= policyobj.get_allowed_actions()
    for action in policy_actions:
        actiondict = parliament.expand_action(action)[0]
        info = get_privilege_info(actiondict['service'], actiondict['action'])
        dict['Allowed Actions'].append("Action: "+ action)
        dict['Allowed Actions'].append("Service Info: "+ info['description'])
    print(shellresponse)
    dict['Findings'] = list(shellresponse.split("\n"))

print(json.dumps(response, sort_keys=False, indent=4))
