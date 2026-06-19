with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<script([^>]*)>([\s\S]*?)</script>', content))

for idx in [20, 21]: # Script 21 and 22 (0-indexed: 20 and 21)
    if idx < len(matches):
        m = matches[idx]
        line_no = content[:m.start()].count('\n') + 1
        print(f"Script {idx+1} at line {line_no}:")
        print(m.group(2).encode('ascii', 'replace').decode('ascii'))
        print("-" * 50)
