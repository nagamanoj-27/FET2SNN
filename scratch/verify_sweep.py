# Let's verify that sweep.html can be read without syntax errors or obvious Javascript bracket mismatch.
with open("sweep.html", "r", encoding="utf-8") as f:
    code = f.read()

# Check brackets balance inside <script> blocks
import re
scripts = re.findall(r'<script>(.*?)</script>', code, re.DOTALL)
print(f"Found {len(scripts)} script block(s)")

for idx, script in enumerate(scripts):
    # check standard bracket balances
    brackets = {')': '(', '}': '{', ']': '['}
    stack = []
    lines = script.split('\n')
    for line_num, line in enumerate(lines):
        for char in line:
            if char in brackets.values():
                stack.append((char, line_num + 1))
            elif char in brackets.keys():
                if not stack:
                    print(f"Unexpected closing {char} on line {line_num+1}")
                    continue
                top, top_ln = stack.pop()
                if top != brackets[char]:
                    print(f"Mismatch: {char} on line {line_num+1} doesn't match {top} from line {top_ln}")
    if stack:
        print(f"Unclosed brackets remaining in script block {idx}:")
        for char, ln in stack[:10]:
            print(f"  Unclosed {char} from line {ln}")
    else:
        print(f"Script block {idx} brackets are perfectly balanced!")
