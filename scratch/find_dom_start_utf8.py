import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("document.addEventListener('DOMContentLoaded'")
if start != -1:
    print(text[start-100:start+600])
else:
    print("Not found")
