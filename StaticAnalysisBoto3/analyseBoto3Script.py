from argparse import Action
import json
from pickle import NONE
from sys import prefix
from typing import Dict, List, Tuple
from inspect import getmembers, isfunction, signature
import inspect
import re
from unittest.util import strclass
import ctypes

def analysePythonScript(filepath: str) -> json:

    lineNumDict = createLineNumDict(filepath)


    respDict = getUsedServicesAWS(filepath)  
    print(json.dumps(respDict, sort_keys=False, indent=4))
    statementNum = 1


    newPolicy = {"Version": "2012-10-17",
                "Statement": [] }

    for service in respDict:
        for resource in respDict[service]:

            newPolicy["Statement"].append(createAllowStatement(resource, statementNum))

            for method in respDict[service][resource]:
                caseConverted = convertSnakeCasetoPascalCase(method)

                addService = str(service)+":"+caseConverted


                #list_buckets needs ListAllMyBuckets permission
                if(addService == "s3:ListBuckets"):
                    addService = "s3:ListAllMyBuckets"

                newPolicy["Statement"][statementNum-1]["Action"].append(addService)
                # print(newPolicy["Statement"][statementNum-1]["Action"])
            statementNum +=1
            # print(respDict[service][resource])


    print("Zach's linenum mapping:")
    print(json.dumps(lineNumDict, sort_keys=False, indent=4))




    print("Generated IAM policy:")


    print(json.dumps(newPolicy, sort_keys=False, indent=4))
    return newPolicy



def convertSnakeCasetoPascalCase(string: str) -> str:

    res = string.replace("_", " ").title().replace(" ", "")

    return res



def createAllowStatement(resource: str, statementNum: int) ->json:
    newStatement = {"Sid": "Statement" + str(statementNum),
                    "Effect": "Allow",
                    "Action": [],
                    "Resource": resource}
    
    return newStatement


def createAction(service: str, method: str) -> str:
    return "\""+ service+":"+method + "\""
#"*": [], "resourcearn1": []
# {"lambda" : { { * : [], resourcearn1: [], resourcearn2: []}, "userObjectNames:" []},
# "s3" : {"*": [], "resourcearn2": []}}


# temp = {"lambda" : {"resourcearn1": [], "resourcearn2": []}}


# temp1 = {"userObjectName": "s3",
#         "userObjectName2" : "lambda"}



def getUsedServicesAWS(filepath:str) -> Tuple[Dict[str, Dict[str, List[str]]], Dict[str, str]]:

    userObjDict = createUserObjtoAWSMapping(filepath)

    awsMethodDict = createAWSMethodDict(userObjDict)


    file = open(filepath, 'r')
    lines = file.readlines()
    arnList = []
    lineNum = 1
    for line in lines:

        for userObj in userObjDict:
            if(userObj in line):
                if(getAWSMethod(line, userObj) != None):
                    awsMethod = getAWSMethod(line, userObj)

                    awsService = convertUserObjtoService(userObjDict, userObj)

                    # print(awsMethod, userObj, awsService)

                    nameArg = getMethodNameArg(lineNum, filepath, userObj, arnList)

                    # print(nameArg)

                    if(nameArg not in awsMethodDict[awsService]):
                        awsMethodDict[awsService][nameArg] = []


                    if(awsMethod not in awsMethodDict[awsService][nameArg]):
                        awsMethodDict[awsService][nameArg].append(awsMethod)

        lineNum +=1 
                    
    return awsMethodDict
    # print(json.dumps(awsMethodDict, sort_keys=False, indent=4))
    # print()
    # print(json.dumps(userObjDict, sort_keys=False, indent=4))
    # have to return dict obj to get the defined functions 



def createLineNumDict(filepath):

    lineNumDict = {}
    userObjDict = createUserObjtoAWSMapping(filepath)

    file = open(filepath, 'r')

    lines = file.readlines()

    lineNum = 1

    for line in lines:
        for userObj in userObjDict:
            if userObj in line:
                if(userObj not in lineNumDict):
                    lineNumDict[userObj] = [lineNum]

                else:
                    lineNumDict[userObj].append(lineNum)

        lineNum+=1 

    return lineNumDict
    # for line in lines:




    


def getMethodNameArg(lineNum: int, filepath: str, userobj: str, arnList: list) -> str:
    # returns a list of arns from the userobj, check if list contains arns before returning 
    methodName = getMethodsFromDict(filepath, userobj, arnList)
    # print(methodName, lineNum)
    # print(methodName)
    if methodName:
        # print(methodName)
        return methodName[0]
    else:

        return "*"



def createAWSMethodDict(userObjDict: Dict) -> Dict:
    awsMethodDict = {}
    for value in userObjDict.values():
        if(value not in awsMethodDict):
            awsMethodDict[value] = {"*": []}

    return awsMethodDict
