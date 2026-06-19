with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re
match = re.search(r'function animate\b', content)
if match:
    # Print the animate function
    print(content[match.start():match.start()+1500].encode('ascii', 'replace').decode('ascii'))
else:
    print("Function animate not found!")
