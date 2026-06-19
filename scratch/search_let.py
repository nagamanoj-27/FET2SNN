with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re
lines = content.splitlines()
print("All let variable declarations:")
for idx, line in enumerate(lines):
    if 'let ' in line:
        print(f"Line {idx+1}: {line.strip()}")
