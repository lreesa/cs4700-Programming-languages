# Laryssa Revelli
# A01979841
from random import random, randint
import os
PATH = "C:/Users/lreesa/cs4700/Assn10/"
if not os.path.exists(PATH):
    os.makedirs(PATH)

Index = 0
Bindings = {}
ReservedWords = ['+', '-', '*', '/', 'if', 'and', 'or', 'not', '>', 'eq', 'def', 'set', 'True', 'False']
OperatorsAll = ['+', '-', '*', '/', 'if', 'and', 'or', 'not', '>', 'eq', 'set', 'def']
OperatorsBoolBool = ['and', 'or', 'not', 'eq']
OperatorsBoolNumb = ['>', 'eq']
OperatorsNumb = ['+', '-', '*', '/']
OperatorsDeclaritive = ['set', 'def']
NumberOfArguments = {}
ArgumentCount = [(1, ['not']),(2, ['+', '-', '*', '/', '>', 'and', 'or', 'eq', 'set']), (3, ['if', 'def'])]
# # fill the mapping from operator to argument count
for (count, operators) in ArgumentCount:
    for op in operators:
        NumberOfArguments[op] = count

def atom(token):       
    # changes a token to an actual integer or boolean
    if token.isdigit():
        return int(token)
    if token == 'True' :
        return bool(token)
    if token == 'False':
        return not bool(token)
    return token

### takes a program string and returns a parse tree
def parse(programStr):
    # returns the input string as a parse tree, represented as either an int or a list of expressions
    return createParseTree(tokenize(programStr))
    
### does error checking
def parseX(programStr):
    # returns the input string as a parse tree, represented as either an int or a list of expressions
    return createParseTreeX(tokenize(programStr))

def createParseTree(tokenList):
    token = tokenList.pop(0)
    if isinstance(token, int) or isinstance(token, bool):
        return token
    operator = tokenList.pop(0) 
    parseTree = [operator]
    for i in range(NumberOfArguments[operator]):
        parseTree += [createParseTree(tokenList)]
    tokenList.pop(0) # pop the ')'
    return parseTree
     
def createParseTreeX(tokenList):
    if tokenList == []:
        raise Exception("Run out of tokens")
    token = tokenList.pop(0)
    if isinstance(token, int) or isinstance(token, bool):
        return tokenList
    if not token == "(":
        raise Exception("Found %s instead of (" % (token,))
    if tokenList == []:
        raise Exception("Missing Operator")
    operator = tokenList.pop(0) 
    if not operator in OperatorsAll:
        raise Exception("Unknown operator %s" % operator)
    parseTree = [operator]
    for i in range(NumberOfArguments[operator]):
        parseTree += [createParseTree(tokenList)]
    if tokenList == []:
        raise Exception("Missing )")
    close = tokenList.pop(0) # pop the ')'
    if not ')' == close: # pop the ')'
        raise Exception("Found %s instead of )" % (close,))
    return parseTree

### takes a program string and evaluates
def evalL(programStr):
    # returns the solution of expressions
    try:
        return evaluate(createParseTree(tokenize(programStr)))
    except Exception as error:
        print(error)

def evaluate(parseTree):
    if isinstance(parseTree, int):
        return parseTree
    if isinstance(parseTree, bool):
        return parseTree
    if parseTree in Bindings: #vars
        return Bindings[parseTree]
    operator = parseTree[0]
    if operator == '+':
        return evaluate(parseTree[1]) + evaluate(parseTree[2])
    if operator == '-':
        return evaluate(parseTree[1]) - evaluate(parseTree[2])
    if operator == '*':
        return evaluate(parseTree[1]) * evaluate(parseTree[2])
    if operator == '/':
        divisor = evaluate(parseTree[2])
        if divisor == 0:
            raise Exception('Cannot divide by 0')
        else:
            return evaluate(parseTree[1]) / divisor
    if operator == 'not':
        return not evaluate(parseTree[1])
    if operator == 'and':
        return evaluate(parseTree[1]) and evaluate(parseTree[2])
    if operator == 'or':
        return evaluate(parseTree[1]) or evaluate(parseTree[2])
    if operator == '>':
        return evaluate(parseTree[1]) > evaluate(parseTree[2])
    if operator == 'eq':
        return evaluate(parseTree[1]) == evaluate(parseTree[2])
    if operator == 'if':
        if evaluate(parseTree[1]):
            return  evaluate(parseTree[2])
        else:
            return evaluate(parseTree[3])
    if operator == 'set':
        Bindings[parseTree[1]] = evaluate(parseTree[2])
    if operator == 'def':
        Bindings[parseTree[1]] = parseTree[2:]
    if operator in Bindings:
        (args, body) = Bindings[operator]
        for i in range(len(args)):
            Bindings[args[i]] = evaluate(parseTree[i+1])
        for j in range(len(body)-1):
            evalL(body[j])
        return evalL(body[-1])

def quote(parseTree):
    return parseTree

        
### very simple code that just checks whether the number of open parentheses
### is the same as the number of closed parentheses
def checkBalanced(tokenList):
    depth = 0
    while not tokenList == []:
        token = tokenList.pop(0)
        if token == '(': #consume and add 1 to depth
            depth = depth + 1
        if token == ')':
            depth = depth - 1
    return depth == 0
    
### takes a string representing an expression in simple lisp and returns a list of tokens
def tokenize(programStr):
    tokens = programStr.replace('(', ' ( ').replace(')', ' ) ').split()
    if all(legalToken(token) for token in tokens):
        return [atom(token) for token in tokens]
    else:
        badTokens = str([token for token in tokens if not legalToken(token)])[1:][:-1]
        raise Exception("Unknown token found %s" % (badTokens,))
  
### returns True if the token is legal      
def legalToken(token):
    # returns True if legal for our simple lisp
    return (token.isdigit() or token == 'True' or token == 'False'
                           or token in OperatorsAll + [')', '(']
                           or isinstance(token, str)) #vars

evalL('(set var 7)')
print(Bindings[var])