with open("index.html", "r", encoding="utf-8") as f:
    current = f.readlines()

with open("index.html.bak", "r", encoding="utf-8") as f:
    backup = f.readlines()

print(f"Current length: {len(current)}, Backup length: {len(backup)}")

# Find where "deviceAnimationContainer" appears in both
for idx, line in enumerate(current, 1):
    if "deviceAnimationContainer" in line:
        print(f"Current: Line {idx}: {line.strip()}")
        # print some context
        for j in range(max(0, idx-5), min(len(current), idx+10)):
            print(f"  {j+1}: {current[j].strip()}")
        break

print("-" * 40)
for idx, line in enumerate(backup, 1):
    if "deviceAnimationContainer" in line:
        print(f"Backup: Line {idx}: {line.strip()}")
        for j in range(max(0, idx-5), min(len(backup), idx+10)):
            print(f"  {j+1}: {backup[j].strip()}")
        break
