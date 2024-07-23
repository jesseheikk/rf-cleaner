*** Settings ***
Resource        ../resources/some_resource.robot
Test Timeout    20

*** Keywords ***
Keyword from test suite
    Log    message

Another keyword from test suite
    Log    ${another_variable}

*** Test Cases ***
Some example test case
    Another keyword from test suite
    Some keyword from resource file