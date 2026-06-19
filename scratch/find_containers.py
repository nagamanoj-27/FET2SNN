import re

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("=== Openings ===")
for idx, line in enumerate(lines, 1):
    if "app-container" in line or "class=\"pw\"" in line or "id=\"page-" in line:
        print(f"Line {idx:4d}: {line.strip()}")
