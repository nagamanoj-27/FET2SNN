import glob
import re

for f in glob.glob('*.html'):
    content = open(f, encoding='utf-8', errors='ignore').read()
    # Find tags containing video
    matches = list(re.finditer(r'<[^>]*video[^>]*>', content, re.IGNORECASE))
    if matches:
        print(f"File {f} has {len(matches)} video tags/elements:")
        for m in matches[:10]:
            print(f"  {m.group(0).strip()}")
