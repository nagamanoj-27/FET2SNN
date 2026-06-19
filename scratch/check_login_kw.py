with open('login.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
print("Search results in login.html:")
for kw in ['voxel', 'tornado', 'atmosphere', 'sparkle', 'stream', 'pulse', 'volumetric']:
    count = content.lower().count(kw)
    print(f'Keyword: "{kw}" -> count: {count}')
