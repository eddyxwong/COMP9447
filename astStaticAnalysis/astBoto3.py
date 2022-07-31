import ast
import json
import os
from pprint import pprint
import argparse
from typing import List
import astpretty
import subprocess
'''
general style refactoring, pylint
arg parse (add details, !directory argument!)
comparable function CLI. 
parsing of directorys, filter for python files in directory recursively, potentially can use walk
python filter in built function


AST walker, find boto3 object client (extensible for resources and sessions) medium
have existing file in repo, with mapping of actions (iann file) do first

'''

def main():
    args = parseArgs()

    astList = fileASTConvert(args.files)

    astList +=dirAstConvert(args.dir)


    resp = analyseASTList(astList)

    iamPolicy = json.dumps(generateIAMPolicy(resp), sort_keys=False, indent=4)

    policyFile = createPolicyFile(iamPolicy)

    createTerraformTemplate(args.tf, policyFile)

    createCFNTemplate(args.cfn, iamPolicy)

    # print(json.dumps(generateIAMPolicy(resp), sort_keys=False, indent=4))
    return json.dumps(generateIAMPolicy(resp), sort_keys=False, indent=4)

def dirAstConvert(dirargs):

    pythonFiles = []
    if(dirargs):
        for dir in dirargs:
            for root, dirs, files in os.walk(dir, topdown = False):
                for file in files:
                    if file.endswith(".py"):
                        pythonFiles.append(os.path.join(os.path.abspath(root), file))

    return fileASTConvert(pythonFiles)





def createCFNTemplate(cfnArg:bool, iamPolicy:json):
    if(cfnArg):
        with open('./templates/cfnSample.json') as json_file:
            cfnTemplate = json.load(json_file)
            iamPolicy = json.loads(iamPolicy)

            cfnTemplate["Resources"]["MyIAMPolicy"]["Properties"]["PolicyDocument"] = iamPolicy


        with open('cfnTemplate.json', 'w') as f:
            f.write(json.dumps(cfnTemplate, sort_keys=False, indent=4))
    
    return




def createTerraformTemplate(tfArg: bool, policyFile:json):
    if(tfArg):
        p = subprocess.Popen(["iam-policy-json-to-terraform < "+ policyFile+" > tfTemplate.tf"], stdout=subprocess.PIPE,shell=True)
    
    return 


def createPolicyFile(iamPolicy:json)->str:
    """Writes a given IAM policy is json format to a file titled policy.json in the same directory

    Args:
        iamPolicy (json): IAM policy in json format

    Returns:
        str : name of the created IAM policy file
    """
    with open('policy.json', 'w') as f:
        f.write(iamPolicy)

    return "policy.json"



def analyseASTList(astList: List[ast.AST]) -> dict:
    """Given a list of ASTs traverses each ast extracting information

    Args:
        astList (List[ast.AST]): list of asts

    Returns:
        dict: a dictionary with the extract information which will be used in IAM policy generation

        Example return:

        {'lambda': 
            {'arn:aws:lambda:us-east-1:221094580673:function:testFunction': 
                ['get_function']},
        's3': 
            {'*':
                ['list_buckets']}}
    """
    analyzer = Analyzer()

    for tree in astList:
        analyzer.visit(tree)
        # resp = analyzer.report()

    resp = analyzer.report()

    return resp
#args.files as input
def fileASTConvert(fileargs):
    """Given a list of files parsed in as arguments, generates the AST of each file before appending to a list

    Args:
        fileargs (str): a string of file names

    Returns:
        List(ast): list of asts
    """
    astList = []

    for arg in fileargs:
        with open(arg, "r") as source:
            tree = ast.parse(source.read())
            astList.append(tree)

    #Code below formats the AST and prints it out
    #astpretty.pprint(tree, show_offsets=False)
    return astList


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help="list of files")
    parser.add_argument('--dir' ,nargs='+', help="a directory of files")
    parser.add_argument('--tf' ,action='store_true', help="a flag for if you also want a terraform template")
    parser.add_argument('--cfn', action='store_true', help="a flag for if you also want a cloudformation template" )

    return parser.parse_args()

