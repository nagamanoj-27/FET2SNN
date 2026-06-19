import subprocess
import time
import os
import sys

def run_chrome_and_get_logs():
    # Force sys.stdout to handle UTF-8 to print emojis correctly on Windows console
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    log_file = os.path.abspath("scratch/chrome_debug.log")
    if os.path.exists(log_file):
        os.remove(log_file)
        
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
    
    time.sleep(5)
    
    print("Terminating Chrome...")
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        
    if os.path.exists(log_file):
        print(f"Log file created successfully.")
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()
        print("\n--- CHROME LOGS (UTF-8) ---")
        lines = log_content.split('\n')
        for line in lines:
            if 'CONSOLE' in line or 'error' in line.lower() or 'exception' in line.lower() or 'failed' in line.lower():
                # Print using safe utf-8 representation or encode/decode
                safe_line = line.encode('utf-8', errors='replace').decode('utf-8')
                print(safe_line)
        print("-------------------")
    else:
        print("Log file was not created.")

if __name__ == '__main__':
    run_chrome_and_get_logs()
