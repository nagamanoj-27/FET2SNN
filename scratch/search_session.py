import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for login, token, or session check logic in index.html
print("--- Login redirects or token checks ---")
for m in re.finditer(r'(location\.href|localStorage|sessionStorage|token|login|logout)', content, re.IGNORECASE):
    start = max(0, m.start() - 80)
    end = min(len(content), m.start() + 120)
    snippet = content[start:end].replace('\n', ' ')
    print(f"[{m.group(0)}] at {m.start()}: ... {snippet} ...")
