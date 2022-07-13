import pytest
from astStaticAnalysis.astBoto3 import generateIAMPolicy


def test_basecase():
    respDict = {'lambda': {'arn:aws:lambda:us-east-1:221094580673:function:testFunction': ['get_function'], 
                '*': ['list_functions']}, 
                's3': {'*': ['list_buckets', 'create_bucket', 'delete_bucket']}}
    response = generateIAMPolicy(respDict)

    assert response == {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "lambda:GetFunction"
            ],
            "Resource": "arn:aws:lambda:us-east-1:221094580673:function:testFunction"
        },
        {
            "Sid": "Statement2",
            "Effect": "Allow",
            "Action": [
                "lambda:ListFunctions"
            ],
            "Resource": "*"
        },
        {
            "Sid": "Statement3",
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets",
                "s3:CreateBucket",
                "s3:DeleteBucket"
            ],
            "Resource": "*"
        }
    ]
    }

def test_emptyInput():
    respDict = {}

    response = generateIAMPolicy(respDict)

    assert response == {
    "Version": "2012-10-17",
    "Statement": [
    ]
    }
def test_IncorrectInput():
    with pytest.raises(Exception):
        response = generateIAMPolicy(None)


test_basecase()