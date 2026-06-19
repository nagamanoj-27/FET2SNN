import re

# Define replacement mappings for index.html content
def replace_index_colors(content):
    # Hex mappings
    replacements = {
        r'--border:#e0d4ff;': r'--border:#d0dbff;',
        r'--border-glow:rgba\(124,58,237,\.35\);': r'--border-glow:rgba(65,105,225,.35);',
        r'--violet:#7c3aed;': r'--violet:#4169e1;',
        r'--vl:#8b5cf6;': r'--vl:#5c7ff6;',
        r'--vm:#a78bfa;': r'--vm:#8faafc;',
        r'--vp:#f3e8ff;': r'--vp:#e6eeff;',
        r'--sh1:0 4px 15px rgba\(124,58,237,\.05\);': r'--sh1:0 4px 15px rgba(65,105,225,.05);',
        r'--sh2:0 10px 30px rgba\(124,58,237,\.09\);': r'--sh2:0 10px 30px rgba(65,105,225,.09);',
        r'--accent-blue:\s*#4a9eff;': r'--accent-blue: #5c7ff6;',
        r'--accent-purple:\s*#6c5ce7;': r'--accent-purple: #4169e1;',
        
        # Dark theme
        r'--border-glow:rgba\(74, 158, 255, 0.4\);': r'--border-glow:rgba(65, 105, 225, 0.4);',
        r'--violet:#4a9eff;': r'--violet:#4169e1;',
        r'--vl:#6c5ce7;': r'--vl:#5c7ff6;',
        r'--vm:#6c5ce7;': r'--vm:#8faafc;',
        r'--blue:#4a9eff;': r'--blue:#4169e1;',
        r'--magenta:#6c5ce7;': r'--magenta:#5c7ff6;',
        r'--cyan:#4a9eff;': r'--cyan:#5c7ff6;',
        r'--sh2:0 10px 30px rgba\(74, 158, 255, 0.15\);': r'--sh2:0 10px 30px rgba(65, 105, 225, 0.15);',
        
        # Scrollbar thumb
        r'::-webkit-scrollbar-thumb\{background:#e0d4ff;': r'::-webkit-scrollbar-thumb{background:#d0dbff;',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
        
    # RGB/RGBA mappings
    rgba_replacements = {
        r'rgba\(124,58,237,\.22\)': r'rgba(65,105,225,.22)',
        r'rgba\(124,58,237,\.04\)': r'rgba(65,105,225,.04)',
        r'rgba\(124,58,237,\.08\)': r'rgba(65,105,225,.08)',
        r'rgba\(124,58,237,\.18\)': r'rgba(65,105,225,.18)',
        r'rgba\(124,58,237,\.2\)': r'rgba(65,105,225,.2)',
        r'rgba\(124,58,237,\.3\)': r'rgba(65,105,225,.3)',
        r'rgba\(124, 58, 237, 0.04\)': r'rgba(65, 105, 225, 0.04)',
        r'rgba\(124,58,237,\.1\)': r'rgba(65,105,225,.1)',
        r'rgba\(124,58,237,0.1\)': r'rgba(65,105,225,0.1)',
        r'rgba\(124,58,237,\.35\)': r'rgba(65,105,225,.35)',
        r'rgba\(124,58,237,\.13\)': r'rgba(65,105,225,.13)',
        r'rgba\(124,58,237,\.05\)': r'rgba(65,105,225,.05)',
        r'rgba\(124,58,237,\.09\)': r'rgba(65,105,225,.09)',
        r'rgba\(224,212,255,\.18\)': r'rgba(208,219,255,.18)',
        r'rgba\(108, 92, 231, 0.05\)': r'rgba(65, 105, 225, 0.05)',
        r'rgba\(74, 158, 255, 0.05\)': r'rgba(92, 127, 246, 0.05)',
    }
    
    for pattern, replacement in rgba_replacements.items():
        content = re.sub(pattern, replacement, content)
        
    return content

# Read, replace, and write index.html
print("Updating index.html...")
with open("index.html", "r", encoding="utf-8") as f:
    idx_content = f.read()

new_idx = replace_index_colors(idx_content)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_idx)


# Update other files
other_files = ["codesign.html", "model_cards.html", "sweep.html", "validation.html", "tcad_viewer.html"]
for name in other_files:
    print(f"Updating {name}...")
    with open(name, "r", encoding="utf-8") as f:
        c = f.read()
    
    c = c.replace("#8b5cf6", "#5c7ff6")
    c = c.replace("#8B5CF6", "#5c7ff6")
    c = c.replace("#3a86ff", "#4169e1")
    c = c.replace("#3A86FF", "#4169e1")
    
    with open(name, "w", encoding="utf-8") as f:
        f.write(c)


# Update JS files
print("Updating lif-neuron.js...")
with open("lif-neuron.js", "r", encoding="utf-8") as f:
    lif = f.read()
lif = lif.replace("#7c3aed", "#4169e1")
lif = lif.replace("#7C3AED", "#4169e1")
with open("lif-neuron.js", "w", encoding="utf-8") as f:
    f.write(lif)

print("Updating snn-simulator.js...")
with open("snn-simulator.js", "r", encoding="utf-8") as f:
    sim = f.read()
sim = sim.replace("rgba(139, 92, 246", "rgba(92, 127, 246")
sim = sim.replace("#8b5cf6", "#5c7ff6")
with open("snn-simulator.js", "w", encoding="utf-8") as f:
    f.write(sim)

# Update login.html toast
print("Updating login.html...")
with open("login.html", "r", encoding="utf-8") as f:
    log = f.read()
log = log.replace("rgba(124, 58, 237, 0.1)", "rgba(65, 105, 225, 0.1)")
log = log.replace("rgba(124, 58, 237, 0.15)", "rgba(65, 105, 225, 0.15)")
log = log.replace("rgba(139, 92, 246, 0.9)", "rgba(92, 127, 246, 0.9)")
with open("login.html", "w", encoding="utf-8") as f:
    f.write(log)

print("Color changes complete.")
