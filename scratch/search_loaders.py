with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
print("Search results for loading/loader/spinner:")
for m in re.finditer(r'(loader|loading|spinner|overlay)', content, re.IGNORECASE):
    line_no = content[:m.start()].count('\n') + 1
    snippet = content[m.start()-50:m.start()+100].replace('\n', ' ')
    safe_snippet = snippet.encode('ascii', 'replace').decode('ascii')
    print(f"Line {line_no} [{m.group(0)}]: {safe_snippet}")
