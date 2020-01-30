from random import random, randint
import os
PATH = "C:/Users/lreesa/cs4700/LispLang/"
if not os.path.exists(PATH):
    os.makedirs(PATH)

# define all the possible operators and how many arguments they take
Operators = ['+', '-', '*', '/', 'if', 'and', 'or', 'not', '>', 'eq' ]
NumberOfArguments = {}
ArgumentCount = [(1, ['not']),(2, ['+', '-', '*', '/', 'and', 'or', 'eq']), (3, ['if'])]
# fill the mapping from operator to argument count
for (count, operators) in ArgumentCount:
    for op in operators:
        NumberOfArguments[op] = count

def generateRandomExpression(maxDepth = 1):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateRandomExpression(maxDepth - 1), 
                                generateRandomExpression(maxDepth - 1))

def atom(token):
    # changes a token to an actual integer 
    if token.isdigit():
        return int(token)
    return token
                
BadOps = ['_', '=','(','%']
BadNumbers = ['1.2344','x','y']
def generateBadRandomExpression(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    if random() < 0.05 or maxDepth < 0:
        return str(BadNumbers[randint(0, len(BadNumbers)-1)])
    elif random() < 0.05:
        return "(%s %s %s" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
    elif random() < 0.05:
        return "%s %s %s)" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
                        
def createParseTree(tokenList):
    # takes a tokenized string expression and parses it into parse trees
    token = tokenList.pop(0)
    if isinstance(token, int):
        return token
    else:
        if token != '(': #check for parenthesis in correct order
            raise Exception('Missing open parenthesis')
        operator = tokenList.pop(0)
        if operator in Operators:
            # try:
            parseTree = [operator, 
                createParseTree(tokenList), 
                createParseTree(tokenList)]
        else:
            raise Exception('Missing Operator')

        paren = tokenList.pop(0)
        if paren != ')': #check for parenthesis in correct order
            raise Exception('Missing close parenthesis')
        return parseTree        

### takes a program string and returns a parse tree
def parse(programStr, debug = False):
    # returns the input string as a parse tree, represented as either an int or a list of expressions
    return createParseTree(tokenize(programStr))#, debug)
                          
### prettyPrint an expression (parsed list of tokens)
def prettyPrintExp(expression, index, depth = 0):
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
            prettyPrintExp(expression[1], index, depth+2)
            prettyPrintExp(expression[2], index, depth+2)
            file.write("%s) " % (' ' * (depth+1)) + "\n")
            file.flush()
        
        
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
    if checkBalanced(tokens.copy()) == False:
        raise Exception("Unbalanced parenthesis")
    if all(legalToken(token) for token in tokens):
        return [atom(token) for token in tokens]
    else:
        badTokens = str([token for token in tokens if not legalToken(token)])[1:][:-1]
        raise Exception("Unknown token found %s" % (badTokens,))
  
### returns True if the token is legal      
def legalToken(token):
    # returns True if legal for our simple lisp
    return token.isdigit() or token in Operators + [')', '(']

def readFile(fileName):
    fil = open(PATH + fileName)
    fileLines = fil.readlines()
    index = 0
    for f in fileLines:
        try: 
            prettyPrintExp(parse(f), index, 0)
        except Exception as error:
            errorPrint(error, index)
        index +=1

def errorPrint(error, index):
    # takes an error and prints to error.txt
    with open(PATH + 'error.txt', 'a') as file:  
        file.write("Index: %d" % (index) + "\n" + "Parse error: %s" % (error,) + "\n")
    

if __name__ == '__main__':
    # readFile('correctSyntax.txt')
    # readFile('errorSyntax.txt')

