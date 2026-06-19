with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
pattern = r'<!-- Three.js Library for Device Animation -->\s*<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\s*<script>([\s\S]*?)</script>'
match = re.search(pattern, content)
if match:
    script_content = match.group(1)
    lines = script_content.splitlines()
    for idx, line in enumerate(lines[:150]):
        print(f"{idx+1}: {line.encode('ascii', 'replace').decode('ascii')}")
else:
    print("Script not found!")
