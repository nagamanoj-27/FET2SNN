def trace_nesting():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    import re
    clean_content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    tag_pattern = re.compile(r'<(div|/div)\b[^>]*>', re.IGNORECASE)
    
    stack = []
    
    for match in tag_pattern.finditer(clean_content):
        tag_type = match.group(1).lower()
        full_tag = match.group(0)
        line_num = clean_content[:match.start()].count('\n') + 1
        
        if tag_type == 'div':
            is_tab = 'class="' in full_tag and 'tab-page' in full_tag
            tab_id = None
            if is_tab:
                id_match = re.search(r'id="([^"]+)"', full_tag)
                if id_match:
                    tab_id = id_match.group(1)
            
            stack.append({'line': line_num, 'tag': full_tag, 'id': tab_id})
        elif tag_type == '/div':
            if stack:
                stack.pop()
            else:
                pass
                
        if line_num >= 1188 and line_num <= 1562:
            tag_desc = f"<{tag_type}>" if tag_type == 'div' else f"</{tag_type}>"
            stack_repr = []
            for item in stack:
                if item['id']:
                    stack_repr.append(f"#{item['id']}")
                else:
                    class_match = re.search(r'class="([^"]+)"', item['tag'])
                    id_match = re.search(r'id="([^"]+)"', item['tag'])
                    desc = ""
                    if id_match:
                        desc = f"#{id_match.group(1)}"
                    elif class_match:
                        desc = f".{class_match.group(1).split()[0]}"
                    else:
                        desc = "div"
                    stack_repr.append(desc)
            print(f"Line {line_num:4d} | {tag_desc:6s} | Stack depth: {len(stack)} | Stack: {stack_repr}")

if __name__ == '__main__':
    trace_nesting()
