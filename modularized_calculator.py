#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_function(line, index): 
    function_name = ""
    name_to_func = {
        'abs': abs, 
        'int': int,
        'round': round,
    }
    while index < len(line) and line[index].isalpha():
        function_name += line[index]
        index += 1
    assert(function_name in name_to_func.keys())
    token = {'type': 'FUNCTION', 'function': name_to_func[function_name]}
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line, index): 
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_divide(line, index): 
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_left_parentheses(line, index): 
    token = {'type': 'LEFT'}
    return token, index + 1

def read_right_parentheses(line, index): 
    token = {'type': 'RIGHT'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit() or line[index] == '.':
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parentheses(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parentheses(line, index)
        elif line[index].isalpha(): 
            (token, index) = read_function(line, index)
        elif line[index].isspace(): 
            index += 1
            continue
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def has_parentheses(tokens): 
    return any((token['type'] == 'LEFT' or token['type'] == 'RIGHT') for token in tokens)

def has_functions(tokens): 
    return any(token['type'] == 'FUNCTION' for token in tokens)

def process_parentheses(tokens):
    index = 1 # starts with 1 since the input tokens has inserted the dummy PLUS sign
    left_index = -1 # stores the innermost left index, updated whenever LEFT is found in traversing
    temp_tokens = [{'type': 'PLUS'}]
    while index < len(tokens): 
        if tokens[index]['type'] == 'LEFT': # start of a parenthesis pair
            left_index = index
        elif tokens[index]['type'] == 'RIGHT': 
            if left_index != -1:  # ensure current parentheses pair is kept track of [avoid triggering (1+2*(3+4))]
                curr_paren_tokens = tokens[left_index + 1 : index]
                temp_tokens.append({'type': 'NUMBER', 'number': evaluate(curr_paren_tokens, isInternalCall = True)})
                left_index = -1
                index += 1
                continue
        if left_index == -1: 
            temp_tokens.append(tokens[index])
        index += 1
    return temp_tokens

def process_functions(tokens): 
    index = 1
    temp_tokens = [{'type': 'PLUS'}]
    while index < len(tokens) - 1: 
        if tokens[index]['type'] == 'FUNCTION': 
            assert(tokens[index + 1]['type'] == 'NUMBER') # any calculations including MINUS signs were processed in process_parentheses()
            answer = tokens[index]['function'](tokens[index + 1]['number']) # apply function to the number following
            temp_tokens.append({'type': 'NUMBER', 'number': answer})
            index += 1
        else: 
            temp_tokens.append(tokens[index])
            index += 1
    return temp_tokens


#
# Returns final answer given parsed tokens
#
def evaluate(tokens, isInternalCall = False):
    if not isInternalCall: # does not insert extra dummy if it was a call from process_parentheses
        tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    while has_parentheses(tokens):
        tokens = process_parentheses(tokens) # replace parentheses in tokens by their calculation results
    while has_functions(tokens):
        tokens = process_functions(tokens)
    return calculate(tokens) # find result after all parentheses were removed

#
# Returns a float result given tokens without parentheses
#
def calculate(tokens):
    answer = 0.0
    index = 1
    temp_tokens = [{'type': 'PLUS'}]
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            temp_tokens.append(tokens[index])
            index += 1
        elif tokens[index]['type'] == 'MULTIPLY':
            num = temp_tokens[-1]['number'] * tokens[index + 1]['number']
            temp_tokens[-1] = {'type': 'NUMBER', 'number': num}
            index += 2
        elif tokens[index]['type'] == 'DIVIDE':
            num = temp_tokens[-1]['number'] / tokens[index + 1]['number']
            temp_tokens[-1] = {'type': 'NUMBER', 'number': num}
            index += 2
        else: 
            temp_tokens.append(tokens[index])
            index += 1
    index = 1
    tokens = temp_tokens
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    #test("1+2")
    #test("1.0+2.1-3")
    #test("-12+4-7+.5")
    #test("(1+2*(-4*(-3)+4))")
    #test("(1-3-.4/2+(8-.5))")
    #test("round(-1.55)")
    #test("abs(int(-2.3 + 4))")
    test("12 + abs(int(round(-1.55) + abs(int(-2.3 + 4))))")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
