import re

with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("--- Login page redirections ---")
for m in re.finditer(r'(location\.href|localStorage|sessionStorage|token|index\.html)', content, re.IGNORECASE):
    line_no = content[:m.start()].count('\n') + 1
    snippet = content[m.start()-50:m.start()+100].replace('\n', ' ')
    safe_snippet = snippet.encode('ascii', 'replace').decode('ascii')
    print(f"Line {line_no} [{m.group(0)}]: ... {safe_snippet} ...")
