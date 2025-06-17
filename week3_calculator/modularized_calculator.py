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
    # find the innermost parentheses
    left_index = -1
    right_index = -1
    for i in range(len(tokens)): 
        if tokens[i]['type'] == 'LEFT':
            left_index = i
    for i in range(left_index, len(tokens)):
        if tokens[i]['type'] == 'RIGHT' and right_index == -1: 
            right_index = i

    assert(left_index != -1 and right_index != 1)

    # Extract the tokens inside this innermost parenthesis pair
    # Note: we pass isInternalCall=True to prevent the inner evaluate from adding its own dummy '+'
    inner_expression_tokens = tokens[left_index + 1 : right_index]
    
    # Evaluate the inner expression recursively
    evaluated_value = evaluate(inner_expression_tokens, isInternalCall=True)

    # Create a new list of tokens, replacing the `(...)` block with the evaluated number
    new_tokens = (
        tokens[:left_index] +  # Tokens before the current '('
        [{'type': 'NUMBER', 'number': evaluated_value}] + # The result
        tokens[right_index + 1:] # Tokens after the current ')'
    )
    
    return new_tokens

def process_functions(tokens):
    # Process functions from right to left to handle nested functions correctly
    i = len(tokens) - 1
    while i >= 0:
        if tokens[i]['type'] == 'FUNCTION':
            # Check if we have an argument after the function
            if i + 1 >= len(tokens):
                print(f"Error: Function '{tokens[i]['function'].__name__}' missing argument")
                exit(1)
            
            # Get the argument value
            if tokens[i + 1]['type'] != 'NUMBER':
                print(f"Error: Function '{tokens[i]['function'].__name__}' expects a number argument")
                exit(1)
            
            # Apply the function to the argument
            func = tokens[i]['function']
            arg_value = tokens[i + 1]['number']
            result = func(arg_value)
            
            # Replace the function and its argument with the result
            tokens[i] = {'type': 'NUMBER', 'number': result}
            tokens.pop(i + 1)  # Remove the argument token
            
        i -= 1
    
    return tokens

# Returns final answer given parsed tokens
def evaluate(tokens_original, isInternalCall=False):
    tokens = list(tokens_original) # Work on a copy to avoid modifying original list in recursive calls
    # Insert a dummy '+' token only when evaluate is not recursively called from process_parentheses()
    if not isInternalCall:
        if not tokens: 
            return 0.0
        tokens.insert(0, {'type': 'PLUS'})

    # Loop until the expression is fully evaluated to a single number
    while has_parentheses(tokens):
        tokens = process_parentheses(tokens)
    while has_functions(tokens):
        tokens = process_functions(tokens)
    assert(len(tokens) > 0) 
    return calculate(tokens)


# Returns a float result given tokens without parentheses or functions
def calculate(tokens):
    answer = 0.0
    index = 1
    
    # First pass: Handle multiplications and divisions
    temp_tokens = []
    if tokens and tokens[0]['type'] == 'NUMBER':
         temp_tokens.append({'type': 'PLUS'}) # if expression starts with a number, add a dummy plus
    temp_tokens.append(tokens[0])

    while index < len(tokens) - 1:
        if tokens[index]['type'] == 'NUMBER':
            temp_tokens.append(tokens[index])
        elif tokens[index]['type'] == 'MULTIPLY':
            assert(temp_tokens[-1]['type'] == 'NUMBER') # make sure the preceding element in temp tokens is number
            assert(tokens[index + 1]['type'] == 'NUMBER') # make sure the next token is number
            num = temp_tokens.pop()['number'] * tokens[index + 1]['number']
            temp_tokens.append({'type': 'NUMBER', 'number': num})
            index += 1 
        elif tokens[index]['type'] == 'DIVIDE':
            assert(temp_tokens[-1]['type'] == 'NUMBER') # make sure the preceding element in temp tokens is number
            assert(tokens[index + 1]['type'] == 'NUMBER') # make sure the next token is number
            num = temp_tokens.pop()['number'] / tokens[index + 1]['number']
            temp_tokens.append({'type': 'NUMBER', 'number': num})
            index += 1 
        else: # PLUS or MINUS signs are simply added for next pass
            temp_tokens.append(tokens[index])
        index += 1

    # Second pass: Handle additions and subtractions
    # The first token in temp_tokens after multiply and divisions is either dummy PLUS or original operator
    assert(temp_tokens[0]['type'] in ['PLUS', 'MINUS'])
        
    answer = 0.0
    for i in range(1, len(temp_tokens)):
        token = temp_tokens[i]
        if token['type'] == 'NUMBER':
            if temp_tokens[i - 1]['type'] == 'PLUS':
                answer += token['number']
            elif temp_tokens[i - 1]['type'] == 'MINUS':
                answer -= token['number']
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

    test("12 + abs(int(round(-1.55) + abs(int(-2.3 + 4))))")
    test("abs(-5)")
    test("int(3.9)")
    test("round(3.4)")
    test("round(3.6)")
    test("round(3.5)") # Test rounding half
    test("abs(5-10)") # Test abs with an expression inside
    test("int(9.999999999)")
    test("abs(round(-0.5))") # round(-0.5) is -0, abs(-0) is 0


    test("1+2")
    test("1.0+2.1-3")
    test("-12+4-7+.5")
    test("1+2*3")
    test("10/2-1")
    test("(-3+2)")
    test("(3)")
    test("(1+2*(-4*(-3)+4))") # Test nested parentheses and negative numbers
    test("(1-3-.4/2+(8-.5))")
    test("round(-1.55)")
    test("abs(int(-2.3 + 4))")

    print("==== Test finished! ====\n")

run_test()

while False:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
