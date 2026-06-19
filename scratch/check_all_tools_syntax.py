import glob
import re

def parse_brackets(js_code, file_name, start_line):
    stack = []
    mismatches = []
    in_single_comment = False
    in_multi_comment = False
    in_string = None
    escaped = False
    
    for i, char in enumerate(js_code):
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
        if char in ['(', '{', '[']:
            stack.append((char, i))
        elif char in [')', '}', ']']:
            if not stack:
                mismatches.append((char, i, "extra_close"))
            else:
                top_char, top_idx = stack.pop()
                matches_bracket = (
                    (top_char == '(' and char == ')') or
                    (top_char == '{' and char == '}') or
                    (top_char == '[' and char == ']')
                )
                if not matches_bracket:
                    mismatches.append((char, i, "mismatch", top_char))
    return len(stack), len(mismatches)

for f in ['codesign.html', 'tcad_viewer.html', 'fet2snn_comparison.html', 'model_cards.html', 'sweep.html', 'validation.html']:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        matches = list(re.finditer(r'<script([^>]*)>([\s\S]*?)</script>', content))
        # Check syntax of each inline script block
        for idx, m in enumerate(matches):
            body = m.group(2)
            if not body.strip():
                continue
            line_no = content[:m.start()].count('\n') + 1
            unclosed, mismatches = parse_brackets(body, f, line_no)
            if unclosed > 0 or mismatches > 0:
                print(f"File {f}: Script {idx+1} at line {line_no} has {unclosed} unclosed brackets and {mismatches} mismatches!")
    except Exception as e:
        print(f"Error checking {f}: {e}")

print("Verification completed.")
