with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
print("Search results for background variables:")
matches = re.findall(r'(--bg[a-zA-Z0-9_-]*|background|body\s*\{[^}]*\})', content, re.IGNORECASE)
for m in matches[:30]:
    print(m)
