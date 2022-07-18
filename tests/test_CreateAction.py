import pytest
from astStaticAnalysis.astBoto3OLD import createAction

def test_basecase():
    response = createAction("lambda", "get_function")
    assert response == '"lambda:get_function"'

def test_basecase2():
    response = createAction("s3", "list_buckets")
    assert response == '"s3:list_buckets"'


def test_badinput():
    response = createAction("s3", None)
    with pytest.raises(Exception):
        response = createAction(response)

def test_NoInput():
    with pytest.raises(Exception):
        response = createAction(None)