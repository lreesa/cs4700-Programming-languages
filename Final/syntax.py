def parseProgram(programString):
    #takes a string that represents a program, multiple statements
    #returns a list of list of tokens, each a statement
    tokens = spaceOut(programString).split()
    codeList = []
    while not tokens == []:
        code = createCode(tokens)
        codeList.append(code)
    return codeList
    
def parseRules(ruleString):
    #takes a string representing a list or rules, each rule is
    #<statement> ==> <statement>
    tokens = spaceOut(ruleString).replace('==>', '  ').split()
    ruleList = []
    while not tokens == []:
        lhs = createCode(tokens)
        rhs = createCode
        ruleList.append((lhs, rhs))
    return ruleList
   
def spaceOut(string):
    return string.replace('(', ' ( ').replace(')', ' ) ')
    
def createCode(tokenList):
    # takes a token list and returns a parse tree
    token = tokenList.pop(0) #pop off ( or atom
    if token.isdigit() or token[0].isdigit(): #integer
        return int(token)
    if isinstance(token, str) and not token == '(': #atom
        return token
    args = []
    while not tokenList[0] == ')':
        args.append(createCode(tokenList))
    tokenList.pop(0) # pop the ')'
    return args
    
def checkSyntax(code, grammarWord, grammar):
    # traverses the grammar tree and code tree
    # explores alternative rhs for each rule
    if isinstance(code, int): #should be an int
        return grammarWord == '<number>'
    if isinstance(code, str): # could be any non-int atom
        return (grammarWord == code) or grammarWord == '<string>' 
    oneTrue = True #only one rhs has to be true
    for oneRHS in grammar[grammarWord]: #for all possible rhs
        # example <builtInExpression> | <userFunctionCall> 
        if not len(code) == len(oneRHS): # not the same length
            continue
        allTrue = True # all of this rhs has to be correct
        for i in range(0, len(oneRHS)): #try each word in the rhs
            # example (def <variable> (<parameterList>) <body>)
            allTrue = allTrue and checkSyntax(code[i], oneRHS[i], grammar)
        oneTrue = allTrue or oneTrue #update for all rhs
        if oneTrue: #found one that works
            return True
    return False

def readInGrammar(PATH):
    with open(PATH + 'eLgrammarDefinition.txt', 'r') as file:  # Use file to refer to the file object
        return file.readlines()
        
def parseGrammar(PATH):
    grammar = {}
    for line in readInGrammar(PATH):
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