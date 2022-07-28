import json
import parliament
import os
import subprocess
import shlex

# Grab a txt file of json files found
# Take json files and run parliament in github actions
# Take parliament output and put that inside the dictionary
# Make the pyton program take in the directory and scan it 

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

# include reasoning why this is here
shellresponse = subprocess.getoutput('parliament --directory {}'.format(shlex.quote('TestIAMpolicies'))).split('\n')

for jsonfile_name in json_files:
    response['Policies'].append({
        'Policy Name': jsonfile_name,
        'Findings': [],
        'Differences': {}
    })

for dict in response['Policies']:
    jsonfile_name = dict['Policy Name']
    for x in shellresponse:
        reformed = x.replace(r'\\', '/')
        if jsonfile_name in reformed:
            dict['Findings'].append(str(reformed))
    if len(dict['Findings']) == 0:
        dict['Findings'].append('No faults found within policy')
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