def generateIAMPolicy(respDict):
    """Given actions extract from boto3 script generate an IAM policy

    Args:
        respDict (_type_): _description_

    Returns:
        str: IAM policy
    """
    with open('./awsMappings/python/map.json') as json_file:
        mapping = json.load(json_file)


    statementNum = 1


    newPolicy = {"Version": "2012-10-17",
                "Statement": [] }

    for service in respDict:
        for resource in respDict[service]:

            newPolicy["Statement"].append(createAllowStatement(resource, statementNum))

            for method in respDict[service][resource]:
                caseConverted = convertSnakeCasetoPascalCase(method)

                
                addServiceMap = str(service).capitalize()+"."+caseConverted
                addServiceMap = addServiceMap.lower()
                iamPermission = mapping[addServiceMap]


                newPolicy["Statement"][statementNum-1]["Action"].append(iamPermission)


                #Code below is old version when we didnt have the mapping
                # addService = str(service)+":"+caseConverted
                #list_buckets needs ListAllMyBuckets permission
                #potentially hardcode others later on
                # if(addService == "s3:ListBuckets"):
                #     addService = "s3:ListAllMyBuckets"

                # newPolicy["Statement"][statementNum-1]["Action"].append(addService)

                # print(newPolicy["Statement"][statementNum-1]["Action"])
            statementNum +=1
            # print(respDict[service][resource])
    return newPolicy


def convertSnakeCasetoPascalCase(string: str) -> str:
    """function to convert a string to Pascal Case. Needed in IAM policy generation

    Args:
        string (str): any string

    Returns:
        str: converted string
    """

    res = string.replace("_", " ").title().replace(" ", "")

    return res



def createAllowStatement(resource: str, statementNum: int):
    """Creates a statement which compose IAM policies

    Args:
        resource (str): resource ARN
        statementNum (int): statementNum, no functional purpose
    Returns:
        dict : Dictionary with required structure.
    """
    newStatement = {"Sid": "Statement" + str(statementNum),
                    "Effect": "Allow",
                    "Action": [],
                    "Resource": resource}
    
    return newStatement


def createAction(service: str, method: str) -> str:
    return "\""+ service+":"+method + "\""



# {'lambda': {'arn:aws:lambda:us-east-1:221094580673:function:testFunction': ['get_function'], '*': ['list_functions']}, 's3': {'*': ['list_buckets', 'create_bucket', 'delete_bucket']}}

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}


        '''
        extractDict contains all extracted actions from a boto3 script file which will
        be used in the IAM policy generation
        '''
        self.extractDict = {}

        '''
        userObjDict provides a mapping of the user created objects and the AWS service they interact with. 
        As example:
        {'clientLambda': 'lambda'}

        Consider classes, self references

        This dictionary indicates that there is a user created object 'clientLambda' that interfaces with the lambda service
        '''
        self.userObjDict = {}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)
    def visit_Assign(self, node):
        try:
            if(node.value.func.value.id == 'boto3'):
                self.userObjDict[node.targets[0].id] = node.value.args[0].value

                if node.value.args[0].value not in self.extractDict:
                    self.extractDict[node.value.args[0].value] = {}
        
                self.generic_visit(node)

            else:
                callingUserObj = node.value.func.value.id

                if(callingUserObj in self.userObjDict):

                    awsMethod = node.value.func.attr

                    keywords = node.value.keywords

                    nameArg = "*"
                    # node.value.keywords
                    if keywords == []:
                        nameArg = "*"
                    else:
                        for keyword in keywords:

                            '''
                            FunctionName refers to name argument for lambda 
                            equivalent s3 argument is sometimes 'Bucket'
                            '''
                            if keyword.arg == 'FunctionName':
                                nameArg = keyword.value.value
                                '''
                                session -> config ->
                                Figure out how to translate testFunction to arn:aws:lambda:us-east-1:221094580673:function:testFunction
                                '''
                    awsService = self.userObjDict[callingUserObj]   
                    
                    if nameArg not in self.extractDict[awsService]:
                        self.extractDict[awsService][nameArg] = []

                    if(awsMethod not in self.extractDict[awsService][nameArg]):
                        self.extractDict[awsService][nameArg].append(awsMethod)          
        except AttributeError:
        # except:
            self.generic_visit(node)


        self.generic_visit(node)

    def report(self):
        # pprint(self.stats)
        pprint(self.userObjDict)
        pprint(self.extractDict)
        # print()

        return self.extractDict


if __name__ == "__main__":
    main()
