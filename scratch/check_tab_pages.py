with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<div[^>]*class="[^"]*tab-page[^"]*"[^>]*>', content))
print("Tab pages count:", len(matches))
for m in matches:
    # Find next closing div tag and see if it has an iframe
    start = m.start()
    # Let's search from start for the next 1000 characters
    snippet = content[start:start+1200]
    line_no = content[:start].count('\n') + 1
    
    # Get the ID of the tab page
    id_match = re.search(r'id=["\']([^"\']+)["\']', snippet)
    tab_id = id_match.group(1) if id_match else "unknown"
    
    has_iframe = 'iframe' in snippet
    src_match = re.search(r'src=["\']([^"\']+)["\']', snippet) if has_iframe else None
    iframe_src = src_match.group(1) if src_match else "none"
    
    print(f"Line {line_no}: ID={tab_id}, Has iframe={has_iframe}, Iframe source={iframe_src}")
