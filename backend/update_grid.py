with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's replace the inner HTML generation of renderBeautifulGrid
old_js = """              <div class="mb-2.5 transition-transform duration-300 group-hover:scale-110 flex items-center justify-center">
                ${getBrandSvg(s.icon, 40)}
              </div>"""
              
new_js = """              <div class="mb-2.5 transition-transform duration-300 group-hover:scale-110 flex items-center justify-center h-10 w-10">
                <img src="/static/logos/${s.icon}.svg" class="w-10 h-10 object-contain" alt="${s.name}" onerror="this.onerror=null; this.outerHTML=getBrandSvg('${s.icon}', 40)" />
              </div>"""

html = html.replace(old_js, new_js)

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
