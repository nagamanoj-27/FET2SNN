with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.finditer(r'blending\s*:\s*THREE\.AdditiveBlending', content)
for m in matches:
    line_no = content[:m.start()].count('\n') + 1
    # Print surrounding lines
    print(f"Line {line_no}:")
    print(content[m.start()-100:m.start()+150].encode('ascii', 'replace').decode('ascii'))
    print("-" * 40)
