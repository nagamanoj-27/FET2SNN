import os
import re

files = [
    'index.html', 'index.html.bak', 'login.html', 'tcad_viewer.html', 
    'model_cards.html', 'sweep.html', 'codesign.html', 'validation.html', 
    'fet2snn_comparison.html'
]

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Find all classes or elements containing 'brain'
            brain_matches = re.findall(r'<[^>]*brain[^>]*>', content, re.IGNORECASE)
            # Find all SVG paths or tags
            svg_matches = re.findall(r'<svg[^>]*>', content, re.IGNORECASE)
            
            print(f"=== {filename} ===")
            print(f"Brain matches ({len(brain_matches)}):")
            for m in brain_matches[:10]:
                print("  ", m.strip())
            print(f"SVG tags count: {len(svg_matches)}")
