# Laryssa Revelli
# A01979841

########## 1) BNF Grammar ##########
# <expression> := <booleanExpression> | <numberExpression> 
#                 | '(' 'if' <booleanExpression> <expression> <expression> ')'
# <booleanExpression> ::= '(' 'not' <booleanExpression> ')'
#                 | '(' <booleanOperator> <booleanExpression> <booleanExpression> ')'
#                 | '(' '>' <numberExpression> <numberExpression> ')'
#                 | '(' 'eq' <expression> <expression> ')'
# <numberExpression> ::= <integer> | '(' <operator> <expression> <expression> ')' 

# <operator> := '+' | '-' | '*' | '/'
# <booleanOperator> := 'and' | 'or' # 'not' is accounted for in booleanExpression

# <booleanConstants> := 'True' | 'False'


def evaluate(parseTree):
    if isinstance(parseTree, int):
        return parseTree
    operator = parseTree[0]
    if operator == '+':
        return evaluate(parseTree[1]) + evaluate(parseTree[2])
    if operator == '-':
        return evaluate(parseTree[1]) - evaluate(parseTree[2])
    if operator == '*':
        return evaluate(parseTree[1]) * evaluate(parseTree[2])
    if operator == '/':
        return evaluate(parseTree[1]) / evaluate(parseTree[2])
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
            return  evaluate(parseTree[2]) and evaluate(parseTree[3])
    

def quote(parseTree):
    return parseTree

def testEvaluator(parseTree):
    # tests the evaluator by looping over 1000 random legal expressions 
    # and evaluating the expression and printing the result.
    #  Manually verify the system is working by starting with 
    # very simple expressions (depth = 1)
    pass