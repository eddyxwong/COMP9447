import jsondiff as jd
from jsondiff import diff
import json


f = open("policy1.json")
g = open("policy2.json")

text1 = json.load(f)
text2 = json.load(g)


v = diff(text1, text2, syntax='symmetric')
print(v)