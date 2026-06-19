import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's find all IDs in index.html
ids = re.findall(r'id="([a-zA-Z0-9_-]+)"', text)
print("IDs found:")
for i in ids:
    if any(keyword in i.lower() for keyword in ["panel", "card", "view", "btn", "chart", "container", "plot", "canvas"]):
        print(f"  {i}")

# Let's find major cards / sections with class="card" or class containing card
cards = re.findall(r'<div\s+[^>]*class="[^"]*card[^"]*"[^>]*>', text)
print("\nCards found:")
for c in cards[:15]:
    print(f"  {c}")
