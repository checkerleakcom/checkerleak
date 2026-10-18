import re
with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

cases = ['instagram', 'tiktok', 'kucoin', 'htx', 'binance', 'dhl', 'temu', 'airbnb']
for c in cases:
    m = re.search(f'case "{c}":\\s*return `(.*?)`;', text)
    if m:
        print(f'{c}: {m.group(1)[:50]}...')
    else:
        print(f'{c}: Not found')
