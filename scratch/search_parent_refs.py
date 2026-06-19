import glob
import re

for f in ['codesign.html', 'tcad_viewer.html', 'fet2snn_comparison.html', 'model_cards.html', 'sweep.html', 'validation.html']:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        matches = list(re.finditer(r'(parent\.|window\.parent)', content))
        if matches:
            print(f"File {f} has {len(matches)} parent references:")
            for m in matches:
                line_no = content[:m.start()].count('\n') + 1
                snippet = content[m.start()-50:m.start()+100].replace('\n', ' ')
                print(f"  Line {line_no}: {snippet.strip()}")
    except Exception as e:
        print(f"Error checking {f}: {e}")
