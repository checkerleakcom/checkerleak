import re
with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

cases = re.findall(r'case "(.*?)":', text)
print(cases)
