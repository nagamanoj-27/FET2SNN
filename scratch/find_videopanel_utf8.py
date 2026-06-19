import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('id="videoPanel"')
if start != -1:
    print(text[start-100:start+1800])
else:
    print("Not found")
