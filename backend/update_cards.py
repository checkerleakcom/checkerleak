import re
with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace WhatsApp SVG
wa_svg = re.search(r'(<div class="w-12 h-12 rounded-xl bg-emerald-50.*?>\s*)<svg.*?cx="12".*?#25D366.*?</svg>', html, re.DOTALL)
if wa_svg:
    html = html.replace(wa_svg.group(0), wa_svg.group(1) + '<img src="/static/logos/whatsapp.png" class="w-8 h-8 object-contain" alt="WhatsApp">')

# Replace Apple SVG
ap_svg = re.search(r'(<div class="w-12 h-12 rounded-xl bg-blue-50.*?>\s*)<svg.*?cx="12".*?#000.*?</svg>', html, re.DOTALL)
if ap_svg:
    html = html.replace(ap_svg.group(0), ap_svg.group(1) + '<img src="/static/logos/apple.png" class="w-8 h-8 object-contain" alt="Apple">')

# Replace Telegram SVG
tg_svg = re.search(r'(<div class="w-12 h-12 rounded-xl bg-sky-50.*?>\s*)<svg.*?cx="12".*?#2AABEE.*?</svg>', html, re.DOTALL)
if tg_svg:
    html = html.replace(tg_svg.group(0), tg_svg.group(1) + '<img src="/static/logos/telegram.png" class="w-8 h-8 object-contain" alt="Telegram">')

# Replace Binance SVG
bi_svg = re.search(r'(<div class="w-12 h-12 rounded-xl bg-amber-50.*?>\s*)<svg.*?#F3BA2F.*?</svg>', html, re.DOTALL)
if bi_svg:
    html = html.replace(bi_svg.group(0), bi_svg.group(1) + '<img src="/static/logos/binance.png" class="w-8 h-8 object-contain" alt="Binance">')

# Replace Revolut SVG
rv_svg = re.search(r'(<div class="w-12 h-12 rounded-xl bg-slate-900.*?>\s*)<svg.*?cx="12".*?#000.*?R.*?</svg>', html, re.DOTALL)
if rv_svg:
    # Since Revolut is dark mode (bg-slate-900), the image might have a white background if we downloaded a white version? 
    # Actually, Google Favicon PNG is usually transparent and colored. Let's make the background white instead of slate-900 to ensure the logo shows well.
    html = html.replace(rv_svg.group(0), '<div class="w-12 h-12 rounded-xl bg-white border border-slate-200 flex items-center justify-center font-bold">\n                <img src="/static/logos/revolut.png" class="w-8 h-8 object-contain drop-shadow-sm" alt="Revolut">')

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Replaced inline SVGs with PNGs!')
