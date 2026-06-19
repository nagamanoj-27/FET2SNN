with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'animate\(\);', content))
if matches:
    # Get the last match
    m = matches[-1]
    line_no = content[:m.start()].count('\n') + 1
    print(f"Last animate() call found at line {line_no}!")
    start = max(0, m.start() - 600)
    print(content[start:m.start()+200].encode('ascii', 'replace').decode('ascii'))
else:
    print("No matches for animate() found!")
