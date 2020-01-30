def createParseTree(tokenList):
    token = tokenList.pop(0)
    if isinstance(token, int) or isinstance(token, bool):
        return token
    operator = tokenList.pop(0) 
    for i in NumberOfArguments(operator):
        arg = createParseTree(tokenList)
    tokenList.pop(0) # pop the ')'
    return [operator] + [firstArg] + [secondArg]
     
def createParseTreeX(tokenList):
    if tokenList == []:
        raise Exception("Run out of tokens")
    token = tokenList.pop(0)
    if isinstance(token, int):
        return tokenList
    if not token == "(":
        raise Exception("Found %s instead of (" % (token,))
    if tokenList == []:
        raise Exception("Missing Operator")
    operator = tokenList.pop(0) 
    if not operator in Operators:
        raise Exception("Unknown operator %s" % operator)
    for i in NumberOfArguments(operator):
        arg = createParseTree(tokenList)
    if tokenList == []:
        raise Exception("Missing )")
    close = tokenList.pop(0) # pop the ')'
    if not ')' == close: # pop the ')'
        raise Exception("Found %s instead of )" % (close,))
    return [operator] + [firstArg] + [secondArg]