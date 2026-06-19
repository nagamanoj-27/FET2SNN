with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
match = re.search(r'function initThree', content)
if match:
    # Print the function body
    print(content[match.start():match.start()+1500].encode('ascii', 'replace').decode('ascii'))
else:
    print("Function initThree not found!")
