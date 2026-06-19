import re
with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's find all range inputs
pattern = re.compile(r'<input\s+[^>]*type="range"[^>]*id="([^"]+)"[^>]*>')
sliders = pattern.findall(text)
print("Sliders found:", sliders)

# Let's find all select inputs
pattern_select = re.compile(r'<select\s+[^>]*id="([^"]+)"[^>]*>')
selects = pattern_select.findall(text)
print("Selects found:", selects)
