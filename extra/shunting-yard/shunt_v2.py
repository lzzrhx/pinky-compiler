################################################################################
# A simple shunting yard implementation
################################################################################

input = "3 + 4 * ( 2 - 1 ) * 6 + 8"
print(f'INPUT: {input}')

precedence = {
    '*': 3,
    '/': 3,
    '+': 2,
    '-': 2
}


################################################################################
# Perform Shunting-Yard algorithm
################################################################################
output = [] # Input in Reverse Polish Notation (RPN)
opstack = [] # Operator stack

for token in input.strip().split():
    if token == '(':
        opstack.append(token)
    elif token == ')':
        while len(opstack) > 0:
            op = opstack.pop()
            if op == '(':
                break
            output.append(op)
    else:
        if token in precedence:
            while len(opstack) > 0:
                op = opstack[-1] # Get the operator from the top of the opstack
                if op == '(' or precedence[token] > precedence[op]:
                    break
                opstack.pop()
                output.append(op)
            opstack.append(token)
        else:
            output.append(token) # Push numbers directly to the output

# Push the remaining operators from the opstack into the output
while len(opstack) > 0:
    output.append(opstack.pop())

print(f'POSTFIX (RPN): {output}')


################################################################################
# Evaluate a list of elements (in postfix notation / RPN form)
################################################################################
result = []
for elem in output:
    if elem not in precedence:
        result.append(float(elem))
    else:
        right = result.pop()
        left = result.pop()
        if elem == '+':
            result.append(left + right)
        elif elem == '-':
            result.append(left - right)
        elif elem == '*':
            result.append(left * right)
        elif elem == '/':
            result.append(left / right)

print(f'RESULT: {result}')
