import json
from pickle import NONE
from sys import prefix
from typing import Dict, List, Tuple
from inspect import getmembers, isfunction, signature
import inspect
import re
import pprint

def analysePythonScript(filepath: str) -> json:

    respDict = getUsedServices(filepath)  

    newPolicy = {"Version": "2012-10-17",
                "Statement": [] }


    newStatement = createAllowStatement()

    for service in respDict:
        if("service" == "lambda"):
            for method in respDict[service]:
                newAction = createAction(service, method)
                newStatement["Action"].append(newAction)

    return newPolicy


def createAllowStatement() ->json:
    newStatement = {"Effect": "Allow",
                    "Action": [],
                    "Resource": "*"}
    
    return newStatement


def createAction(service: str, method: str) -> str:
    return "\""+ service+":"+method + "\""
#"*": [], "resourcearn1": []
# {"lambda" : { { * : [], resourcearn1: [], resourcearn2: []}, "userObjectNames:" []},
# "s3" : {"*": [], "resourcearn2": []}}


temp = {"lambda" : {"resourcearn1": [], "resourcearn2": []}}


temp1 = {"userObjectName": "s3",
        "userObjectName2" : "lambda"}



def getUsedServicesAWS(filepath:str) -> Tuple[Dict[str, Dict[str, List[str]]], Dict[str, str]]:


    serviceARNDict = {}
    userObjServiceDict = {}


    file = open(filepath, 'r')
    lines = file.readlines()

    serviceARNDict = {}


    for line in lines:
        service = getService(line)
        if(service != None):
            objName = getUserObjectName(line)
            serviceARNDict[service] = {"*": [], "exampleARN1": [] , "exampleARN2": []}

            userObjServiceDict[objName] = service
        else:
            callingObj = getCallingObject(line, userObjServiceDict)

            if(callingObj != None):
                callingObjAWS = convertUserObjtoService(userObjServiceDict, callingObj)
                awsMethod = getAWSMethod(line, callingObjAWS)
                serviceARNDict[callingObjAWS]["*"].append(awsMethod)



    # pprint.pprint(serviceARNDict)
    # pprint.pprint(userObjServiceDict)
    # print(serviceARNDict)
    # print(userObjServiceDict)
    print(json.dumps(serviceARNDict, sort_keys=False, indent=4))
    # print(json.dumps(userObjServiceDict, sort_keys=False, indent=4))



def getService(string: str) -> List[str]:
    services = re.findall("(?<=boto3\.client\(').*(?='\))", string)

    if(len(services) == 0):
        return None
    return services[0]

def getUserObjectName(string:str) -> str:

    objNames = re.findall("\w*(?=\s*\=\s*boto3\.client)", string)

    return objNames[0]
    
def convertUserObjtoService( userObjServiceDict: Dict, userObj: str) -> str:
    return userObjServiceDict[userObj]


def getCallingObject(string: str, userObjServiceDict: Dict) -> str:
    for objName in userObjServiceDict:
        if objName in string:
            return objName
                   
    return None

def getAWSMethod(string: str, callingObjName: str) -> str:

    awsMethod = re.findall("(?<=clientLambda\.).*(?=\()",string)

    return awsMethod[0]


'''
{"s3": [list_bucket_names], 
"cloudtrail": [list_event_data_stores, list_trails]}

'''
'''
questions to ask frank
    1. Would we be assuming that the script passed in would be creating a bucket using boto3?
    2. If the script uses defined functions instead of s3, it may be an issue gonna try to solve it
'''

def getUsedServices(filepath: str) -> Dict[str, str]:
    # File would be of type xx.py
    file = open(filepath, 'r')
    # list contents of file containing script
    contents = file.readlines()
    # Create a list to append to for bucket names
    bucketNameList = []
    # Check if there are any functions in the script that creates buckets, returns a 2 lists, one containing user defined functions that create buckets and the other returns 
    # an ignore list for any functions not defined but still create buckets
    bucketCreationFunctions, bucketIgnoreList= BucketFunctionSearcher(filepath)
    # This function will search through and find the bucketnames of all buckets created through either user-defined functions or s3_create_bucket
    BucketSearcher(contents, bucketNameList, bucketIgnoreList, bucketCreationFunctions)

    print(bucketCreationFunctions)
    print(bucketIgnoreList)
    print(bucketNameList)


# This function will search for s3.create_bucket command and add to a list of all bucket names for that instance
def BucketSearcher(contents, bucketList, ignoreList, bucketFunctions):
    # Check for Errors
    if contents == NONE:
        print("Error, script is empty")
        exit()
    for line in contents:
        #clean line
        line = line.rstrip('\n')
        # Remove all items in ignore list from lines
        line = removeFunctions(line,ignoreList)
        # Check for bucket creation commands not in any user-defined functions
        getBucketName(line, bucketList)
        # Check for user-defined functions which create buckets and get their names
        getUserBucketNames(line,bucketList, bucketFunctions)
    # check for success
    if bucketList:
        print("Successfully added bucketnames to list")
    else:
        print("No bucket creation found")
    
    
