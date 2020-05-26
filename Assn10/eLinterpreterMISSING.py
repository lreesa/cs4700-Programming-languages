from random import random, randint, choice
import string
#from newCode import createcode, evaluate

import os
PATH = "C:/Users/lreesa/cs4700/Assn10/"
if not os.path.exists(PATH):
    os.makedirs(PATH)

def readEvalLoop(program):
    grammar = parseGrammar()
    codeList = [parse(oneStatement) for oneStatement in program]
    for code in codeList:
        if checkSyntax(code, '<statement>', grammar):
            print("Syntax error?")
    answer = evalElBody(codeList, {}, [], trace = True)
    print("%s == > %s" % (program, answer))
    
#######################################################################
################# PARSER PARSER   #####################################    
def parse(programString):
    tokens = programString.replace('(', ' ( ').replace(')', ' ) ').split()
    return createcode(tokens)
    
def createcode(tokenList):
    #print(tokenList)
    token = tokenList.pop(0) #pop off (
    if token.isdigit() or token[0].isdigit():
        return int(token)
    if isinstance(token, str) and not token == '(':
        return token
    operator = tokenList.pop(0) 
    if operator.isdigit() or operator[0].isdigit():
        operator = int(operator)
    args = []
    while not tokenList[0] == ')':
        args.append(createcode(tokenList))
    tokenList.pop(0) # pop the ')'
    return [operator] + args
    
#######################################################################
################# CHECK SYNTAX    #####################################    
def checkSyntax(code, grammarWord, grammar):
    #print("%s ==> %s " % (grammarWord, str(code)))
    if isinstance(code, int):
        return grammarWord == '<number>'
    if isinstance(code, str): # +  + for example
        return (grammarWord == code) or grammarWord == '<string>' 
    if code == []:
        return grammarWord == "'"
    oneTrue = True
    for oneRHS in grammar[grammarWord]: #for all possible rhs
        # [ + 6 [+ 4 5]] vs. (+ <expression> <expression>)
        if not len(code) == len(oneRHS):
            continue
        allTrue = False # only one alternative has to be true
        for i in range(0, len(oneRHS)): #
            allTrue = allTrue and checkSyntax(code[i], oneRHS[i], grammar)
        oneTrue = allTrue or oneTrue
        if oneTrue:
            return True
    return False
        
#######################################################################
################# EXECUTE CODE    #####################################    
def evalEl(code, bindings = []):
    answer = evalElHelp(code, bindings)
    #print("Eval %s ==> %s" % (str(code), str(answer)))
    return answer
     
def evalElHelp(code, bindings):
    if isinstance(code, int):
        return code
    if "True" == code:
        return True
    if "False" == code:
        return False
    if isinstance(code, str): # variable
        return findValue(code, bindings)
    fun = code[0]
    if fun == '+':
        return evalEl(code[1], bindings) + evalEl(code[2], bindings)
    if fun == '-':
        return evalEl(code[1], bindings) - evalEl(code[2], bindings)    
    if fun == '*':
        return evalEl(code[1], bindings) * evalEl(code[2], bindings)    
    if fun == '/':
        return evalEl(code[1], bindings) / evalEl(code[2], bindings)
    if fun == 'if':
        if evalEl(code[1], bindings):
            return evalEl(code[2], bindings)
        else:
            return evalEl(code[3], bindings)
    if fun == 'not':
        return not evalEl(code[1], bindings)
    if fun == 'and':
        return evalEl(code[1], bindings) and evalEl(code[2], bindings)
    if fun == 'or':
        return evalEl(code[1], bindings) or evalEl(code[2], bindings)
    if fun == 'eq':
        return evalEl(code[1], bindings) == evalEl(code[2], bindings)
    if fun == '<':
        return evalEl(code[1], bindings) < evalEl(code[2], bindings)
    if fun == 'cons':
        return [evalEl(code[1], bindings)] + evalEl(code[2], bindings)
    if fun == 'first':
        return evalEl(code[1], bindings)
    if fun == 'rest':
         return evalEl(code[2], bindings)
    if fun == 'quote':
         return code[1]
    if fun == 'evalEl':
         return evalEl(evalEl(code[1], bindings))   
     #user function call
    return evalElFun(code[0], code[1:], bindings)

