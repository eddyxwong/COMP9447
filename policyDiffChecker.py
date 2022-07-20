import json
import parliament
import os
import subprocess
import pkg_resources
import shlex

# Grab a txt file of json files found
# Take json files and run parliament in github actions
# Take parliament output and put that inside the dictionary


iam_definition_path = pkg_resources.resource_filename(__name__, "iam_definition.json")
iam_definition = json.load(open(iam_definition_path, "r"))


# Helper Function To Get Priviledge info
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
for r, d, f in os.walk('TestIAMpolicies'):
    for file in f:
        if file.endswith(".json"):
            abspath = os.path.join(r, file)
            json_files.append(str(os.path.relpath(abspath).replace(os.path.sep, '/')))

#From the policies, map it to the functions and list out what they can do
response = {'Policies': []}

shellresponse = subprocess.getoutput('parliament --directory {}'.format(shlex.quote('TestIAMpolicies'))).split('\n')

for jsonfile_name in json_files:
    response['Policies'].append({
        'Policy Name': jsonfile_name,
        'Findings': [],
        'Differences': {}
    })

for dict in response['Policies']:
    jsonfile_name = dict['Policy Name']
    file = open(jsonfile_name)
    jsonfile = json.load(file)
    jsonobj = json.dumps(jsonfile)
    policyobj = parliament.analyze_policy_string(jsonobj)
    policy_actions= policyobj.get_allowed_actions()
    for x in shellresponse:
        reformed = x.replace(r'\\', '/')
        if jsonfile_name in reformed:
            dict['Findings'].append(str(reformed))
    for jsonfile_name2 in json_files:
        filename1 = jsonfile_name
        filename2 = jsonfile_name2
        if filename1 == filename2:
            continue
        file1contents = set(open(filename1).readlines())
        file2contents = set(open(filename2).readlines())
        if file1contents == file2contents:
            print("Yup they're the same!")
        else:
            dict['Differences'].update({"Contents found in "+filename1+" but not in "+filename2: []})
            for diffLine in file1contents - file2contents:
                dict['Differences']["Contents found in "+filename1+" but not in "+filename2].append(" ".join(str(diffLine).split()))
print(json.dumps(response, sort_keys=False, indent=4))