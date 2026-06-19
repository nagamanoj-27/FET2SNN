import glob

for f in glob.glob('*.html'):
    content = open(f, encoding='utf-8', errors='ignore').read()
    if 'mp4' in content or 'manim' in content:
        print(f"File {f} contains mp4/manim references.")
        # Find lines containing them
        for line in content.splitlines():
            if 'mp4' in line or 'manim' in line:
                print(f"  {line.strip()}")
