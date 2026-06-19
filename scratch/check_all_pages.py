import subprocess
import time
import os
import sys

def check_page(url, page_name):
    # Force sys.stdout to handle UTF-8 to print emojis correctly on Windows console
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    log_file = os.path.abspath(f"scratch/chrome_debug_{page_name}.log")
    if os.path.exists(log_file):
        os.remove(log_file)
        
    print(f"Checking {page_name} at {url}...")
    process = subprocess.Popen([
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--enable-logging",
        "--v=1",
        f"--log-file={log_file}",
        url
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    time.sleep(3)
    
    process.terminate()
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        process.kill()
        
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()
        lines = log_content.split('\n')
        errors = []
        for line in lines:
            if 'GL_INVALID_VALUE' in line:
                continue
            if 'CONSOLE' in line or 'error' in line.lower() or 'exception' in line.lower() or 'failed' in line.lower() or 'uncaught' in line.lower():
                errors.append(line)
        if errors:
            print(f"--- LOGS FOR {page_name} ---")
            for err in errors:
                print(err.encode('utf-8', errors='replace').decode('utf-8'))
            print("----------------------------\n")
        else:
            print(f"{page_name}: Clean (0 console messages/errors)\n")
    else:
        print(f"Could not create log file for {page_name}.\n")

if __name__ == '__main__':
    pages = [
        ("http://127.0.0.1:5000/codesign.html", "codesign"),
        ("http://127.0.0.1:5000/tcad_viewer.html", "tcad_viewer"),
        ("http://127.0.0.1:5000/sweep.html", "sweep"),
        ("http://127.0.0.1:5000/model_cards.html", "model_cards"),
        ("http://127.0.0.1:5000/fet2snn_comparison.html", "comparison")
    ]
    for url, name in pages:
        check_page(url, name)
