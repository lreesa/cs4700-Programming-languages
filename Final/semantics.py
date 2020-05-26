   
def evalProgram(codeList, trace = False):
    # top call, evaluates a list of parsed statements
    global Trace
    Trace = trace
    return evalElBlock(codeList, {}, [])
    
def evalEl(code, bindings = [], depth = 0):
    # evaluates the code with the bindings so far
    # bindings is a list of dictionaries, each with a mapping from a symbol
    # to its value. These are generated from set or def statements, and when
    # a user-defined function is called
    if Trace or depth == 0:
        print("%sEval %s" % ("|  "*depth, str(code)))
    answer = evalElHelp(code, bindings, depth)
    if Trace or depth == 0:
        print("%sAns  %s " % ("|  "*depth, str(answer)))
    return answer
     
def evalElHelp(code, bindings, depth):
    # do all atoms
    if isinstance(code, int):
        return code
    if "True" == code:
        return True
    if "False" == code:
        return False
    if "nil" == code: #nil is the empty list
        return []
    if isinstance(code, str): # variable
        return findValue(code, bindings, depth)
    # do all composite code
    fun = code[0]
    #numerical functions
    if fun == '+':
        return evalEl(code[1], bindings, depth +1) + evalEl(code[2], bindings, depth +1)
    if fun == '-':
        return evalEl(code[1], bindings, depth +1) - evalEl(code[2], bindings, depth +1)    
    if fun == '*':
        return evalEl(code[1], bindings, depth +1) * evalEl(code[2], bindings, depth +1)    
    if fun == '/':
        return evalEl(code[1], bindings, depth +1) / evalEl(code[2], bindings, depth +1)
    # control functions
    if fun == 'if':
        if evalEl(code[1], bindings, depth +1):
            return evalEl(code[2], bindings, depth +1)
        else:
            return evalEl(code[3], bindings, depth +1)
    # boolean functions
    if fun == 'not':
        return not evalEl(code[1], bindings, depth +1)
    if fun == 'and':
        return evalEl(code[1], bindings, depth +1) and evalEl(code[2], bindings, depth +1)
    if fun == 'or':
        return evalEl(code[1], bindings, depth +1) or evalEl(code[2], bindings, depth +1)
    if fun == 'eq': #only works between atoms
        return simpleEqual(evalEl(code[1], bindings, depth +1), evalEl(code[2], bindings, depth +1))
    if fun == '<':
        return evalEl(code[1], bindings, depth +1) < evalEl(code[2], bindings, depth +1)
    if fun == 'atom':
        ans = evalEl(code[1], bindings, depth +1)
        return isinstance(ans, int) or isinstance(ans, str) or ans == True or ans == False or ans == []
    # data structures
    if fun == 'cons': #add the first to a list
        return [evalEl(code[1], bindings, depth +1)] + evalEl(code[2], bindings, depth +1)
    if fun == 'first': #eval then return the first
        return evalEl(code[1], bindings, depth +1)[0]
    if fun == 'rest': #eval then return the rest
         return evalEl(code[1], bindings, depth +1)[1:]
    # evaluation
    if fun == 'quote': #stop evaluation
         return code[1]
    if fun == 'evalEl': #evaluate to get the code, then evaluate the code
         return evalEl(evalEl(code[1], bindings, depth +1))   
     #must be a user function call
    return evalElFun(code[0], code[1:], bindings, depth +1)
    
def simpleEqual(a, b):
    # only works on primitives
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    if (a is True and b is True) or (a is False and b is False):
        return True
    if (a == []) and (b == []):
        return True
    return False

def evalElFun(funName, args, bindings, depth):
    #Execute a user defined function
    if Trace:
        print("|  "*depth + "Calling function %s" % (funName,))
    #lookup the function definition in bindings
    (params, block) = findValue(funName, bindings, depth)
    #create a new binding to hold local variables from parmeters, sets and defs
    oneBinding = {} 
    # add the mapping from parameter names to values
    for (oneParam, oneExpression) in zip(params, args):
        value = evalEl(oneExpression, bindings, depth +1)
        #Check for function param
        # if len(oneParam) > 1: 
        #     raise Exception('Cannot pass function as parameter')
        oneBinding[oneParam] = value
        if Trace:
            print("|  "*depth + "Create parameter-value binding: %s = %s" % (oneParam, value))
    # work through each statement in block
    return evalElBlock(block, oneBinding, bindings, depth = depth +1)
    
def evalElBlock(block, oneBinding, bindings, depth = 0):
    # walks down the block evaluating each statement and accumulating bindings
    # into this oneBinding for this block
    if len(block) == 0: #empty block, return None
        return 
    else:
        code = block[0]
        if code[0] == 'set':
            # map the name of the variable to the eval of value
            if Trace:
                print("|  "*depth + "Evaluating set %s = %s" % (code[1], str(code[2])))
            value = evalEl(code[2], [oneBinding] + bindings, depth +1)
            oneBinding[code[1]] = value
            if Trace:
                print("|  "*depth + "Create set variable binding: %s = %s" % (code[1], value))
            # keep going through the block
            return evalElBlock(block[1:], oneBinding, bindings, depth = depth)
            
        elif code[0] == 'def': #put mapping from name to arguments, block
            oneBinding[code[1]] = (code[2], code[3:])
            if Trace:
                print("|  "*depth + "Create function binding: %s = [%s, %s]" % (code[1], str(code[2]), str(code[3:])))
            # keep working through block
            return evalElBlock(block[1:], oneBinding, bindings, depth = depth)
            
        else: #found an expression, evaluate it with current bindings
            ans = evalEl(block[0], [oneBinding] + bindings, depth)
            # if last expression then return the answer
            if block[1:] == []:
                return ans
            else: #keep going through the block
                return evalElBlock(block[1:], oneBinding, bindings, depth = depth)
    
def findValue(name, bindings, depth):
    # name is a variable, bindings is a list of dictionaries ordered most
    # recent first, search up the bindings seeing if this variable is in
    # one of the dictionaries
    if bindings == []: #have not found the value
        print("NO Value %s" % name)
    if name in bindings[0]: #found its value
        if Trace:
            print("|  "*depth + "Found Value of %s as %s" % (name, bindings[0][name]))
        return bindings[0][name]
    if Trace:
        print("|  "*depth + "Looking for %s" % (name,))
    # If this is reached, moving up a dictionary means non local variable 
    # print('Error: non-local variable referenced')
    return findValue(name, bindings[1:],depth)
    

def toString(code):
    # prints the parse tree in a more readable form
    if isinstance(code, int) or isinstance(code, str) or len(code) == 0:
        return str(code) + " "
    string = "("
    for item in code:
        string = string + toString(item)
    return string + ')'