def createUserObjtoAWSMapping(filepath) -> Dict[str, str]:
    userObjServiceDict = {}
    
    file = open(filepath, 'r')

    lines = file.readlines()

    for line in lines:

        service = getService(line)
        if(service != None):
            userObjName = getUserObjectName(line)

            userObjServiceDict[userObjName] = service

    return userObjServiceDict
'''
# Code below extracts 'lambda' from "clientLambda = boto3.client('lambda')""
# Code below extracts 's3' from "clientLambda = boto3.client('s3')""
'''
def getService(string: str) -> List[str]:
    services = re.findall("(?<=boto3\.client\(').*(?='\))", string)

    if(len(services) == 0):
        return None
    return services[0]


# Code below extract 'clientLambda' from "clientLambda = boto3.client('lambda')""
def getUserObjectName(string:str) -> str:

    objNames = re.findall("\w+(?=\s*\=\s*boto3\.client)", string)

    return objNames[0]
    
# As example code below converts clientLambda to lambda
def convertUserObjtoService( userObjDict: Dict, userObj: str) -> str:
    return userObjDict[userObj]

# Code below extracts get_function from  response = clientLambda.get_function()
def getAWSMethod(string: str, userObj: str) -> str:

    regex = r"(?<=" + re.escape(userObj) + r"\.).*(?=\(.*)"

    awsMethod = re.findall(regex,string)

    if(len(awsMethod) == 0):
        return None

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

# create a function that extracts the name of the arn function from the method, i only have the line number, need the arn function name
# First find function name
def getMethodsFromDict(script, obj, arnList):
    cleanedScript = re.search('./(.+?).py',script).group(1)
    module = __import__(cleanedScript)
    # grab a function available in each key and use inspect to find the module name
    # Keys are user defined variables that can call for instance foo.get_functions(FunctionName='arn:aws:lambda:us-east-1:221094580673:function:testFunction')
    file = open(script, 'r')
    lines = file.read()
    #find the particular objs while ignoring objs that do not have the get.function callable next to them
    try:
        func_to_run = getattr(module, obj)
        # this obj is where we need to find the arn encolsed in its brackets
        if getattr(func_to_run, 'get_function'):
            # We want to find all occurances of this function in the string 
            stringToFind = str(obj+'.get_function(')
            # Returns list of indexes where our .getfunction is
            indexList = find_all(lines, stringToFind)
            # find each index
            for index in indexList:
                length = len(stringToFind)
                text = lines[index+length:]
                arnNameList = searchForPhrase(')', text)
                # If it is in the form we want, just check and return it
                for arnName in arnNameList:
                    if re.search('arn:aws:',arnName):
                        if arnName not in arnList:
                            arnList.append(arnName)
                    else:
                        # If it is a user defined variable, we pass it to the extractor
                        userArnName = arnExtractor(cleanedScript, obj, arnName)
                        if (userArnName not in arnList and re.search('arn:aws:',arnName)):
                            arnList.append(userArnName)
                return arnList
    except:
        return ["*"]
        # print("user obj does not have get function")
    # print(arnList)
    return ["*"]
    # return arnList

# Extracts corresponding arn from user defined function name
def arnExtractor(cleanedScript, functionName, arnName):
    module = __import__(cleanedScript)
    func_to_run = getattr(module, functionName)
    try: 
        getattr(func_to_run, 'list_functions')
        # functionDirectory Gives me a list of directories containing function names and corresponding arns
        functionDirectory = func_to_run.list_functions()
        # Iterate through to find the corresponding arns
        for funcName in functionDirectory['Functions']:
            if funcName['FunctionName'] == arnName:
                return funcName['FunctionArn']
    except:
        pass



# Helper function, returns phrase ending with text specified
def searchForPhrase(phrase, text):
    functions = []
    listOfFunc = text.split(phrase)
    for x in listOfFunc:
        clean = re.sub(r"[\n|?|$|.|!|,|'| ]",r'',x)
        clean = re.sub(r'^.*?FunctionName=', '', clean)
        functions.append(clean)
    return functions

def find_all(string, substring):
    result = []
    k = 0
    while k < len(string):
        k = string.find(substring, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1 #change to k += len(sub) to not search overlapping results
    return result

# getUsedServices('testScript.py')


# getUsedServicesAWS('./testLambdaScript.py')


analysePythonScript('./demoScript.py')

# getUsedServicesAWS('./demoScript.py')

# print()
# print("*******")
# print()
# getUsedServicesAWS('./demoScript.py')




'''
when method calls are indented, there are extra characters on the extracted arn string
even when method calls do not have an ARN, the first encountered ARN gets returned
where there are functions with different ARNs, the first encountered ARN gets returned


issues likely due to searching over the entire file

use franks line number to search for the onject then, should be faster and easier to do


'''