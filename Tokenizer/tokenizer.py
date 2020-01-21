# Laryssa Revelli
# A01979841
# Assignment 3 Part 1

import Random

########## BNF Grammar ##########
Operators = ['+', '-', '*', '/']

def generateRandomExpression(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateRandomExpression(maxDepth - 1), 
                                generateRandomExpression(maxDepth - 1))
                
            
def tokenize(chars):
    # takes a string representing an expression in simple lisp and returns a list of tokens
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()
    
    
def atom(token):
    # changes a token to an actual integer 
    if token.isdigit():
        return int(token)
    return token

def prettyPrint(chars):

    pass

if __name__ == '__main__':
##### Note: Tokenizer cannot detect mismatched parenthesis, or invalid expressions #####
    # Test Case 1: Invalid operator

    # Test Case 2: Invalid parenthesis

    # Test Case 3: Invalid expression

    # Test Case 4: Valid whitespace expression

    # Test Case 5: Valid expression- no whitespace.
    
    pass
