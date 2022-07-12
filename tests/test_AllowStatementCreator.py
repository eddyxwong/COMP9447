import pytest
from astStaticAnalysis.astBoto3 import createAllowStatement

def test_basecase():
    resource = "*"
    statementNum = 1
    response = createAllowStatement(resource,statementNum)


    assert response == {"Sid": "Statement" + str(1),
                    "Effect": "Allow",
                    "Action": [],
                    "Resource": "*"}



def test_IncorrectInput():
    resource = "*"
    statementNum = 1
    response = createAllowStatement(None,None)

    with pytest.raises(Exception):
        response = createAllowStatement(None,None)

    # assert response == {"Sid": "Statement" + str(1),
    #                 "Effect": "Allow",
    #                 "Action": [],
    #                 "Resource": "*"}


    

