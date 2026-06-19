with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
print("Search results for --bg definitions:")
for m in re.finditer(r'--bg\s*:\s*([^;]+);', content):
    line_no = content[:m.start()].count('\n') + 1
    print(f"Line {line_no}: {content[m.start():m.start()+100]}")
