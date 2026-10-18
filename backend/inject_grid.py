import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Extract ALL_SERVICES block
services_js = re.search(r'const ALL_SERVICES = \[.*?\];', idx, re.DOTALL).group(0)

# Extract renderServicesDirectory block
render_js = re.search(r'function renderServicesDirectory\(\) \{.*?\n      \}', idx, re.DOTALL).group(0)

# Extract helper functions
get_svg_js = re.search(r'function getBrandSvg\(brand, size = 18\) \{.*?\}', idx, re.DOTALL).group(0)
render_badge_js = re.search(r'function renderBadge\(badge\) \{.*?\}', idx, re.DOTALL).group(0)

html_block = """
<!-- FULL SERVICES DIRECTORY -->
<div class="mt-8 bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
  <div class="p-6 border-b border-slate-100">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
      <div class="relative flex-1">
        <i data-lucide="search" class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400"></i>
        <input type="text" id="serviceSearchInput" onkeyup="filterServicesDirectory()" placeholder="Search for WhatsApp, Binance, Revolut..." class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:bg-white focus:ring-2 focus:ring-[#435ebf] focus:outline-none transition">
      </div>
      <div class="flex items-center gap-2 text-xs font-mono text-slate-500 shrink-0">
        <span>SHOWING:</span>
        <span id="serviceCountBadge" class="font-bold text-[#435ebf] px-2.5 py-1 rounded bg-blue-50 border border-blue-100">102 Checkers</span>
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-1.5 pt-2" id="directoryCategoryFilters">
      <button onclick="setDirectoryCategory('ALL')" id="catBtn_ALL" class="cat-pill active px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-800 text-white">All Engines (102)</button>
      <button onclick="setDirectoryCategory('SOCIAL_MESSAGING')" id="catBtn_SOCIAL_MESSAGING" class="cat-pill inactive px-3 py-1.5 rounded-lg text-xs font-semibold transition text-slate-600 hover:bg-slate-100">Messengers</button>
      <button onclick="setDirectoryCategory('CRYPTO_EXCHANGE')" id="catBtn_CRYPTO_EXCHANGE" class="cat-pill inactive px-3 py-1.5 rounded-lg text-xs font-semibold transition text-slate-600 hover:bg-slate-100">Crypto</button>
      <button onclick="setDirectoryCategory('EMAIL_VERIFICATION')" id="catBtn_EMAIL_VERIFICATION" class="cat-pill inactive px-3 py-1.5 rounded-lg text-xs font-semibold transition text-slate-600 hover:bg-slate-100">Email</button>
      <button onclick="setDirectoryCategory('FINTECH_PAYMENTS')" id="catBtn_FINTECH_PAYMENTS" class="cat-pill inactive px-3 py-1.5 rounded-lg text-xs font-semibold transition text-slate-600 hover:bg-slate-100">FinTech</button>
    </div>
  </div>
  <div class="p-6 overflow-y-auto bg-slate-50 max-h-[800px]">
    <div id="servicesDirectoryContainer" class="space-y-6">
      <!-- Rendered dynamically -->
    </div>
  </div>
</div>
"""

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

# Replace handleServiceClick to link to product page
js_block = js_block.replace("onclick=\"handleServiceClick('${s.id}')\"", "onclick=\"window.location.href='/products/' + s.id.replace(/_/g, '-')\"")


with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    d = f.read()

# Only inject if not already injected
if 'id="servicesDirectoryContainer"' not in d:
    d = d.replace('<!-- Active Job / File Processing Tracker -->', html_block + '\n\n        <!-- Active Job / File Processing Tracker -->')
    d = d.replace('</script>\n</body>', js_block + '\n</script>\n</body>')

    with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(d)
    print('Done integrating grid into dashboard!')
else:
    print('Already injected')
