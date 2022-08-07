import ast
import astpretty

tree = ast.parse('x = print("Hello World!")')

astpretty.pprint(tree, show_offsets=False)