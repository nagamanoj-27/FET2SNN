import subprocess
import time
import os
import sys

def click_tab_and_get_logs():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    log_file = os.path.abspath("scratch/chrome_debug_click.log")
    if os.path.exists(log_file):
        os.remove(log_file)
        
    # Python script to run Chrome with debugging enabled, so we can run JS commands.
    # Actually, we can run chrome with --headless and execute JavaScript on load!
    # How? Chrome doesn't let you run JS from the CLI easily unless you use remote debugging.
    # But wait! We can inject a script in index.html to click the button on load, or we can just run Chrome,
    # wait, and let it run index.html where we temporarily inject a click!
    # Let's temporarily append a script to index.html that clicks the codesign button 2 seconds after load,
    # and then run the standard headless chrome check! That is extremely easy and doesn't require complex debugging protocols!
    print("Injecting temporary auto-clicker into index.html...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    # Append the clicker before </body>
    clicker_script = """
    <script>
    window.addEventListener('load', () => {
        setTimeout(() => {
            console.log("AUTO-CLICKER: Clicking Co-design Mode button");
            const btn = document.querySelector('.sidebar-btn[data-target="page-codesign"]');
            if (btn) {
                btn.click();
            } else {
                console.log("AUTO-CLICKER: Button not found!");
            }
        }, 1500);
    });
    </script>
    """
    temp_html = html.replace("</body>", clicker_script + "\n</body>")
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(temp_html)
        
    try:
        print("Starting Chrome...")
        process = subprocess.Popen([
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--enable-logging",
            "--v=1",
            f"--log-file={log_file}",
            "http://127.0.0.1:5000/"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Let it run for 5 seconds to let the clicker fire and codesign.html load
        time.sleep(5)
        
        print("Terminating Chrome...")
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            
    finally:
        # Restore index.html
        print("Restoring index.html...")
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
            
    if os.path.exists(log_file):
        print("Log file created.")
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            log_content = f.read()
        lines = log_content.split('\n')
        print("\n--- AUTO-CLICKER CHROME LOGS ---")
        for line in lines:
            if 'GL_INVALID_VALUE' in line:
                continue
            if 'CONSOLE' in line or 'error' in line.lower() or 'exception' in line.lower() or 'failed' in line.lower() or 'uncaught' in line.lower():
                print(line.encode('utf-8', errors='replace').decode('utf-8'))
        print("---------------------------------")
    else:
        print("Log file not created.")

if __name__ == '__main__':
    click_tab_and_get_logs()
