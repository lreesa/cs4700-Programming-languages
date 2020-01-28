# Laryssa Revelli
# A01979841
# Assignment 3 Part 1

from random import random, randint

########## 1) BNF Grammar ##########
# <expression> := <integer> | '(' <operator> <expression> <expression> ')'
# <operator> := '+' | '-' | '*' | '/'
Operators = ['+', '-', '*', '/']

def generateRandomExpression(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateRandomExpression(maxDepth - 1), 
                                generateRandomExpression(maxDepth - 1))
                
########## 2) Lexical Analysis ##########
# A: Tokenizer cannot detect mismatched parenthesis, or invalid expressions 
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

########## 3) Pretty Printer (Not functioning properly still) ##########
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

### prettyPrint a list of tokens
def prettyPrint(tokenList, depth = 0):
    token = tokenList.pop(0)
    # atom, just print at depth and return
    if isinstance(token, int):
        print("%s%d" % (' ' * depth, token))
    else:
        # compound expression
        operator = tokenList.pop(0)
        print("%s(%s" % (' ' * depth, operator))
        prettyPrint(tokenList, depth+1)
        prettyPrint(tokenList, depth+1)
        tokenList.pop(0) # remove )
        print("%s)" % (' ' * depth,))
    
########## 4) Balance Parenthesis checker ##########
def checkParenthesis(chars, depth):
    # Base case: empty list
    if not chars:
        return depth == 0

    elif chars[0] == '(':
        depth += 1 
    elif chars[0] == ')':
        depth -= 1 
    return checkParenthesis(chars[1 :], depth)

if __name__ == '__main__':
    # Check Mismatched Parenthesis: 
    print(checkParenthesis(tokenize('(+ 2 5))'), 0))
    # Check Matched Parenthesis: 
    print(checkParenthesis(tokenize('(+ 2 (- 3 5))'), 0))

    #Test Case 0: Integer expression
    validInt = '111'
    token0 = tokenize(validInt)
    #print(token0)
    prettyPrint(token0, 0)
    # Test Case 1: Invalid operator
    invalidOp = '(! 2 3)'
    token1 = tokenize(invalidOp)
    #print(token1)
    prettyPrint(token1, 0)
    # Test Case 2: Invalid parenthesis
    invalidPar = '[+ 4 2]'
    token2 = tokenize(invalidPar)
   # print(token2)
    prettyPrint(token2, 0)
    # Test Case 3: Invalid expression (number)
    invalidEx = '0.224'
    token3 = tokenize(invalidEx)
    print(token3)
    prettyPrint(token3, 0)
    # Test Case 4: Valid whitespace expression
    validWS = '(    / 4   2             )'
    token4 = tokenize(validWS)
    print(token4)
    prettyPrint(token4, 0)
    # Test Case 5: Valid expression- no whitespace.
    validNoWS = '(-(+2(*3 4))5)'
    token5 = tokenize(validNoWS)
    print(token5)
    prettyPrint(token5, 0)
    
