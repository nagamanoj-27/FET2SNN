def check_js(f):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        stack = []
        mismatches = 0
        in_single_comment = False
        in_multi_comment = False
        in_string = None
        escaped = False
        
        for i, char in enumerate(content):
            if escaped:
                escaped = False
                continue
            if in_single_comment:
                if char == '\n':
                    in_single_comment = False
                continue
            if in_multi_comment:
                if char == '/' and i > 0 and content[i-1] == '*':
                    in_multi_comment = False
                continue
            if in_string:
                if char == '\\':
                    escaped = True
                elif char == in_string:
                    in_string = None
                continue
            if char == '/' and i + 1 < len(content):
                next_char = content[i+1]
                if next_char == '/':
                    in_single_comment = True
                    continue
                elif next_char == '*':
                    in_multi_comment = True
                    continue
            if char in ["'", '"', '`']:
                in_string = char
                continue
            if char in ['(', '{', '[']:
                stack.append(char)
            elif char in [')', '}', ']']:
                if not stack:
                    mismatches += 1
                else:
                    top_char = stack.pop()
                    matches = (
                        (top_char == '(' and char == ')') or
                        (top_char == '{' and char == '}') or
                        (top_char == '[' and char == ']')
                    )
                    if not matches:
                        mismatches += 1
        
        if len(stack) > 0 or mismatches > 0:
            print(f"File {f} has {len(stack)} unclosed brackets and {mismatches} mismatches!")
        else:
            print(f"File {f} is clean.")
    except Exception as e:
        print(f"Error checking {f}: {e}")

for f in ["lif-neuron.js", "snn-simulator.js", "snn-aging.js", "snn-tornado.js", "snn-monte-carlo.js", "snn-validation.js"]:
    check_js(f)
