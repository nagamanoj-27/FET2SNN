import os

with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    user = f.read()
with open('scratch/index_js.js', 'r', encoding='utf-8') as f:
    idx = f.read()

keywords = ['voxel', 'tornado', 'atmosphere', 'sparkle', 'stream', 'pulse', 'volumetric']
for kw in keywords:
    user_count = user.lower().count(kw)
    idx_count = idx.lower().count(kw)
    print(f'Keyword: "{kw}" -> User count: {user_count}, Index count: {idx_count}')
