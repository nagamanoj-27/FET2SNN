with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'id=["\']three-container["\']', content))
print("Number of matches for id='three-container' in index.html:", len(matches))
for m in matches:
    print(content[m.start()-40:m.start()+100])
