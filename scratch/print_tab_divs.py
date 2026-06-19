with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<div[^>]*id="page-(codesign|compare|tcad|modelcards|sweep)"[^>]*>', content))
for m in matches:
    start = m.start()
    print(f"Match found at position {start}:")
    print(content[start:start+400].encode('ascii', 'replace').decode('ascii').replace('\n', ' '))
    print("-" * 40)
