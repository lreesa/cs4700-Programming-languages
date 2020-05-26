from random import random, uniform, randint, choice
import string
from syntax import *
#from semantics import *
from semantics import *

import os
PATH = "C:/Users/lreesa/cs4700/Final/"
#C:\Users\nickf\Dropbox\Classes\CS4700 Spring 2020\lisp interpreter
if not os.path.exists(PATH):
    os.makedirs(PATH)
    
 
def runProgram(fileName, trace = False):
    #reads the code in file name, parses it, check each statememt, executes each statement
    global Trace
    Trace = trace
    # read in the grammar as a tree
    grammar = parseGrammar(PATH)
    # read in the program file as a single string
    program = readInFile(fileName)
    # parse the string into a list of lists
    codeList = parseProgram(program)
    # run each parsed statement through a syntax check
    for code in codeList:
        if checkSyntax(code, '<statement>', grammar):
            print("Syntax error?")
    # evaluate each statement in the program
    evalProgram(codeList, trace = trace)
    
def readInFile(fileName):
    #reads in a eL program, returns as one big string
    print("Reading %s" % (PATH + fileName,))
    with open(PATH + fileName, 'r') as file:  # Use file to refer to the file object
        lines = [l for l in file.readlines() if not l[0] == '#']
    whole = ""
    for line in lines:
        whole = whole + line
    return whole

fileName = "code.el"
#print(readInProgram(fileName))
runProgram(fileName, True)
