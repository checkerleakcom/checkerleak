import re

with open('backend/full_getBrandSvg.js', 'r', encoding='utf-8') as f:
    js_func = f.read()

with open('backend/app/static/index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

pos_start = idx.find('const ALL_SERVICES = [')
pos_end = idx.find('];', pos_start)
services_code = idx[pos_start:pos_end+2]

items = []
for line in services_code.splitlines():
    line = line.strip()
    if line.startswith('{') and 'id:' in line:
        id_m = re.search(r'id:\s*["\']([^"\']+)["\']', line)
        name_m = re.search(r'name:\s*["\']([^"\']+)["\']', line)
        icon_m = re.search(r'icon:\s*["\']([^"\']+)["\']', line)
        cat_m = re.search(r'cat:\s*["\']([^"\']+)["\']', line)
        if id_m and name_m and icon_m:
            items.append((id_m.group(1), name_m.group(1), icon_m.group(1), cat_m.group(1) if cat_m else ''))

# Extract cases
cases = dict(re.findall(r'case\s+["\']([^"\']+)["\']:\s*return\s*[`"\'](.*?)[`"\'];', js_func, re.DOTALL))

print(f"Total services in ALL_SERVICES: {len(items)}")
print(f"Total cases in getBrandSvg: {len(cases)}")

# Let's inspect the SVGs of all services
for i, (sid, name, icon, cat) in enumerate(items, 1):
    svg = cases.get(icon, 'DEFAULT_LUCIDE_FALLBACK')
    # Check if this SVG is generic (e.g. circle with text, or lucide path, or generic icon)
    is_text_only = '<text' in svg and not any(tag in svg for tag in ['<path', '<defs', '<linearGradient'])
    is_stroke_only = 'fill="none"' in svg and 'stroke="currentColor"' in svg
    print(f"{i:3d}. {sid:28} | {name:32} | icon: {icon:16} | svg_len: {len(svg):4d} | {'STROKE_ONLY' if is_stroke_only else ('TEXT_ONLY' if is_text_only else 'BRAND')}")
