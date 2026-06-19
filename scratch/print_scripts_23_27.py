with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<script([^>]*)>([\s\S]*?)</script>', content))

for idx in [22, 23, 24, 25, 26]: # Scripts 23, 24, 25, 26, 27 (0-indexed: 22 to 26)
    if idx < len(matches):
        m = matches[idx]
        line_no = content[:m.start()].count('\n') + 1
        print(f"Script {idx+1} at line {line_no}:")
        print(m.group(2).encode('ascii', 'replace').decode('ascii'))
        print("-" * 50)
