# Laryssa Revelli
# A01979841
from random import random, randint
### TODO ##### 
# 1) False, True print 1
# 2) KeyError: '>' in createParseTree line 147
import os
PATH = "C:/Users/lreesa/cs4700/Assn5n6/"
if not os.path.exists(PATH):
    os.makedirs(PATH)

########## 1) BNF Grammar ############################################################
# <expression> := <booleanExpression> | <numberExpression> 
#                 | '(' 'if' <booleanExpression> <expression> <expression> ')'
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
OperatorsAll = ['+', '-', '*', '/', 'if', 'and', 'or', 'not', '>', 'eq' ]
OperatorsBoolBool = ['and', 'or', 'not', 'eq']
OperatorsBoolNumb = ['>', 'eq']
OperatorsNumb = ['+', '-', '*', '/']
NumberOfArguments = {}
ArgumentCount = [(1, ['not']),(2, ['+', '-', '*', '/', 'and', 'or', 'eq']), (3, ['if'])]
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
# (extend the one that works with parse trees)
def atom(token):
    # changes a token to an actual integer or boolean
    if token.isdigit():
        return int(token)
    if token == 'True' or token == 'False':
        return bool(token) 
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
        
        ### prettyPrint an expression (parsed list of tokens)

# takes a parse tree and prints it out so it is easier to read (maybe)
def prettyPrintExp(expression, depth = 0):
    if isinstance(expression, int):
        print("%s %d" % (' ' * depth, expression))
    # elif isinstance(expression, bool):
    #     print("%s %s" % (' ' * depth, expression))
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
                           or token in OperatorsAll + [')', '('])

# Reads file are parses, prints to error or prettyprintcorrect
def readFile(fileName):
    fil = open(PATH + fileName)
    fileLines = fil.readlines()
    for f in fileLines:
        parseTree = parseX(f)
        if None not in parseTree:
            prettyPrint(parseTree, f)
        else:
            errorPrint(parseTree, f)

# Prints exceptions to error.txt
def errorPrint(expression, depth):
    # takes a tokenized string expression and prints it out based on depth
    token = expression.pop(0)     

# # 3) run your parser over the two attached files, one containing 
# valid expressions, the other expressions with syntax errors. 

# readFile('correctSyntax.txt')
prg = generateRandomProgram(2) 
print(prg)
prettyPrintExp(parse(prg))                
                                