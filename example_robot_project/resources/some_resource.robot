*** Settings ***

*** Variables ***
${some_variable}        message
${another_variable}     message
${third_variable}       message
#${fourth_variable}      message

*** Keywords ***
Some keyword from resource file
    Log    ${some_variable}

Another keyword from resource file
    Log    message