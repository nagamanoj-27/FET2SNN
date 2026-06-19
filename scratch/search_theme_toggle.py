with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
match = re.search(r'function toggleTheme', content)
if match:
    print("Found toggleTheme!")
    print(content[match.start():match.start()+1500].encode('ascii', 'replace').decode('ascii'))
else:
    print("toggleTheme not found!")
