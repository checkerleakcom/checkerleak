import re
with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

cases = ['kucoin', 'binance', 'htx']
for c in cases:
    m = re.search(f'case "{c}":\\s*return `(.*?)`;', text)
    if m:
        print(f'{c}: {m.group(1)}')
