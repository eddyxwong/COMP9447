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

    inputCheck(argv)

    directory = argv[1].strip(".\\")

    json_files = folderWalker(directory)

    shellresponse = subprocess.getoutput('parliament --directory {}'.format(shlex.quote(directory))).split('\n')

    response = diffCheck(shellresponse, json_files)

    print(json.dumps(response, sort_keys=False, indent=4))

    return json.dumps(response, sort_keys=False, indent=4)




"""Given a list of commandline arguments, checks for any input error and informs the user if any are found

    Args:
        argument(list): a list of command line arguments

    Returns:
        (str): string of error message
"""
def inputCheck(argument: list) -> str:
    if len(argument) > 2 or len(argument) < 2:
        print("Incorrect input, too many/too little arguments provided.\nPlease follow the format:\n'python policyDiffchecker.py directory_name'")
        exit()


"""Given a directory, traverses it and finds the relative path to all .json files before appending to a list

    Args:
        directory(str): a string of directory name

    Returns:
        json_files(list): list of .json files inside said directory
"""
def folderWalker(directory: str) -> list:
    json_files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(directory):
        for file in f:
            if file.endswith(".json"):
                json_files.append(str(os.path.relpath(os.path.join(r, file)).replace(os.path.sep, '/')))
    return json_files
    

"""Given a empty dictionary and list of json_files found, create the template for 
    findings to be added.

    Args:
        dictionary (dict): An empty dictionary containing a empty list,
        json_files (list): List of json files found inside the directory

    Returns:
        dictionary(dict): list of .json files inside said directory
"""
def directInit(dictionary: dict, json_files: list) -> dict:
    for jsonfile_name in json_files:
        dictionary['Policies'].append({
            'Policy Name': jsonfile_name,
            'Findings': [],
            'Differences': {}
        })
    
    return dictionary


"""
    Given a previously created base template for displaying IAM policies, add the corresponding findings to
    the template.

    Args:
        shellresponse (list): Findings for all json files within the directory specified by the user based on 
        the tool, parliament.
        template (dict): Base template to display all findings and differences.
        json_files (list): List of json files found inside the directory specified by the user.

    Returns:
        template(dict): Template that has been filled with findings and differences between policies
"""
def diffCheck(shellresponse: list, json_files: list) -> dict:
    template = {'Policies': []}

    for jsonfile_name in json_files:
        template['Policies'].append({
            'Policy Name': jsonfile_name,
            'Findings': [],
            'Differences': {}
        })



    for dict in template['Policies']:

        jsonfile_name = dict['Policy Name']

        appendFindings(shellresponse, dict, jsonfile_name)

        appendDifferences(dict, json_files, jsonfile_name)
       
    return template


def appendFindings(shellresponse: list, dictionary: dict, jsonfile_name: str):
    for pathing in shellresponse:
        reformed_findings = str(pathing.replace(r'\\', '/'))
        if jsonfile_name in reformed_findings:
            dictionary['Findings'].append(reformed_findings)

    if len(dictionary['Findings']) == 0:
            dictionary['Findings'].append('No faults found within policy')

def appendDifferences(dictionary: dict, json_files: list, jsonfile_name: str):
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
                dictionary['Differences'].update({"Contents found in "+filename1+" but not in "+filename2: []})
                for diffLine in file1contents - file2contents:
                    diffLine = (diffLine).replace(" ", "").replace('\n','').replace(',','').replace('}', '').replace('"', '')
                    if diffLine != '':
                        dictionary['Differences']["Contents found in "+filename1+" but not in "+filename2].append(str(diffLine))


if __name__ == "__main__":
    main(sys.argv)
