# Laryssa Revelli
# A01979841
from random import random, randint
import os
PATH = "C:/Users/lreesa/cs4700/Assn5n6/"
if not os.path.exists(PATH):
    os.makedirs(PATH)

########## 1) BNF Grammar ############################################################
# <function> := '(' 'def' <variable> <argumentList> <body> ')'
# <body> := '(' ')' | '(' <statementList> ')' | '(' <expression> ')'
# <statementList> := <statement> | <statement> <statementList>
# <statement> := '(' 'set' <variable> <expression> ')'
# <argumentList> := '(' ')' | '(' <varList> ')'
# <varList> := <variable> | <variable> <varList>
# <variable> := <charList> | <charList> <integer> && ! <reservedWords> 
# <charList> := <char> | <char> <charList>
# <reservedWords> := 'def' | 'set' | 'if' | 'True' | 'False' | 'not' | <booleanOperator> | <operator>]

# <expression> := <booleanExpression> | <numberExpression> | <variable>
#                 | '(' 'if' <booleanExpression> <expression> <expression> ')'

########################### Unchanged #########################################
# <booleanExpression> ::= 'True' | 'False' | '(' 'not' <booleanExpression> ')'
#                 | '(' <booleanOperator> <booleanExpression> <booleanExpression> ')'
#                 | '(' '>' <numberExpression> <numberExpression> ')'
#                 | '(' 'eq' <expression> <expression> ')'
# <numberExpression> ::= <integer> | '(' <operator> <expression> <expression> ')' 
# <operator> := '+' | '-' | '*' | '/'
# <booleanOperator> := 'and' | 'or' # 'not' is accounted for in booleanExpression
#######################################################################################
    
# define all the possible operators and how many arguments they take
# for extended language
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
     
def processAllGood ():
    # Generate a set of correct random test problems
    with open(PATH + 'correctSyntax.txt', 'r') as file:  # Use file to refer to the file object
        programs = file.readlines()
    for i in range(0, len(programs)):
        parse(programs[i])
        print("Index = %d \n" % i)

def generateRandomProgram(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our L language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    elif random() < 0.3:
        return generateRandomExpressionBool(maxDepth - 1)
    elif random() < 0.3:
        return generateRandomExpressionNumb(maxDepth - 1)
    else:
        return "(if %s %s %s)" % (generateRandomExpressionBool(maxDepth - 1), 
                                  generateRandomProgram(maxDepth - 1), 
                                  generateRandomProgram(maxDepth - 1))
                                  
def generateRandomExpressionNumb(maxDepth):
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    return "(%s %s %s)" % (OperatorsNumb[randint(0,len(OperatorsNumb)-1)],
                            generateRandomExpressionNumb(maxDepth-1),
                            generateRandomExpressionNumb(maxDepth-1))
                                  
def generateRandomExpressionBool(maxDepth):
    if random() < 0.1 or maxDepth < 0:
        return ['True', 'False'][randint(0,1)]
    elif random() < 0.5:
        operator = OperatorsBoolBool[randint(0, len(OperatorsBoolBool)-1)]
        if NumberOfArguments[operator] == 1:
            return "(%s %s)" % (operator, 
                                generateRandomExpressionBool(maxDepth - 1))
        if NumberOfArguments[operator] == 2:
            return "(%s %s %s)" % (operator, 
                                   generateRandomExpressionBool(maxDepth - 1),
                                   generateRandomExpressionBool(maxDepth - 1))
    else:
        operator = OperatorsBoolNumb[randint(0, len(OperatorsBoolNumb)-1)]
        return "(%s %s %s)" % (operator,
                                generateRandomExpressionNumb(maxDepth - 1),
                                generateRandomExpressionNumb(maxDepth - 1))
    
def genGood ():
    # Generate a set of correct random test problems
    with open(PATH + 'correctSyntax.txt', 'w') as file:  # Use file to refer to the file object
        for _ in range(0, 1000):
            file.write(generateRandomExpressionNumb(1 + randint(0,10)) + "\n")
            
def genBad ():
    with open(PATH + 'errorSyntax.txt', 'w') as file:  # Use file to refer to the file object
        for _ in range(0, 1000):
            program = generateBadRandomExpression(1 + randint(0,10)) #(1 + randint(0,10))
            try: #try to parse the expression
                parse(program)
            # Only if it does not parse then we save
            except Exception as error:
                file.write(program + "\n")
         
BadOps = ['_', '=','(','%']
BadNumbers = ['1.2344','x','y']
def generateBadRandomExpression(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    if random() < 0.05 or maxDepth < 0:
        return str(BadNumbers[randint(0, len(BadNumbers)-1)])
    elif random() < 0.05:
        return "(%s %s %s" % (OperatorsAll[randint(0, 9)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
    elif random() < 0.05:
        return "%s %s %s)" % (OperatorsAll[randint(0, 9)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
    else:
        return "(%s %s %s)" % (OperatorsAll[randint(0, 9)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))

# 2) Extend your parser to handle all the above additional language constructs. 
# This will involve adding new terminals (atoms) to the lexical analyzer, 
# extending the cases that the parser can handle, and extending the pretty printer 
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

def testEvaluator():
    # tests the evaluator by looping over 1000 random legal expressions 
    # and evaluating the expression and printing the result.
    for _ in range(0, 1000):
        prg = generateRandomProgram(1 + randint(0,10))
        print(prg)
        print(evalL(prg)) 
    
        
### prettyPrint an expression (parsed list of tokens)
# takes a parse tree and prints it out so it is easier to read (maybe)
def prettyPrintExp(expression, depth = 0):
    if isinstance(expression, int):
        print("%s %d" % (' ' * depth, expression))
    elif isinstance(expression, bool):
        print("%s %s" % (' ' * depth, bool(expression)))
    else:
        print("%s(%s " % (' ' * depth, expression[0]))
        for i in range(1, NumberOfArguments[expression[0]]+1):
            prettyPrintExp(expression[i], depth+2)
        print("%s) " % (' ' * (depth+1)))
        
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

# Reads file are parses, prints to error or prettyprintcorrect
def readFile(fileName):
    fil = open(PATH + fileName)
    fileLines = fil.readlines()
    index = 0
    for f in fileLines:
        try: 
            prettyPrint(parse(f), index, 0)
        except Exception as error:
            errorPrint(error, index)
        index +=1
### prettyPrint an expression (parsed list of tokens)
def prettyPrint(expression, index, depth = 0):
    # takes a parse tree and prints it out to prettyPrintCorrect.txt
    with open(PATH + 'prettyPrintCorrect.txt', 'a') as file: 
        if depth == 0:
            file.write("Index: %d" % (index) + "\n")
            file.flush()
        if isinstance(expression, int):
            file.write("%s %d" % (' ' * depth, expression) + "\n")
            file.flush()
        else:
            file.write("%s(%s " % (' ' * depth, expression[0]) + "\n")
            file.flush()
            prettyPrint(expression[1], index, depth+2)
            prettyPrint(expression[2], index, depth+2)
            file.write("%s) " % (' ' * (depth+1)) + "\n")
            file.flush()
# Prints exceptions to error.txt
def errorPrint(expression, index):
    # takes an error and prints to error.txt
    with open(PATH + 'error.txt', 'a') as file:  
        file.write("Index: %d" % (index) + "\n" + "Parse error: %s" % (expression) + "\n")
        

# # 3) run your parser over the two attached files, one containing 
# valid expressions, the other expressions with syntax errors. 

# readFile('correctSyntax.txt')
# prg = generateRandomProgram(1) 
# print(prg)
# prettyPrintExp(parse(prg)) 
# testEvaluator()

                                