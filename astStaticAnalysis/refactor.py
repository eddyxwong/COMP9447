import ast
from pprint import pprint
import astpretty
from keyring import set_keyring

def main():
    with open("refactorTest.py", "r") as source:
        tree = ast.parse(source.read())
        astpretty.pprint(tree, show_offsets=False)
    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()

# {'lambda': {'arn:aws:lambda:us-east-1:221094580673:function:testFunction': ['get_function'], '*': ['list_functions']}, 's3': {'*': ['list_buckets', 'create_bucket', 'delete_bucket']}}

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

        self.extractDict = {}

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
                    # if node.value.keywords == []:
                    print(callingUserObj)
            

        except AttributeError:
            self.generic_visit(node)


        self.generic_visit(node)

           



    def report(self):
        # pprint(self.stats)
        pprint(self.userObjDict)
        pprint(self.extractDict)


if __name__ == "__main__":
    main()