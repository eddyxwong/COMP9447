import ast
import json
from pprint import pprint
import astpretty
import sys
def main(argv):
    for arg in argv[1:]:
        print(arg)
        with open(arg, "r") as source:
            tree = ast.parse(source.read())
            # astpretty.pprint(tree, show_offsets=False)

            analyzer = Analyzer()
            analyzer.visit(tree)
            respDict = analyzer.report()
            print(respDict)
            
            response = generateIAMPolicy(respDict)
            print(json.dumps(response, sort_keys=False, indent=4))



        # with open("astTest.py", "r") as source:
        #     tree = ast.parse(source.read())
        #     astpretty.pprint(tree, show_offsets=False)

        # analyzer = Analyzer()
        # analyzer.visit(tree)
        # respDict = analyzer.report()

        
        # response = generateIAMPolicy(respDict)
        # print(json.dumps(response, sort_keys=False, indent=4))



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

    res = string.replace("_", " ").title().replace(" ", "")

    return res



def createAllowStatement(resource: str, statementNum: int):
    newStatement = {"Sid": "Statement" + str(statementNum),
                    "Effect": "Allow",
                    "Action": [],
                    "Resource": resource}
    
    return newStatement


def createAction(service: str, method: str) -> str:
    return "\""+ service+":"+method + "\""


def getUserCreatedObj(node):
        userObj = None
        awsService = None

        for Name in node.targets:

            userObj = Name.id

        for Constant in node.value.args:
                awsService = Constant.value

        return (userObj,awsService)

def getCalledAWSMethod(node, awsService):
    methodARN = "*"
    for keyword in node.value.keywords:
        if(keyword.arg == 'FunctionName'):
            methodARN = keyword.value.value
    return(node.value.func.attr, awsService, methodARN)

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}
        self.userObjDict = {}
        self.calledMethodDict = {}
    # def visit_Import(self, node):
    #     for alias in node.names:
    #         self.stats["import"].append(alias.name)
    #     self.generic_visit(node)

    # def visit_ImportFrom(self, node):
    #     for alias in node.names:
    #         self.stats["from"].append(alias.name)
    #     self.generic_visit(node)
    
        
    def visit_Assign(self, node):
        
        #Code below handles creation of a mapping of user created objects and the AWS service they are connected to. 
        response = getUserCreatedObj(node)

        awsService = response[1]
        userObj = response[0]

        if awsService != None:
            self.userObjDict[userObj] = awsService    

            # return
        if(node.value.func.value.id in self.userObjDict):
            userObj = node.value.func.value.id
            awsService = self.userObjDict[userObj]
            


            response = getCalledAWSMethod(node, awsService)
        
            calledMethod = response[0]
            calledService = response[1]
            methodARN = response[2]



            if calledService not in self.calledMethodDict:
                self.calledMethodDict[calledService] = {}

                self.calledMethodDict[calledService][methodARN] = []

                if calledMethod not in self.calledMethodDict[calledService][methodARN]:
                    self.calledMethodDict[calledService][methodARN].append(calledMethod)

            else:
                if methodARN not in self.calledMethodDict[calledService]:
                    self.calledMethodDict[calledService][methodARN] = []

                    # print(calledMethod)
                    # if calledMethod not in self.calledMethodDict[calledService][methodARN]:
                    #     self.calledMethodDict[calledService][methodARN].append(calledMethod)

                self.calledMethodDict[calledService][methodARN].append(calledMethod)

        self.generic_visit(node)




    def report(self):
        # pprint(self.stats)
        # pprint(self.userObjDict)
        # pprint(self.calledMethodDict)

        return self.calledMethodDict



if __name__ == "__main__":
    main(sys.argv)