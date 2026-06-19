import os
import sys

def filter_logs():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    log_file = "scratch/chrome_debug.log"
    if not os.path.exists(log_file):
        print("Log file not found.")
        return
        
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        log_content = f.read()
        
    lines = log_content.split('\n')
    print("--- FILTERED CHROME LOGS ---")
    for line in lines:
        if 'GL_INVALID_VALUE' in line:
            continue
        if 'CONSOLE' in line or 'error' in line.lower() or 'exception' in line.lower() or 'failed' in line.lower() or 'uncaught' in line.lower():
            # Safely encode and print
            print(line.encode('utf-8', errors='replace').decode('utf-8'))
            
if __name__ == '__main__':
    filter_logs()
