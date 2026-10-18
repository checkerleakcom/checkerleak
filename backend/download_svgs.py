import os
import re
import urllib.request
import time

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

icons = re.findall(r'icon:\s*"([^"]+)"', text)
unique_icons = set(icons)

# Map our icon names to SimpleIcons slugs
slug_map = {
    'telegram': 'telegram',
    'whatsapp': 'whatsapp',
    'viber': 'viber',
    'imessage': 'apple',
    'rcs': 'googlemessages',
    'apple': 'apple',
    'facebook': 'facebook',
    'amazon': 'amazon',
    'instagram': 'instagram',
    'netflix': 'netflix',
    'line': 'line',
    'botim': 'viber', # botim doesn't exist on simpleicons, fallback to something
    'linkedin': 'linkedin',
    'zalo': 'zalo',
    'vk': 'vk',
    'twitter': 'x',
    'tiktok': 'tiktok',
    'microsoft': 'microsoft',
    'snapchat': 'snapchat',
    'messenger': 'messenger',
    'threads': 'threads',
    'spotify': 'spotify',
    'binance': 'binance',
    'kucoin': 'kucoin',
    'htx': 'huobi',
    'coinw': 'coinbase', # fallback
    'cryptocom': 'crypto.com',
    'okx': 'okx',
    'gmail': 'gmail',
    'outlook': 'microsoftoutlook',
    'yahoo': 'yahoo',
    'yandex': 'yandex',
    'mailru': 'mail.ru',
    'paypal': 'paypal',
    'revolut': 'revolut',
    'wise': 'wise',
    'cashapp': 'cashapp',
    'signal': 'signal',
    'github': 'github',
    'dhl': 'dhl',
    'temu': 'temu',
    'airbnb': 'airbnb',
    'discord': 'discord',
    'glovo': 'glovo',
    'talabat': 'talabat',
    'doordash': 'doordash',
    'avito': 'avito',
    'okru': 'okcupid', # fallback
    'kakaotalk': 'kakaotalk',
    'wechat': 'wechat',
    'grab': 'grab'
}

os.makedirs('app/static/logos', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0'}

success_count = 0
for icon in unique_icons:
    slug = slug_map.get(icon)
    if not slug:
        continue
    
    url = f"https://cdn.simpleicons.org/{slug}"
    out_path = f"app/static/logos/{icon}.svg"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response, open(out_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded {icon}.svg")
        success_count += 1
        time.sleep(0.1)
    except Exception as e:
        print(f"Failed {icon}: {e}")

print(f"Done! {success_count}/{len(unique_icons)} downloaded.")
