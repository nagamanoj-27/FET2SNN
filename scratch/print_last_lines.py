with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines[-20:]:
    print(line.encode('ascii', 'replace').decode('ascii'), end='')
