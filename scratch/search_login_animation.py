with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
print("Search results in login.html:")
for m in re.finditer(r'(deviceAnimationContainer|three-container-device-anim|three-container|Ultimate 3D)', content, re.IGNORECASE):
    line_no = content[:m.start()].count('\n') + 1
    snippet = content[m.start()-50:m.start()+100].replace('\n', ' ')
    print(f"Line {line_no} [{m.group(0)}]: {snippet}")
