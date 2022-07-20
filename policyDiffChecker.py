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
    text = subprocess.run(['parliament' ,'--file',jsonfile_name], text=True)
    g = text.stdout
    print(g)