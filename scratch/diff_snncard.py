import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("index.html.bak", "r", encoding="utf-8") as f:
    backup = f.readlines()

for idx, line in enumerate(backup, 1):
    if "snnCard" in line:
        print(f"Backup snnCard: Line {idx}: {line.strip()}")
        for j in range(max(0, idx-5), min(len(backup), idx+30)):
            print(f"  {j+1}: {backup[j].strip()}")
        break
