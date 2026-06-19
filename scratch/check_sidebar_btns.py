with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<button[^>]*class="[^"]*sidebar-btn[^"]*"[^>]*>', content))
print("Sidebar buttons count:", len(matches))
for m in matches:
    line_no = content[:m.start()].count('\n') + 1
    # Print the button tag
    btn_tag = content[m.start():m.start()+150].split('>')[0] + '>'
    print(f"Line {line_no}: {btn_tag.strip()}")
