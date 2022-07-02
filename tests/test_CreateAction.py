from astStaticAnalysis.astBoto3 import createAction

def test_basecase():
    response = createAction("lambda", "get_function")
    assert response == '"lambda:get_function"'

def test_basecase2():
    response = createAction("s3", "list_buckets")
    assert response == '"s3:list_buckets"'

