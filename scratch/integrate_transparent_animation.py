import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the overlay and container markup
container_pattern = r'(<div id="deviceAnimationContainer" style=")[^"]*(">\s*<div id="three-container-device-anim" style="[^"]*"></div>)\s*<div class="overlay top-left" style="[^"]*">[\s\S]*?</div>\s*(</div>)'

replacement_markup = r'''\1width: 100%; height: 600px; position: relative; overflow: hidden; background: transparent; border: none; transition: all 0.8s ease-in-out;\2
          <div class="overlay top-left" style="position: absolute; top: 35px; left: 44px; pointer-events: none; z-index: 10; font-family: var(--outfit);">
            <div class="logo" style="font-size: 24px; font-weight: 800; color: var(--text); letter-spacing: -0.02em; text-shadow: 0 0 40px var(--border-glow);">FET2<span class="accent" style="color: var(--violet); text-shadow: 0 0 20px var(--border-glow);">SNN</span></div>
            <div class="sub" style="font-size: 10px; color: var(--ts); letter-spacing: 0.2em; text-transform: uppercase; margin-top: 2px;">TCAD &middot; SNN</div>
          </div>
        \3'''

modified, count_markup = re.subn(container_pattern, replacement_markup, content)
print(f"Replaced container and overlay markup: {count_markup} matches.")

# 2. Let's find the animation script block and replace it
# We will construct a fresh, clean animation script that handles dynamic blending, light and fog colors.

# Let's read user_js.js to build the script with dynamic theme adjustments
with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    user_js = f.read()

# Make the scene transparent and set up dynamic fog
user_js = user_js.replace(
    "const scene = new THREE.Scene();\n        scene.background = new THREE.Color(0x050a18);\n        scene.fog = new THREE.FogExp2(0x050a18, 0.028);",
    """const scene = new THREE.Scene();
        scene.background = null; // Transparent background to float on the dashboard

        const isDark = document.body.getAttribute('data-theme') === 'dark';
        const initBgColor = isDark ? 0x0f0f2a : 0xf8f9ff;
        const fogColor = new THREE.Color(initBgColor);
        scene.fog = new THREE.FogExp2(fogColor, 0.028);"""
)

# Replace container selector
user_js = user_js.replace(
    "const container = document.getElementById('three-container');",
    "const container = document.getElementById('three-container-device-anim');\n        if (!container) return;"
)

# Replace camera initialization (aspect ratio will be handled by ResizeObserver)
user_js = user_js.replace(
    "const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 1000);",
    "const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 1000);"
)

# Replace renderer size set
user_js = user_js.replace(
    "renderer.setSize(window.innerWidth, window.innerHeight);",
    "// Renderer size will be handled by ResizeObserver below"
)

# Replace key lights and ambient lights to store them as mutable variables
user_js = user_js.replace(
    "const ambientLight = new THREE.AmbientLight(0x0a1a2a, 0.15);",
    "const ambientLight = new THREE.AmbientLight(isDark ? 0x0a1a2a : 0x404060, isDark ? 0.15 : 0.35);"
)

user_js = user_js.replace(
    "const keyLight = new THREE.DirectionalLight(0x00d4ff, 1.4);",
    "const keyLight = new THREE.DirectionalLight(0x00d4ff, isDark ? 1.4 : 1.2);"
)

# Insert ResizeObserver and MutationObserver right after container.appendChild(renderer.domElement);
append_str = "container.appendChild(renderer.domElement);"

# We need to collect all materials that use AdditiveBlending and register them for updates
observer_and_theme_code = """container.appendChild(renderer.domElement);

        // ResizeObserver to ensure canvas matches container size with zero distortion and high resolution
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
        resizeObserver.observe(container);

        // Blending and lighting adaptation observer for seamless Light/Dark mode transitions
        const matsToAdjust = [
            flowMat,
            ringMat,
            tornadoMat,
            sparkleMat,
            atmosMat,
            beamMat
        ];

        function updateThemeColors() {
            const dark = document.body.getAttribute('data-theme') === 'dark';
            const bgColor = dark ? 0x0f0f2a : 0xf8f9ff;
            fogColor.setHex(bgColor);

            // In light mode, switch blending to NormalBlending so bright items are visible against white background.
            // In dark mode, keep AdditiveBlending for glowing volumetric effects.
            const blendingMode = dark ? THREE.AdditiveBlending : THREE.NormalBlending;

            matsToAdjust.forEach(mat => {
                if (mat) {
                    mat.blending = blendingMode;
                    mat.needsUpdate = true;
                }
            });

            rings.forEach(ring => {
                if (ring && ring.material) {
                    ring.material.blending = blendingMode;
                    ring.material.needsUpdate = true;
                }
            });

            nnLines.forEach(line => {
                if (line && line.material) {
                    line.material.blending = blendingMode;
                    line.material.needsUpdate = true;
                }
            });

            if (dark) {
                ambientLight.color.setHex(0x0a1a2a);
                ambientLight.intensity = 0.15;
                keyLight.intensity = 1.4;
            } else {
                ambientLight.color.setHex(0x404060);
                ambientLight.intensity = 0.35;
                keyLight.intensity = 1.2;
            }
        }

        const themeObserver = new MutationObserver(() => {
            updateThemeColors();
        });
        themeObserver.observe(document.body, { attributes: true, attributeFilter: ['data-theme'] });
        
        // Initial setup
        updateThemeColors();"""

user_js = user_js.replace(append_str, observer_and_theme_code)

# Replace the window resize handler
resize_handler_old = """        window.addEventListener('resize', () => {
            const w = window.innerWidth;
            const h = window.innerHeight;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        });"""

resize_handler_new = """        // Window resize is automatically handled by the ResizeObserver above!"""

user_js = user_js.replace(resize_handler_old, resize_handler_new)

# Let's keep container-based click listener to avoid document-wide conflicts with inputs
user_js = user_js.replace(
    "document.addEventListener('click', resetAnimation);",
    "container.addEventListener('click', resetAnimation);"
)

# Build the final script structure
final_script = f"""<script>
(function() {{
{user_js}
}})();
</script>"""

# Replace in modified index_content
script_pattern = r'<!-- Three.js Library for Device Animation -->\s*<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\s*<script>[\s\S]*?</script>'

replacement_script = f'<!-- Three.js Library for Device Animation -->\n<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n{final_script}'

modified, count_script = re.subn(script_pattern, replacement_script, modified)
print(f"Replaced animation script block: {count_script} matches.")

if count_markup > 0 and count_script > 0:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(modified)
    print("Successfully updated index.html for card-to-dashboard seamless blending!")
else:
    print("Error: Could not perform all replacements in index.html!")
