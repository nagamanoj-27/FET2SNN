with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer('tcad-btn-png', content))
print("Occurrences of tcad-btn-png in index.html:", len(matches))
for i, m in enumerate(matches):
    start = max(0, m.start() - 100)
    end = min(len(content), m.start() + 150)
    print(f"Occurrence {i+1}:")
    print(content[start:end].encode('ascii', 'replace').decode('ascii').replace('\n', ' '))
