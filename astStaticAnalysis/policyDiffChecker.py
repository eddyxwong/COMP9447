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
        response (dict): Dictionary of findings and differences in content for policys

'''
def main(dir):

    # inputCheck(argv)

    directory = dir[1].strip(".\\")

    directory = dir
    json_files = folderWalker(dir)

    shellresponse = subprocess.getoutput('parliament --directory {}'.format(shlex.quote(directory))).split('\n')

    response = diffCheck(shellresponse, json_files)

    print(json.dumps(response, sort_keys=False, indent=4))

    return json.dumps(response, sort_keys=False, indent=4)



"""Given a list of commandline arguments, checks for any input error and informs the user if any are found

    Args:
        argument (list): a list of command line arguments

    Returns:
        NA
"""
def inputCheck(argument: list):
    if len(argument) > 2 or len(argument) < 2:
        print("Incorrect input, too many/too little arguments provided.\nPlease follow the format:\n'python policyDiffchecker.py directory_name'")
        exit()


"""Given a directory, traverses it and finds the relative path to all .json files before appending to a list

    Args:
        directory (str): a string of directory name

    Returns:
        json_files (list): list of .json files inside said directory
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
        dictionary (dict): list of .json files inside said directory
"""
def directInit(dictionary: dict, json_files: list) -> dict:
    for jsonfile_name in json_files:
        dictionary['Policies'].append({
            'Policy Name': jsonfile_name,
            'Findings': [],
            'Differences': {}
        })
    
    return dictionary


"""Given a previously created base template for displaying IAM policies, add the corresponding findings to
    a base template to display differences found.

    Args:
        shellresponse (list): Findings for all json files within the directory specified by the user based on the tool, Parliament.
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

    for jsonDict in template['Policies']:

        jsonfile_name = jsonDict['Policy Name']

        jsonDict = appendFindings(shellresponse, jsonDict, jsonfile_name)

        jsonDict = appendDifferences(json_files, jsonDict, jsonfile_name)
       
    return template


"""Appends findings by Parliment to the correct position in the dictionary given.

    Args:
        shellresponse (list): Findings for all json files within the directory specified by the user based on the tool, Parliament.
        dictionary (dict): Dictionary for each json file within the template.
        jsonfile_name (str): a string of a json file name.

    Returns:
        dictionary (dict): Filled dictionary of findings found for the particular json file.
"""
def appendFindings(shellresponse: list, dictionary: dict, jsonfile_name: str) -> dict:
    for pathing in shellresponse:
        reformed_findings = str(pathing.replace(r'\\', '/'))
        if jsonfile_name in reformed_findings:
            dictionary['Findings'].append(reformed_findings)

    if len(dictionary['Findings']) == 0:
            dictionary['Findings'].append('No faults found within policy')

    return dictionary


"""Appends differences in contents of IAM policy json files to the correct position in the dictionary given.

    Args:
        json_files (list): List of all json files previously found in the directory.
        dictionary (dict): Dictionary for each json file within the template.
        jsonfile_name (str): a string of a json file name.

    Returns:
        dictionary (dict): Filled dictionary of differences found for the json files in the directory.
"""
def appendDifferences(json_files: list, dictionary: dict, jsonfile_name: str) -> dict:
    if len(json_files) <= 1:
        return dictionary

    # Run through list to compare while ignoring the json_filename
    for jsonNameCrawl in json_files:
        if jsonfile_name == jsonNameCrawl:
            continue

        filename1 = jsonfile_name
        filename2 = jsonNameCrawl

        # Create sets from both file contents
        file1contents = set(open(filename1).readlines())
        file2contents = set(open(filename2).readlines())

        # Check for differences
        if file1contents == file2contents:
            print("Yup they're the same!")
        else:
            dictionary['Differences'].update({"Contents found in "+filename1+" but not in "+filename2: []})
            for diffLine in file1contents - file2contents:
                diffLine = (diffLine).replace(" ", "").replace('\n','').replace(',','').replace('}', '').replace('"', '')
                if diffLine != '':
                    dictionary['Differences']["Contents found in "+filename1+" but not in "+filename2].append(str(diffLine))
    return dictionary

if __name__ == "__main__":
    main(sys.argv)
