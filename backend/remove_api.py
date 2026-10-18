import re

with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    d = f.read()

# 1. Change grid-cols-3 to grid-cols-2
d = d.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-4">', '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">')

# 2. Remove Tool 03 block
tool3_pattern = r'<div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between\s+cursor-pointer hover:border-\[#435ebf\] transition" onclick="openDeveloperModal\(\)">.*?</div>\s+</div>'
d = re.sub(tool3_pattern, '</div>', d, flags=re.DOTALL)

# 3. Change col-span-8 to col-span-12
d = d.replace('lg:col-span-8 bg-white rounded-2xl', 'lg:col-span-12 bg-white rounded-2xl')

# 4. Remove API Quickstart Card
api_card_pattern = r'<!-- API Quickstart Card -->.*?</button>\s+</div>'
d = re.sub(api_card_pattern, '', d, flags=re.DOTALL)

# 5. Remove API KEY from wallet bar
api_key_pattern = r'<div class="flex items-center gap-2 mt-2 text-xs text-slate-600">\s*<span class="text-slate-400 font-mono text-\[11px\]">API KEY:</span>.*?</div>'
d = re.sub(api_key_pattern, '', d, flags=re.DOTALL)

with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(d)
print("Removed API clutter!")
