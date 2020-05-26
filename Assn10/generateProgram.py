from random import random, randint, choice
import string
#from newCode import createParseTree, evaluate

import os
PATH = "C:/Users/lreesa/cs4700/Assn10/"
if not os.path.exists(PATH):
    os.makedirs(PATH)
    
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

def generateProgram(lhs, grammar, depth = 0):
    #print(lhs)
    #print(depth)
    if not lhs[0] == '<': #a terminal
        return lhs
    if lhs == '<number>':
        return str(randint(-500, +500))
    if lhs == '<variable>':
        return randomString(5)
    # randomly pick one of the alternative rhs
    #print(grammar[lhs])
    if depth > 10:
        pick = 0
    else:
        pick = randint(0, len(grammar[lhs])-1)
    rhs = grammar[lhs][pick]
    if isinstance(rhs, list):
        return ' '.join([generateProgram(subPhrase, grammar, depth+1) for subPhrase in rhs])
    return generateProgram(rhs, grammar, depth+1)
    
def randomString(length):
    return ''.join(choice(string.ascii_letters) for m in range(length))
    
grammar = parseGrammar()
#print(generateProgram('<booleanExpression>', grammar))
print(generateProgram('<dataExpression>', grammar))
print(generateProgram('<list>', grammar))    
print(generateProgram('<program>', grammar))
    
    