# This checks for any functions in the script provided that create s3 buckets
# returns 2 lists. one to check for functions later and one to use to ignore 
def BucketFunctionSearcher(scriptName):
    bucketCreationFunctions = []
    bucketIgnoreFunctions = []
    # Convert script name as module
    module = __import__(scriptName.rstrip('.py'))
    # Generate list of user-defined functions
    flist = (functionList(m) for m in getmembers(module, isfunction))
    # Check if any functions create a bucket
    bucketCreationFunctions, bucketIgnoreFunctions = functionFinder(flist, module, bucketCreationFunctions, bucketIgnoreFunctions)
    # If list is empty, no buckets were found to be created
    if not bucketCreationFunctions: 
        print("No bucket creation found")
    return bucketCreationFunctions, bucketIgnoreFunctions


# Get all user defined functions in script and contain inside a list
def functionFinder(flist, module, bucketList, ignoreList):
    for functionName in flist:
        # Remove the function vars to enable inspection of functions
        cleanedFunction = functionName[ 0 : functionName.index("(")]
        # convert string name to function of module
        func_to_run = getattr(module, cleanedFunction)
        # inspect the function to find if a bucket is created inside it
        functionLines = inspect.getsource(func_to_run)
        # All we need is to check if the function creates a bucket and we can add it to the list
        if 's3.create_bucket' in functionLines:
            print("Found bucket creation function in user-defined functions, adding to function list....")
            # Append the name of the function to the list so we can check how many times its run later
            bucketList.append(cleanedFunction)
            ignoreList.append(functionName)
            # Now we find the command in the function itself
            # Convert str to list
            ignoreFunctionList = functionLines.split()
            # Find all s3_create_bucket commands
            list = [x for x in ignoreFunctionList if re.search('s3.create_bucket', x)]
            for foundFunctions in list:
                suffix = ')'
                prefix = ','
                suffix_index = foundFunctions.find(suffix)
                suffixCheck = foundFunctions[0:suffix_index]
                if prefix not in suffixCheck:
                    if foundFunctions not in ignoreList:
                        ignoreList.append(foundFunctions)
                elif prefix in suffixCheck:
                    if suffixCheck not in ignoreList:
                        ignoreList.append(suffixCheck)
            
    return bucketList, ignoreList


def getBucketName(line, bucketList):
    if 's3.create_bucket' in line:
        print("Searching for bucket name outside of user functions....")
        # Get index of bucket function call
        bucketNameIndex = line.find('s3.create_bucket')
        # Find bucket name specified by script, standadised to +24 from function call
        suffix = ')'
        # Check if correct position is found
        positionChecker = line.endswith(suffix,bucketNameIndex+24)
        if positionChecker:
            # Strip suffix
            bucketName = line[bucketNameIndex+24:].rstrip(')')
            bucketList.append(bucketName)
        else:
            print("Error, found function but name was not found, please be a better coder")

def getUserBucketNames(line, bucketList, bucketFunctions):
    for functions in bucketFunctions:
        # line is my whole function while functions are the names before any vars are added
        functionIndex = line.find('(')
        comparator = line[0:functionIndex]
        if functions==comparator:
            print("Searching for bucket name from user functions....")
            # Get index of bucket function call so you will find start of index of foo
            bucketNameIndex = line.find(functions)
            # Find bucket name specified by script, standadised to +24 from function call
            suffix = ')'
            prefix = ','
            suffix_index = line.find(suffix)
            prefix_index = line.find(prefix)
            # Get args in function: def create_bucket(bucket_name, region=None):
            suffixCheck = line[bucketNameIndex+len(functions):suffix_index]
            print(suffixCheck)
            # check that additional arg for region is not present
            if prefix not in suffixCheck:
                bucketname = suffixCheck.replace('(','')
                # Append to list
                bucketList.append(bucketname)
            # Check if additonal args are present
            elif prefix in suffixCheck:
                # Stop index at first ',' to obtain bucket name instead of region
                bucketname = (line[bucketNameIndex+len(functions):prefix_index]).replace('(','')
                # Append to list
                bucketList.append(bucketname)

# Helper function to ascertain if key corresponds to a user-defined function
def functionList(key):
    try:
        return f"{key[0]}{signature(key[1])}"
    except ValueError:
        return f"{key[0]}(???)" # some functions don't provide a signature

# Helper function to remove unwanted functions in string
def removeFunctions(line, ignoreList):
    for ignore in ignoreList:
        if ignore in line:
            line = line.replace(ignore,'')
    return line

'''
To DO:
Cloud Trail (Should be easy with all the helper functions i have)

'''



# getUsedServices('testScript.py')


getUsedServicesAWS('./testLambdaScript.py')



