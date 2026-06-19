with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<script([^>]*)>([\s\S]*?)</script>', content))
print("Total script tags found:", len(matches))

for idx, m in enumerate(matches):
    attrs = m.group(1)
    body = m.group(2)
    line_no = content[:m.start()].count('\n') + 1
    
    # Skip external scripts without body
    if not body.strip():
        continue
        
    open_curly = body.count('{')
    close_curly = body.count('}')
    open_paren = body.count('(')
    close_paren = body.count(')')
    
    mismatched = ""
    if open_curly != close_curly:
        mismatched += f" Mismatched curlies ({open_curly} vs {close_curly}) "
    if open_paren != close_paren:
        mismatched += f" Mismatched parens ({open_paren} vs {close_paren}) "
        
    if mismatched:
        print(f"Script {idx+1} at line {line_no} ({attrs.strip() or 'inline'}):{mismatched}")
    else:
        # Check basic syntax by matching quotes etc.
        pass
print("Syntax check completed.")
