import ast
import json
from pprint import pprint

import astpretty
from keyring import set_keyring


def main():
    with open("refactorTest.py", "r") as source:
        tree = ast.parse(source.read())

        '''
        Code below formats the AST and prints it out
        '''
        # astpretty.pprint(tree, show_offsets=False)



    analyzer = Analyzer()
    analyzer.visit(tree)
    resp = analyzer.report()
    print(json.dumps(generateIAMPolicy(resp), sort_keys=False, indent=4))


def generateIAMPolicy(respDict):
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
                #potentially hardcode others later on
                if(addService == "s3:ListBuckets"):
                    addService = "s3:ListAllMyBuckets"

                newPolicy["Statement"][statementNum-1]["Action"].append(addService)
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

        self.extractDict = {}


        '''
        userObjDict provides a mapping of the user created objects and the AWS service they interact with. 
        As example:
        {'clientLambda': 'lambda'}

        This dictionary indicates that there is a user created object 'clientLambda' that interacts with the lambda service
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

                    if node.value.keywords == []:
                        nameArg = "*"
                    else:
                        for keyword in node.value.keywords:

                            '''
                            FunctionName refers to argument for lambda 
                            s3 argument is sometimes 'Bucket'
                            '''
                            if keyword.arg == 'FunctionName':
                                nameArg = keyword.value.value
                                '''
                                Figure out how to translate testFunction to arn:aws:lambda:us-east-1:221094580673:function:testFunction
                                '''
                    awsService = self.userObjDict[callingUserObj]   
                    
                    if nameArg not in self.extractDict[awsService]:
                        self.extractDict[awsService][nameArg] = []

                    if(awsMethod not in self.extractDict[awsService][nameArg]):
                        self.extractDict[awsService][nameArg].append(awsMethod)          

        except AttributeError:
            self.generic_visit(node)


        self.generic_visit(node)

    def report(self):
        # pprint(self.stats)
        pprint(self.userObjDict)
        pprint(self.extractDict)
        print()
        return self.extractDict


if __name__ == "__main__":
    main()
