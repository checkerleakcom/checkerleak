import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

def get_block(start_str):
    start = idx.find(start_str)
    if start == -1: return ""
    braces = 0
    end = -1
    for i in range(start, len(idx)):
        if idx[i] == '{':
            braces += 1
        elif idx[i] == '}':
            braces -= 1
            if braces == 0:
                end = i + 1
                break
    return idx[start:end]

render_js = get_block('function renderServicesDirectory() {')
get_svg_js = get_block('function getBrandSvg(brand, size = 18) {')
render_badge_js = get_block('function renderBadge(badge) {')

# Same for ALL_SERVICES array
start_arr = idx.find('const ALL_SERVICES = [')
brackets = 0
end_arr = -1
for i in range(start_arr, len(idx)):
    if idx[i] == '[':
        brackets += 1
    elif idx[i] == ']':
        brackets -= 1
        if brackets == 0:
            end_arr = i + 2 # to include ];
            break
services_js = idx[start_arr:end_arr]

with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    d = f.read()

# Clean out the broken injected JS block
broken_start = d.find("let currentDirCategory = 'ALL';")
if broken_start != -1:
    d = d[:broken_start] + '\n</script>\n</body>\n</html>'

js_block = f"""
let currentDirCategory = 'ALL';
let currentDirSearch = '';

{services_js}

{get_svg_js}

{render_badge_js}

{render_js}

function setDirectoryCategory(cat) {{
  currentDirCategory = cat;
  document.querySelectorAll('.cat-pill').forEach(btn => {{
    btn.className = (btn.id === 'catBtn_' + cat) 
      ? 'cat-pill active px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-800 text-white' 
      : 'cat-pill inactive px-3 py-1.5 rounded-lg text-xs font-semibold transition text-slate-600 hover:bg-slate-100';
  }});
  renderServicesDirectory();
}}

function filterServicesDirectory() {{
  currentDirSearch = document.getElementById('serviceSearchInput').value;
  renderServicesDirectory();
}}

document.addEventListener('DOMContentLoaded', () => {{
    renderServicesDirectory();
}});
"""

js_block = js_block.replace("onclick=\"handleServiceClick('${s.id}')\"", "onclick=\"window.location.href='/products/' + s.id.replace(/_/g, '-')\"")

d = d.replace('</script>\n</body>\n</html>', js_block + '\n</script>\n</body>\n</html>')

with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(d)
print('Fixed dashboard JS properly this time!')
