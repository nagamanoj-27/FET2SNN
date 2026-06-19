with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

stack = []
in_script = False
in_style = False
in_comment = False

import re

print("Line | Tag Action | Stack Depth | Stack")
print("-" * 75)

for idx, line in enumerate(lines, 1):
    # We need to scan this line for divs and script/style tags
    # Let's simplify: look at tags in this line
    # Since comments, scripts, styles can span lines, let's track state
    # We can tokensise using regex
    pos = 0
    while pos < len(line):
        rest = line[pos:]
        
        # Check transitions
        if in_comment:
            end_comment_match = re.match(r'.*?-->', rest)
            if end_comment_match:
                in_comment = False
                pos += end_comment_match.end()
            else:
                break # rest of line is comment
        elif in_script:
            end_script_match = re.match(r'.*?</script>', rest, re.IGNORECASE)
            if end_script_match:
                in_script = False
                pos += end_script_match.end()
            else:
                break # rest of line is script
        elif in_style:
            end_style_match = re.match(r'.*?</style>', rest, re.IGNORECASE)
            if end_style_match:
                in_style = False
                pos += end_style_match.end()
            else:
                break # rest of line is style
        else:
            # Look for next tag
            tag_match = re.search(r'(<!--|<script\b|<style\b|</script>|</style>|<div\b|</div\b)', rest, re.IGNORECASE)
            if not tag_match:
                break
                
            tag = tag_match.group(1).lower()
            pos += tag_match.start()
            
            if tag == '<!--':
                in_comment = True
                pos += 4
            elif tag == '<script':
                in_script = True
                pos += 7
            elif tag == '<style':
                in_style = True
                pos += 6
            elif tag == '<div':
                # find end of this div opening tag on the current line (approximate)
                div_tag_rest = line[pos:]
                end_div_match = re.match(r'<div\b[^>]*>', div_tag_rest, re.IGNORECASE)
                full_tag = ""
                if end_div_match:
                    full_tag = end_div_match.group(0)
                    pos += end_div_match.end()
                else:
                    full_tag = "<div>"
                    pos += 4
                
                id_match = re.search(r'id="([^"]+)"', full_tag)
                class_match = re.search(r'class="([^"]+)"', full_tag)
                tag_id = id_match.group(1) if id_match else None
                tag_class = class_match.group(1) if class_match else None
                
                stack.append({'line': idx, 'tag': full_tag, 'id': tag_id, 'class': tag_class})
                
                # Print status
                is_page = False
                for item in stack:
                    if item['id'] and item['id'].startswith('page-'):
                        is_page = True
                if is_page or len(stack) <= 2:
                    stack_repr = [f"#{item['id']}" if item['id'] else (f".{item['class'].split()[0]}" if item['class'] else "div") for item in stack]
                    print(f"{idx:4d} | OPEN  {full_tag[:20]:20s} | Depth: {len(stack):2d} | Stack: {stack_repr}")
            elif tag == '</div':
                pos += 6 # length of </div> is 6
                # find matching '>'
                close_rest = line[pos-1:]
                if close_rest.startswith('>'):
                    pass # correct
                
                if stack:
                    popped = stack.pop()
                else:
                    print(f"{idx:4d} | WARNING: Popped from empty stack! </div>")
                
                is_page = False
                for item in stack:
                    if item['id'] and item['id'].startswith('page-'):
                        is_page = True
                if is_page or len(stack) <= 2:
                    stack_repr = [f"#{item['id']}" if item['id'] else (f".{item['class'].split()[0]}" if item['class'] else "div") for item in stack]
                    print(f"{idx:4d} | CLOSE </div>               | Depth: {len(stack):2d} | Stack: {stack_repr}")
            else:
                # Should not happen
                pos += len(tag)
