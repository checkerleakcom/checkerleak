import re

svg = """
        case "generic_crypto":
          return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-600"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v8"></path><path d="M8 12h8"></path></svg>`;
"""

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        d = f.read()
    if 'case "generic_crypto":' not in d:
        d = d.replace('switch (brand) {', 'switch (brand) {\n' + svg)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(d)

update_file('app/static/dashboard.html')
update_file('app/static/index.html')
print("Added generic_crypto SVG")
