with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
print("Search results:")
for m in re.finditer(r'(auth|token|session|login|user|profile)', content, re.IGNORECASE):
    # Print the line
    line_no = content[:m.start()].count('\n') + 1
    # Check if we already printed a nearby line to avoid duplicates
    snippet = content[m.start()-50:m.start()+100].replace('\n', ' ')
    print(f"Line {line_no}: ... {snippet} ...")
