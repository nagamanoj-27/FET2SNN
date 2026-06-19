with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'globalSpinner', content))
print("globalSpinner references:", len(matches))
for m in matches:
    line_no = content[:m.start()].count('\n') + 1
    # Print the line
    line_content = content.splitlines()[line_no - 1]
    print(f"Line {line_no}: {line_content.strip()}")
