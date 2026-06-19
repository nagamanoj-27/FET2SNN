with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('onclick="exportPDF()"')
if start != -1:
    print(text[start-600:start+200])
else:
    print("Not found")
