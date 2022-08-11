import json
import os
import sys
import subprocess
import shlex

'''
IAM Policy Comparison Program, find all json files in a given directory and compare them based on findings 
from a third-party tool (parliament) and differences in their contents

Args:
        directory (str): a string of directory name

    Returns:
        dictionary(differences): Dictionary of findings and differences in content for policys

'''


def main(argv):
    if len(argv) > 2:
        print("Too many arguments, please input only one directory name")
        exit()  
    directory = argv[1].strip(".\\")

    json_files = folderWalker(directory)

    response = {'Policies': []}
    response = directInit(response, json_files)

    shellresponse = subprocess.getoutput('parliament --directory {}'.format(shlex.quote(directory))).split('\n')

    response = diffcheck(shellresponse, response, json_files)

    print(json.dumps(response, sort_keys=False, indent=4))

    return json.dumps(response, sort_keys=False, indent=4)

def folderWalker(directory: str) -> list:
    """Given a directory, traverses it and finds the relative path to all .json files before appending to a list

    Args:
        directory(str): a string of directory name

    Returns:
        json_files(list): list of .json files inside said directory
    """
    json_files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(directory):
        for file in f:
                if file.endswith(".json"):
                    abspath = os.path.join(r, file)
                    json_files.append(str(os.path.relpath(abspath).replace(os.path.sep, '/')))
    return json_files
    
def directInit(dictionary: dict, json_files: list) -> dict:
    """Given a empty dictionary and list of json_files found, create the template for 
    findings to be added.

    Args:
        dictionary (dict): An empty dictionary containing a empty list,
        json_files (list): List of json files found inside the directory

    Returns:
        dictionary(dict): list of .json files inside said directory
    """
    for jsonfile_name in json_files:
        dictionary['Policies'].append({
            'Policy Name': jsonfile_name,
            'Findings': [],
            'Differences': {}
        })
    
    return dictionary

def diffcheck(shellresponse: list, response: dict, json_files: list) -> dict:
    for dict in response['Policies']:
        jsonfile_name = dict['Policy Name']
        for x in shellresponse:
            reformed = x.replace(r'\\', '/')
            if jsonfile_name in reformed:
                dict['Findings'].append(str(reformed))
        if len(dict['Findings']) == 0:
            dict['Findings'].append('No faults found within policy')
        if len(json_files) > 1:
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
                        diffLine = (diffLine).replace(" ", "").replace('\n','').replace(',','').replace('}', '').replace('"', '')
                        if diffLine != '':
                            dict['Differences']["Contents found in "+filename1+" but not in "+filename2].append(str(diffLine))
    return response


if __name__ == "__main__":
    main(sys.argv)
