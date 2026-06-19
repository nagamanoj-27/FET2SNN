with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
match = re.search(r'const matsToAdjust', content)
if match:
    # Print 200 characters before and 400 characters after the match
    start = max(0, match.start() - 200)
    end = min(len(content), match.start() + 400)
    print("Code around matsToAdjust:")
    print(content[start:end].encode('ascii', 'replace').decode('ascii').replace('\n', ' '))
else:
    print("Could not find const matsToAdjust!")
