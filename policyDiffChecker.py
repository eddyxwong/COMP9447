import json
import parliament
import os
import sys
import subprocess
import shlex

# Grab a txt file of json files found
# Take json files and run parliament in github actions
# Take parliament output and put that inside the dictionary
# Make the pyton program take in the directory and scan it 


def main(argv):
    directory = argv[1]
    print(directory)

    json_files = []

    json_files = folderWalker(directory, json_files)

    #From the policies, map it to the functions and list out what they can do
    response = {'Policies': []}

    # include reasoning why this is here
    shellresponse = subprocess.getoutput('parliament --directory {}'.format(shlex.quote(directory))).split('\n')

    response = directInit(response, json_files)

    response = diffcheck(shellresponse,response,json_files)

    print(json.dumps(response, sort_keys=False, indent=4))



def folderWalker(directory: str, jsonList: list) -> list:

    # r=root, d=directories, f = files
    for r, d, f in os.walk(directory):
        for file in f:
            if file.endswith(".json"):
                abspath = os.path.join(r, file)
                jsonList.append(str(os.path.relpath(abspath).replace(os.path.sep, '/')))
    
    return jsonList
    
def directInit(response: dict, json_files: list) -> dict:
    for jsonfile_name in json_files:
        response['Policies'].append({
            'Policy Name': jsonfile_name,
            'Findings': [],
            'Differences': {}
        })
    
    return response

def diffcheck(shellresponse: list, response: dict, json_files: list) -> dict:
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
    return response

if __name__ == "__main__":
    main(sys.argv)


