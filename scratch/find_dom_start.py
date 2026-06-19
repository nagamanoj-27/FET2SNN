import subprocess

def find_drop():
    # Run check_html_nesting_fixed.py and look at lines 1350 to 1410
    # We can just import and run it, capturing its stdout, or rewrite a smaller snippet.
    from scratch.check_html_nesting_fixed import trace_nesting
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    trace_nesting()
    
    sys.stdout = old_stdout
    output = mystdout.getvalue()
    
    lines = output.split('\n')
    for line in lines:
        # Match line numbers between 1350 and 1410
        import re
        m = re.match(r'Line\s+(\d+)', line)
        if m:
            l_num = int(m.group(1))
            if 1350 <= l_num <= 1410:
                print(line)

if __name__ == '__main__':
    find_drop()
