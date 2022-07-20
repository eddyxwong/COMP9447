import os


json_files = []

# Getting the current work directory (cwd)
thisdir = os.getcwd()
# r=root, d=directories, f = files
for r, d, f in os.walk(thisdir):
    for file in f:
        if file.endswith(".json"):
            abspath = os.path.join(r, file)
            json_files.append(str(os.path.relpath(abspath).replace(os.path.sep, '/')))


for x in json_files:
    print(x)