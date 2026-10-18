with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    d = f.read()

d = d.replace('class="p-6 overflow-y-auto bg-slate-50 max-h-[800px]"', 'class="p-6 bg-slate-50"')

with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(d)
print('Scrollbar removed!')
