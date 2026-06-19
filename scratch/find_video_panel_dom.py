with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'id=["\']videoPanel["\']', content))
print("Matches found:", len(matches))
for m in matches:
    line_no = content[:m.start()].count('\n') + 1
    print(f"Line {line_no}:")
    snippet = content[m.start()-100:m.start()+300].replace('\n', ' ')
    print(snippet.encode('ascii', 'replace').decode('ascii'))
