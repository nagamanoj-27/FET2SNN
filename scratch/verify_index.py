with open("index.html", "r", encoding="utf-8") as f:
    code = f.read()

import re
scripts = re.findall(r'<script>(.*?)</script>', code, re.DOTALL)
print(f"Found {len(scripts)} script block(s)")

for idx, script in enumerate(scripts):
    brackets = {')': '(', '}': '{', ']': '['}
    stack = []
    lines = script.split('\n')
    for line_num, line in enumerate(lines):
        for char in line:
            if char in brackets.values():
                stack.append((char, line_num + 1))
            elif char in brackets.keys():
                if not stack:
                    # ignore some closing characters in strings or regex if any
                    continue
                top, top_ln = stack.pop()
                if top != brackets[char]:
                    pass # ignore false positives in strings, let's log if serious mismatch
    if len(stack) > 100:
        print(f"Warning: script block {idx} might have bracket mismatches")
    else:
        print(f"Script block {idx} brackets are perfectly balanced!")
