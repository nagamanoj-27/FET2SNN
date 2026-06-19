with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Strip comments
clean_content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
# Strip script blocks
clean_content = re.sub(r'<script\b[^>]*>.*?</script>', '', clean_content, flags=re.DOTALL | re.IGNORECASE)
# Strip style blocks
clean_content = re.sub(r'<style\b[^>]*>.*?</style>', '', clean_content, flags=re.DOTALL | re.IGNORECASE)

tag_pattern = re.compile(r'<(div|/div)\b[^>]*>', re.IGNORECASE)

stack = []

print("Line | Tag | Stack Depth | Stack")
print("-" * 60)

for match in tag_pattern.finditer(clean_content):
    tag_type = match.group(1).lower()
    full_tag = match.group(0)
    line_num = clean_content[:match.start()].count('\n') + 1
    
    if tag_type == 'div':
        id_match = re.search(r'id="([^"]+)"', full_tag)
        class_match = re.search(r'class="([^"]+)"', full_tag)
        tag_id = id_match.group(1) if id_match else None
        tag_class = class_match.group(1) if class_match else None
        
        stack.append({'line': line_num, 'tag': full_tag, 'id': tag_id, 'class': tag_class})
    elif tag_type == '/div':
        if stack:
            stack.pop()
        else:
            print(f"Line {line_num:4d} | WARNING: Pop from empty stack! Tag: {full_tag}")
            
    # Print at key lines:
    # 1. Any tag with id starting with "page-"
    # 2. Stack depth drops to 0 or 1
    is_page = False
    for item in stack:
        if item['id'] and item['id'].startswith('page-'):
            is_page = True
            
    id_match = re.search(r'id="([^"]+)"', full_tag)
    if id_match and id_match.group(1).startswith('page-'):
        is_page = True

    if is_page or len(stack) <= 1:
        tag_desc = f"<{tag_type}>" if tag_type == 'div' else f"</{tag_type}>"
        stack_repr = []
        for item in stack:
            if item['id']:
                stack_repr.append(f"#{item['id']}")
            elif item['class']:
                stack_repr.append(f".{item['class'].split()[0]}")
            else:
                stack_repr.append("div")
        print(f"Line {line_num:4d} | {tag_desc:6s} | Depth: {len(stack)} | Stack: {stack_repr}")
