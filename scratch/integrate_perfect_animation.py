import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Read the user JS code that we extracted
with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    user_js = f.read()

# 1. Modify the user JS code for integration
integrated_js = user_js

# Replace container selector
integrated_js = integrated_js.replace(
    "const container = document.getElementById('three-container');",
    "const container = document.getElementById('three-container-device-anim');\n        if (!container) return;"
)

# Replace camera initialization (aspect ratio will be handled by ResizeObserver)
integrated_js = integrated_js.replace(
    "const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 1000);",
    "const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 1000);"
)

# Replace renderer size set
integrated_js = integrated_js.replace(
    "renderer.setSize(window.innerWidth, window.innerHeight);",
    "// Renderer size will be handled by ResizeObserver below"
)

# Insert ResizeObserver right after container.appendChild(renderer.domElement);
append_str = "container.appendChild(renderer.domElement);"
observer_code = """container.appendChild(renderer.domElement);

        // Dynamic ResizeObserver to ensure canvas matches container size with zero distortion and high resolution
        const resizeObserver = new ResizeObserver(entries => {
            for (let entry of entries) {
                const w = entry.contentRect.width || container.clientWidth;
                const h = entry.contentRect.height || container.clientHeight;
                if (w > 0 && h > 0) {
                    camera.aspect = w / h;
                    camera.updateProjectionMatrix();
                    renderer.setSize(w, h);
                }
            }
        });
        resizeObserver.observe(container);"""

integrated_js = integrated_js.replace(append_str, observer_code)

# Replace the window resize handler to avoid double resizing
resize_handler_old = """        window.addEventListener('resize', () => {
            const w = window.innerWidth;
            const h = window.innerHeight;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        });"""

resize_handler_new = """        // Window resize is automatically handled by the ResizeObserver above!"""

integrated_js = integrated_js.replace(resize_handler_old, resize_handler_new)

# Let's keep container-based click listener to avoid document-wide conflicts with inputs,
# but make sure everything else is 100% identical.
integrated_js = integrated_js.replace(
    "document.addEventListener('click', resetAnimation);",
    "container.addEventListener('click', resetAnimation);"
)

# 2. Wrap in IIFE to protect scope
final_script = f"""<script>
(function() {{
{integrated_js}
}})();
</script>"""

# 3. Replace script 31 in index.html
# We find the script tag that loads the CDN Three.js library and the script after it
pattern = r'<!-- Three.js Library for Device Animation -->\s*<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\s*<script>[\s\S]*?</script>'

replacement = f'<!-- Three.js Library for Device Animation -->\n<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n{final_script}'

modified_content, count = re.subn(pattern, replacement, index_content)
print(f"Replaced animation script: {count} matches.")

# 4. Replace the overlay in index.html to match user's exact overlay
# Let's look for the deviceAnimationContainer div
container_pattern = r'(<div id="deviceAnimationContainer" style="[^"]*">)\s*<div id="three-container-device-anim" style="[^"]*"></div>\s*<div class="overlay-device-anim" style="[^"]*">[\s\S]*?</div>\s*(</div>)'

overlay_replacement = r'''\1
          <div id="three-container-device-anim" style="width: 100%; height: 100%;"></div>
          <div class="overlay top-left" style="position: absolute; top: 35px; left: 44px; pointer-events: none; z-index: 10;">
            <div class="logo" style="font-size: 24px; font-weight: 800; color: #f0f4f8; letter-spacing: -0.02em; text-shadow: 0 0 60px rgba(0, 212, 255, 0.05);">FET2<span class="accent" style="color: #00d4ff; text-shadow: 0 0 60px rgba(0, 212, 255, 0.2);">SNN</span></div>
            <div class="sub" style="font-size: 10px; color: rgba(240, 244, 248, 0.6); letter-spacing: 0.2em; text-transform: uppercase; margin-top: 2px;">TCAD &middot; SNN</div>
          </div>
        \2'''

modified_content, overlay_count = re.subn(container_pattern, overlay_replacement, modified_content)
print(f"Replaced overlay: {overlay_count} matches.")

# Save modified index.html
if count > 0 and overlay_count > 0:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(modified_content)
    print("Successfully updated index.html!")
else:
    print("Error: Could not find script or overlay patterns in index.html!")
