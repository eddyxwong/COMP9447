import json

# s3.uploadfile is missing from official documentation, hence we had to manually put it in.

with open('test.json') as data_file:    
    data = json.load(data_file)

    mappingDict = {}

    for sdkMethod in data["sdk_method_iam_mappings"]:

        mappingDict[sdkMethod.lower()] = data["sdk_method_iam_mappings"][sdkMethod][0]['action']

        # if(sdkMethod == "S3.ListBuckets"):
        #     print(data["sdk_method_iam_mappings"][sdkMethod][0]['action'])
        #     print(sdkMethod)
    mapping = json.dumps(mappingDict, sort_keys=True, indent=4)

    with open('map.json', 'w') as f:
        f.write(mapping)


    # print(mappingDict)