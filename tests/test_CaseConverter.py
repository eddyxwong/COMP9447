import pytest
from astStaticAnalysis.astBoto3 import convertSnakeCasetoPascalCase

def test_basecase():
    testString = "hello_world"

    response = convertSnakeCasetoPascalCase(testString)


    assert response == "HelloWorld"


def test_noUnderscore():
    testString = "Test"

    response = convertSnakeCasetoPascalCase(testString)


    assert response == "Test"


def test_noUnderscoreNoCapital():
    testString = "test"

    response = convertSnakeCasetoPascalCase(testString)


    assert response == "Test"


def test_EmptyString():

    testString = ""
    response = convertSnakeCasetoPascalCase(testString)

    assert response == ""

def NoInput():
    with pytest.raises(Exception):
        response = convertSnakeCasetoPascalCase(None)