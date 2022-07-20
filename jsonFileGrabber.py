import os
import parliament
import json

json_files = []

# Getting the current work directory (cwd)
thisdir = os.getcwd()
# r=root, d=directories, f = files
for r, d, f in os.walk(thisdir):
    for file in f:
        if file.endswith(".json"):
            abspath = os.path.join(r, file)
            json_files.append(str(os.path.relpath(abspath).replace(os.path.sep, '/')))


for jsonfile_name in json_files:
    file = open(jsonfile_name)
    jsonfile = json.load(file)
    jsonobj = json.dumps(jsonfile)
    policyobj = parliament.analyze_policy_string(jsonobj)
    policyobj.analyze
    if 'MALFORMED_JSON' in policyobj.finding_ids:
        json_files.remove(jsonfile_name)

for jsonfile_name in json_files:
    print(jsonfile_name)
