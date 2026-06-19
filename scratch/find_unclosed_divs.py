def find_nesting_errors():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    import re
    # We want to tokenize `<div`, `</div` and `class="tab-page"` inside index.html.
    # To do this accurately, let's scan tag by tag.
    tag_pattern = re.compile(r'<(div|/div)\b[^>]*>', re.IGNORECASE)
    
    # Let's trace the stack of divs, printing the stack when we hit tab-page divs
    stack = []
    
    # We will ignore commented out HTML.
    # Let's clean the HTML comments first.
    clean_content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    tokens = []
    for match in tag_pattern.finditer(clean_content):
        tag_type = match.group(1).lower()
        full_tag = match.group(0)
        # Find line number
        line_num = clean_content[:match.start()].count('\n') + 1
        tokens.append((match.start(), tag_type, full_tag, line_num))
        
    print(f"Total div tokens found: {len(tokens)}")
    
    # Start traversing
    tab_pages = {}
    for pos, t_type, tag, line in tokens:
        if t_type == 'div':
            # Check if it is a tab page
            is_tab = 'class="' in tag and 'tab-page' in tag
            tab_id = None
            if is_tab:
                id_match = re.search(r'id="([^"]+)"', tag)
                if id_match:
                    tab_id = id_match.group(1)
            
            stack.append({'line': line, 'tag': tag, 'id': tab_id})
            if is_tab:
                print(f"Opening tab-page '{tab_id}' at line {line}. Current stack depth: {len(stack)}")
                print(f"Stack: {[item.get('id') or 'div' for item in stack]}")
        elif t_type == '/div':
            if stack:
                popped = stack.pop()
                if popped['id']:
                    print(f"Closing tab-page '{popped['id']}' at line {line}. Remaining stack depth: {len(stack)}")
            else:
                print(f"ERROR: Extra closing </div> at line {line}!")

if __name__ == '__main__':
    find_nesting_errors()
