with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
match = re.search(r'id=["\']dashboardPage["\']', content)
if match:
    print("Found dashboardPage in login.html!")
    print(content[match.start():match.start()+1000].encode('ascii', 'replace').decode('ascii'))
else:
    print("dashboardPage not found in login.html!")
