with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
pattern = r'animate\(\);[\s\S]*?</script>'
match = re.search(pattern, content)
if match:
    print("Found bottom of script!")
    # Print the 300 characters before animate()
    start = max(0, match.start() - 300)
    print(content[start:match.start()+100].encode('ascii', 'replace').decode('ascii'))
else:
    print("Could not find animate() at bottom!")
