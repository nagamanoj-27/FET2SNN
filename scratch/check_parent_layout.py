import subprocess
import time
import os
import sys

def get_dom_hierarchy():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    log_file = os.path.abspath("scratch/chrome_dom.log")
    if os.path.exists(log_file):
        os.remove(log_file)
        
    # We will temporarily append a script to index.html that dumps the DOM parent structure to console.log on load.
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    dom_script = """
    <script>
    window.addEventListener('load', () => {
        console.log("DOM-DUMP-START");
        const tabPages = document.querySelectorAll('.tab-page');
        tabPages.forEach(p => {
            let path = [];
            let curr = p;
            while(curr) {
                let nodeName = curr.nodeName.toLowerCase();
                let idStr = curr.id ? '#' + curr.id : '';
                let classStr = curr.className ? '.' + Array.from(curr.classList).join('.') : '';
                path.unshift(nodeName + idStr + classStr);
                curr = curr.parentElement;
            }
            console.log("DOM-PATH: " + path.join(" > "));
        });
        console.log("DOM-DUMP-END");
    });
    </script>
    """
    temp_html = html.replace("</body>", dom_script + "\n</body>")
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(temp_html)
        
    try:
        process = subprocess.Popen([
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--enable-logging",
            "--v=1",
            f"--log-file={log_file}",
            "http://127.0.0.1:5000/"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(4)
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            
    finally:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
            
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            log_content = f.read()
        lines = log_content.split('\n')
        print("\n--- DOM HIERARCHY FROM BROWSER ---")
        for line in lines:
            if 'DOM-PATH:' in line:
                print(line.split('DOM-PATH: ')[1])
        print("----------------------------------")
    else:
        print("Log file not created.")

if __name__ == '__main__':
    get_dom_hierarchy()
