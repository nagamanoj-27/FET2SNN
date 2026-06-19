import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Read the user JS code that we extracted
with open('scratch/user_js.js', 'r', encoding='utf-8') as f:
    user_js = f.read()

# 1. Modify the user JS code for integration (without defining the observer yet)
integrated_js = user_js

# Replace container selector
integrated_js = integrated_js.replace(
    "const container = document.getElementById('three-container');",
    "const container = document.getElementById('three-container-device-anim');\n        if (!container) return;"
)

# Replace camera initialization
integrated_js = integrated_js.replace(
    "const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 1000);",
    "const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 1000);"
)

# Replace renderer size set
integrated_js = integrated_js.replace(
    "renderer.setSize(window.innerWidth, window.innerHeight);",
    "// Renderer size will be handled by ResizeObserver below"
)

# Make the scene transparent and set up dynamic fog (initial color set statically)
integrated_js = integrated_js.replace(
    "const scene = new THREE.Scene();\n        scene.background = new THREE.Color(0x050a18);\n        scene.fog = new THREE.FogExp2(0x050a18, 0.028);",
    """const scene = new THREE.Scene();
        scene.background = null; // Transparent background to float on the dashboard

        const isDark = document.body.getAttribute('data-theme') === 'dark';
        const initBgColor = isDark ? 0x0f0f2a : 0xf8f9ff;
        const fogColor = new THREE.Color(initBgColor);
        scene.fog = new THREE.FogExp2(fogColor, 0.028);"""
)

# Replace key lights and ambient lights to store them as mutable variables
integrated_js = integrated_js.replace(
    "const ambientLight = new THREE.AmbientLight(0x0a1a2a, 0.15);",
    "const ambientLight = new THREE.AmbientLight(isDark ? 0x0a1a2a : 0x404060, isDark ? 0.15 : 0.35);"
)

integrated_js = integrated_js.replace(
    "const keyLight = new THREE.DirectionalLight(0x00d4ff, 1.4);",
    "const keyLight = new THREE.DirectionalLight(0x00d4ff, isDark ? 1.4 : 1.2);"
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

# Replace the window resize handler
resize_handler_old = """        window.addEventListener('resize', () => {
            const w = window.innerWidth;
            const h = window.innerHeight;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        });"""

resize_handler_new = """        // Window resize is automatically handled by the ResizeObserver above!"""

integrated_js = integrated_js.replace(resize_handler_old, resize_handler_new)

# Let's keep container-based click listener to avoid document-wide conflicts with inputs
integrated_js = integrated_js.replace(
    "document.addEventListener('click', resetAnimation);",
    "container.addEventListener('click', resetAnimation);"
)

# 2. Insert the Blending & Theme Observer at the VERY BOTTOM of the script (before animate())
# Let's find "animate();" in the integrated_js and place the code right before it.
theme_and_observer_snippet = """// Blending and lighting adaptation observer for seamless Light/Dark mode transitions
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
        
        // Initial setup execution (Safe here because all variables are declared)
        updateThemeColors();

        animate();"""

integrated_js = integrated_js.replace("animate();", theme_and_observer_snippet)

# 3. Build the final script tag
final_script = f"""<script>
(function() {{
{integrated_js}
}})();
</script>"""

# 4. Replace script 31 in index.html
script_pattern = r'<!-- Three.js Library for Device Animation -->\s*<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\s*<script>[\s\S]*?</script>'

replacement_script = f'<!-- Three.js Library for Device Animation -->\n<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n{final_script}'

modified_content, count_script = re.subn(script_pattern, replacement_script, content)
print(f"Replaced animation script block: {count_script} matches.")

if count_script > 0:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(modified_content)
    print("Successfully resolved TDZ ReferenceError and updated index.html!")
else:
    print("Error: Could not perform script replacement in index.html!")
