with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace .svg with .png in the image tag
old_js = """<img src="/static/logos/${s.icon}.svg" class="w-10 h-10 object-contain" alt="${s.name}" onerror="this.onerror=null; this.outerHTML=getBrandSvg('${s.icon}', 40)" />"""
new_js = """<img src="/static/logos/${s.icon}.png" class="w-10 h-10 object-contain drop-shadow-sm" alt="${s.name}" onerror="this.onerror=null; this.outerHTML=getBrandSvg('${s.icon}', 40)" />"""

html = html.replace(old_js, new_js)

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
