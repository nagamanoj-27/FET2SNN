with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re
lines = content.splitlines()

# Search around lines 350-600 for material declarations
for idx, line in enumerate(lines[300:600], start=301):
    if 'const ' in line and ('Material' in line or 'Mat' in line or 'material' in line):
        print(f"Line {idx}: {line.strip()}")
