with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    d = f.read()

d = d.replace('<a href="/" class="flex items-center gap-2.5">', '<a href="/dashboard" class="flex items-center gap-2.5">')

with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(d)
