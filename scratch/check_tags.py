import re

def check_html_structure(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all tab-page divs and print their start positions
    tab_pages = []
    for match in re.finditer(r'<div\s+[^>]*id="page-[^"]+"\s+[^>]*class="[^"]*tab-page[^"]*"[^>]*>', content):
        tab_pages.append((match.start(), match.group(0)))
    
    print(f"Found {len(tab_pages)} tab-page divs:")
    for pos, tag in tab_pages:
        print(f"Pos {pos}: {tag}")
        
    # We want to trace the tag stack to verify if any tab-page is a child of another tab-page.
    # Let's do a simple tag tokenizer for <div and </div
    tokens = []
    # Find all div start and end tags
    for match in re.finditer(r'<(div|/div)\b[^>]*>', content, re.IGNORECASE):
        tag_type = match.group(1).lower()
        full_tag = match.group(0)
        tokens.append((match.start(), tag_type, full_tag))
        
    stack = []
    nested_errors = []
    
    for pos, t_type, tag in tokens:
        if t_type == 'div':
            # Check if this div is a tab-page
            is_tab = 'class="' in tag and 'tab-page' in tag
            tab_id = None
            if is_tab:
                id_match = re.search(r'id="([^"]+)"', tag)
                if id_match:
                    tab_id = id_match.group(1)
            
            # Check if we are currently inside a tab page
            active_tabs = [item for item in stack if item['is_tab']]
            if is_tab and active_tabs:
                nested_errors.append(f"Tab page '{tab_id}' at pos {pos} is nested inside tab page '{active_tabs[-1]['id']}'!")
                
            stack.append({
                'pos': pos,
                'is_tab': is_tab,
                'id': tab_id,
                'tag': tag
            })
        elif t_type == '/div':
            if stack:
                stack.pop()
            else:
                # Extra closing div
                pass

    if nested_errors:
        print("\nERRORS FOUND:")
        for err in nested_errors:
            print(err)
    else:
        print("\nNo nested tab-page divs found!")

if __name__ == '__main__':
    check_html_structure('index.html')
