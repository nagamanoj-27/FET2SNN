with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for btn_id in ['tcad-btn-png', 'tcad-btn-gltf', 'tcad-btn-csv']:
    matches = content.count(btn_id)
    print(f"ID '{btn_id}' count in index.html: {matches}")
