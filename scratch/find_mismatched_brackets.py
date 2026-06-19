import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract Script 9 (starts at line 2421)
script_pattern = r'<script>([\s\S]*?)</script>'
matches = list(re.finditer(script_pattern, content))
# Let's verify which match corresponds to line 2421
target_match = None
for m in matches:
    line_no = content[:m.start()].count('\n') + 1
    if 2410 <= line_no <= 2430:
        target_match = m
        break

if not target_match:
    # Fallback to the largest script
    target_match = max(matches, key=lambda m: len(m.group(1)))

js_code = target_match.group(1)
start_line = content[:target_match.start()].count('\n') + 1
print(f"Analyzing script starting at line {start_line}, length {len(js_code)} chars...")

# Character-by-character parser that ignores strings and comments
stack = []
mismatches = []

in_single_comment = False
in_multi_comment = False
in_string = None # Can be ', ", or `
escaped = False

lines = js_code.splitlines()

for i, char in enumerate(js_code):
    # Calculate current line and column (1-indexed)
    prefix = js_code[:i]
    cur_line = start_line + prefix.count('\n')
    last_nl = prefix.rfind('\n')
    cur_col = i - last_nl if last_nl != -1 else i + 1
    
    if escaped:
        escaped = False
        continue
        
    if in_single_comment:
        if char == '\n':
            in_single_comment = False
        continue
        
    if in_multi_comment:
        if char == '/' and i > 0 and js_code[i-1] == '*':
            in_multi_comment = False
        continue
        
    if in_string:
        if char == '\\':
            escaped = True
        elif char == in_string:
            in_string = None
        continue
        
    # Check for comments and strings start
    if char == '/' and i + 1 < len(js_code):
        next_char = js_code[i+1]
        if next_char == '/':
            in_single_comment = True
            continue
        elif next_char == '*':
            in_multi_comment = True
            continue
            
    if char in ["'", '"', '`']:
        in_string = char
        continue
        
    # Check for brackets
    if char in ['(', '{', '[']:
        stack.append((char, cur_line, cur_col, i))
    elif char in [')', '}', ']']:
        if not stack:
            print(f"ERROR: Extra closing bracket '{char}' at line {cur_line}, col {cur_col}")
            mismatches.append((char, cur_line, cur_col, "extra_close"))
        else:
            top_char, top_line, top_col, top_idx = stack.pop()
            matches_bracket = (
                (top_char == '(' and char == ')') or
                (top_char == '{' and char == '}') or
                (top_char == '[' and char == ']')
            )
            if not matches_bracket:
                print(f"ERROR: Mismatched bracket. Opened '{top_char}' at line {top_line}, col {top_col} but closed with '{char}' at line {cur_line}, col {cur_col}")
                mismatches.append((char, cur_line, cur_col, "mismatch", top_char, top_line, top_col))

# Print remaining items on the stack
if stack:
    print(f"\nERROR: {len(stack)} unclosed brackets remaining at end of script:")
    for item in stack[-10:]: # print last 10
        print(f"  Unclosed '{item[0]}' opened at line {item[1]}, col {item[2]}")
        # Print snippet of line
        line_content = lines[item[1] - start_line]
        print(f"    Line content: {line_content.strip()}")
else:
    print("\nNo unclosed brackets remaining.")
