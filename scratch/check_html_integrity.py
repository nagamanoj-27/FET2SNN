with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("File length:", len(content))
print("Ends with </html>?", content.strip().endswith('</html>'))
print("Last 100 characters of the file:")
print(repr(content[-100:]))