def evalElFun(funName, args, bindings):
    [params, body] = findValue(funName, bindings)
    oneBinding = {}
    for oneParam, oneValue in zip(params, args):
        oneBinding[oneParam] = evalEl(oneValue, bindings)
    return evalElBody(body, oneBinding, bindings)
    
def evalElBody(body, oneBinding, bindings, trace = False):
    #work through a list of statements or expressions, returning the value of the last
    #body is a list of expressions or statements
    #needs to deal with two kinds of statements set and def here
    #oneBinding is a dictonary that contains local bindings,
    #bindings is a list of dictionaries representing bindings
    #trace prints out the steps if needed
    if len(body) == 1:
        return evalEl(body[0], [oneBinding] + bindings)
    code = body[0]
    if code[0] == 'set':
        oneBinding[code[1]] = evalEl(code[2], [oneBinding] + bindings)
    elif code[0] == 'def':
        oneBinding[code[1]] = code[2:]
    else:
        evalEl(code, [oneBinding] + bindings)
    evalElBody(body[1:], oneBinding,  bindings)
    
def findValue(name, bindings):
    #takes a name (a string) and bindings, a list of dictionaries
    #returns the value of this name or throws an error
    #if len(bindings) == 1:
    try:
        return bindings[0][name]
    except:
        if len(bindings) == 1:
            return Exception('This value has not yet been defined')
        else:
            return findValue(name, bindings[1:])
        
#######################################################################
################# READ IN GRAMMAR #####################################    
def readInGrammar():
    with open(PATH + 'eLgrammarDefinition.txt', 'r') as file:  # Use file to refer to the file object
        return file.readlines()
        
def parseGrammar():
    grammar = {}
    for line in readInGrammar():
        if len(line) == 1 or line[0] == '#':
            continue
        rule = line.replace('(', ' ( ').replace(')', ' ) ').replace('|', ' | ').split()
        #map each lhs to a list of alternative rhs
        alternatives = generateAlternatives(rule[2:])
        # for rhs in alternatives:
        #     print("%s => %s" % (rule[0].ljust(20), rhs))
        grammar[rule[0]] = alternatives
    return grammar
        
def generateAlternatives(rhs, current = []):
    #splits into alternative definitions
    if rhs == []: #done
        return [current]
    if rhs[0] == '|': # finish this current alternativ and start a new one
        return [current] + generateAlternatives(rhs[1:], [])
        # continue the current alternative
    return generateAlternatives(rhs[1:], current + [rhs[0]])
    
##########################################################################################
readEvalLoop(["(+ 5 6)"])
readEvalLoop(["(set x (+ 5 6))", "(set y (+ 5 x))", " (* x y))"])
# readEvalLoop(["(def f (x y) (+ x y))", "set x 10)" , "(set y (+ 5 (f x 1)))", " (* x y))"])
# readEvalLoop(["(set x 5)", 
#               "(def fact (x) (if (eq x 1) x (* x (fact ( - x 1)))))", 
#               "(+ (fact 5) (fact x))"])
# readEvalLoop(["(set l (quote (1 2 3 4 5)))",
#               "(set q (quote (1 2 3 4 5)))",
#               "(def equal (a b) (if (eq a b) True (and (equal (first a) (first b)) (equal (rest a) (rest b)))))",
#               "(equal l q)"])
              
# readEvalLoop(["(def count (N n) (if (eq N 0) (eq n 0) (if (< n 0) 0 (countEach N n 6))))",
#               "(def countEach (N n face) (if (eq face 0) 0 (+ (count (- N 1) (- n face))(countEach N n (- face 1)))))",
#               "(count 5 10)"])
            
# readEvalLoop(["(set x 5)", 
#               "(def fib (x) (if (eq x 1) x (+ (fib ( - x 2) (fib (- x 1)))))", 
#               "(+ (fib 2) (fib x))"])