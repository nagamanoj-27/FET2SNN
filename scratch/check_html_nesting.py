from html.parser import HTMLParser

class TabPageNestingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.tab_pages = {} # maps tab_id -> parent_id (or None for root level)
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag_id = attrs_dict.get('id')
        classes = attrs_dict.get('class', '')
        
        # Check if this is a tab page
        is_tab = 'tab-page' in classes.split()
        
        parent_id = None
        # Find the nearest parent that is a tab page
        for item in reversed(self.stack):
            if item['is_tab']:
                parent_id = item['id']
                break
                
        if is_tab:
            self.tab_pages[tag_id or f"unnamed-tab-{self.getpos()}"] = parent_id
            
        self.stack.append({
            'tag': tag,
            'id': tag_id,
            'is_tab': is_tab
        })
        
    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

parser = TabPageNestingParser()
parser.feed(content)

print("--- Tab Pages Nesting Analysis ---")
nested_count = 0
for tab_id, parent_id in parser.tab_pages.items():
    if parent_id:
        print(f"ERROR: Tab '{tab_id}' is nested inside '{parent_id}'!")
        nested_count += 1
    else:
        print(f"Tab '{tab_id}' is correctly at the root level.")

if nested_count == 0:
    print("All tab pages are correctly placed at the root level (no nesting issues).")
else:
    print(f"Total nested tab pages: {nested_count}")
