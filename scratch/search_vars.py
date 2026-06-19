with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re
print("Variable declarations at the top:")
# Let's print the first 100 lines of user_js.js
lines = content.splitlines()
for idx, line in enumerate(lines[:100]):
    if any(x in line for x in ['let ', 'const ', 'var ']):
        print(f"Line {idx+1}: {line.strip()}")
