from random import random, randint
from evaluator import evaluate
Operators = ['+', '-', '*', '/']

def parse(tokenList, depth):
    # takes a tokenized string expression and parses it into parse trees
    token = tokenList.pop(0)
    if isinstance(token, int):
        return token
    else:
        try:
            if token != '(': #check for parenthesis in correct order
                raise ValueError('Missing open parenthesis')
            parseTree = [tokenList.pop(0), 
                    parse(tokenList, depth+1),
                    parse(tokenList, depth+1)]
            paren = tokenList.pop(0)
            if paren != ')': #check for parenthesis in correct order
                raise ValueError('Missing open parenthesis')
            return parseTree
        except ValueError:
            print('Syntax error.')

def generateRandomExpression(maxDepth = 1):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateRandomExpression(maxDepth - 1), 
                                generateRandomExpression(maxDepth - 1))

def tokenize(chars):
    # takes a string representing an expression in simple lisp and returns a list of tokens
    tokens = chars.replace('(', ' ( ').replace(')', ' ) ').split()
    #Simple Error checking
    for i in range(len(tokens)):
        tokens[i] = atom(tokens[i])
        if (tokens[i] != '(' and tokens[i] != ')' 
                and isinstance(tokens[i], int) == False  
                and  tokens[i] not in Operators):
            #raise RuntimeError('Invalid expression')
            print('Invalid Expression: ' + chars)
            return
        else:
            return tokens
    
def atom(token):
    # changes a token to an actual integer 
    if token.isdigit():
        return int(token)
    return token

def readFile(fileName):
    fil = open('correctSyntax.txt')
    fileLines = fil.readlines()
    for f in fileLines:
        parseTree = parse(tokenize(f), 0)
        if None not in parseTree:
            prettyPrint(parseTree, f)
        else:
            errorPrint(parseTree, f)

def prettyPrint(expression, depth):
    # takes a tokenized string expression and prints it out based on depth
    token = expression.pop(0)
    if isinstance(token, int):
        print("%s%d" % (' ' * depth, token))
    else:
        operator = expression.pop(0)
        print("%s(%s" % (' ' * depth, operator))
        prettyPrint(expression, depth+1)
        prettyPrint(expression, depth+1)
        expression.pop(0)
        print("%s)" % (' ' * depth,))

def errorPrint(expression, depth):
    # takes a tokenized string expression and prints it out based on depth
    token = expression.pop(0)
    

if __name__ == '__main__':
    exp = generateRandomExpression()
    tokenList = tokenize(exp)
    parseTree = parse(tokenList, 0)
    print(parseTree)