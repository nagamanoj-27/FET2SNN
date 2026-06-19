import os

def check_brackets(code, filepath):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    
    in_string = False
    string_char = None
    in_line_comment = False
    in_block_comment = False
    
    i = 0
    n = len(code)
    errors = []
    while i < n:
        char = code[i]
        
        # Handle block comments
        if in_block_comment:
            if i + 1 < n and code[i:i+2] == '*/':
                in_block_comment = False
                i += 2
                continue
            i += 1
            continue
            
        # Handle line comments
        if in_line_comment:
            if char == '\n':
                in_line_comment = False
            i += 1
            continue
            
        # Handle strings
        if in_string:
            if char == '\\':
                i += 2  # skip escaped char
                continue
            if char == string_char:
                in_string = False
            i += 1
            continue
            
        # Check comment starts
        if i + 1 < n and code[i:i+2] == '/*':
            in_block_comment = True
            i += 2
            continue
        if i + 1 < n and code[i:i+2] == '//':
            in_line_comment = True
            i += 2
            continue
            
        # Check string starts
        if char in ['"', "'", '`']:
            in_string = True
            string_char = char
            i += 1
            continue
            
        # Track braces, parens, brackets
        if char in '({[':
            stack.append((char, i))
        elif char in ')}]':
            expected = pairs[char]
            if not stack:
                code_before = code[:i]
                rel_line = 1 + code_before.count('\n')
                errors.append(f"Unmatched closing '{char}' at line {rel_line}")
            else:
                top, pos = stack.pop()
                if top != expected:
                    code_before = code[:i]
                    rel_line = 1 + code_before.count('\n')
                    errors.append(f"Mismatched '{char}' (expected '{pairs[char]}' matching '{top}' from line {1 + code[:pos].count('\n')}) at line {rel_line}")
        i += 1
        
    if stack:
        for top, pos in stack:
            rel_line = 1 + code[:pos].count('\n')
            errors.append(f"Unclosed opening '{top}' declared at line {rel_line}")
            
    if errors:
        print(f"\n--- ERRORS in {filepath} ---")
        for err in errors:
            print(err)
    else:
        print(f"File {filepath}: OK")

def scan_js_files():
    for f in os.listdir('.'):
        if f.endswith('.js'):
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
            check_brackets(content, f)

if __name__ == '__main__':
    scan_js_files()
