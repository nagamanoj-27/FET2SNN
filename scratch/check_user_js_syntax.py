with open('scratch/user_animation_code.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
pattern = r'<script>([\s\S]*?)</script>'
matches = re.findall(pattern, content)
if matches:
    script_content = matches[-1]
    print("Script found! Length:", len(script_content))
    
    # Check braces matching
    open_curly = script_content.count('{')
    close_curly = script_content.count('}')
    open_paren = script_content.count('(')
    close_paren = script_content.count(')')
    print(f"Curly braces: {{ = {open_curly}, }} = {close_curly}")
    print(f"Parentheses: ( = {open_paren}, ) = {close_paren}")
    
    if open_curly != close_curly:
        print("WARNING: Mismatched curly braces!")
    if open_paren != close_paren:
        print("WARNING: Mismatched parentheses!")
else:
    print("Script tag not found!")
