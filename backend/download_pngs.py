import os
import urllib.request
import time

domain_map = {
    'telegram': 'telegram.org', 'whatsapp': 'whatsapp.com', 'viber': 'viber.com',
    'imessage': 'apple.com', 'rcs': 'google.com', 'apple': 'apple.com',
    'facebook': 'facebook.com', 'amazon': 'amazon.com', 'instagram': 'instagram.com',
    'netflix': 'netflix.com', 'line': 'line.me', 'botim': 'botim.me',
    'linkedin': 'linkedin.com', 'zalo': 'zalo.me', 'vk': 'vk.com',
    'twitter': 'x.com', 'tiktok': 'tiktok.com', 'microsoft': 'microsoft.com',
    'snapchat': 'snapchat.com', 'messenger': 'messenger.com', 'threads': 'threads.net',
    'spotify': 'spotify.com', 'binance': 'binance.com', 'kucoin': 'kucoin.com',
    'htx': 'htx.com', 'coinw': 'coinw.com', 'cryptocom': 'crypto.com',
    'okx': 'okx.com', 'gmail': 'gmail.com', 'outlook': 'outlook.com',
    'yahoo': 'yahoo.com', 'yandex': 'yandex.com', 'mailru': 'mail.ru',
    'paypal': 'paypal.com', 'revolut': 'revolut.com', 'wise': 'wise.com',
    'cashapp': 'cash.app', 'signal': 'signal.org', 'github': 'github.com',
    'dhl': 'dhl.com', 'temu': 'temu.com', 'airbnb': 'airbnb.com',
    'discord': 'discord.com', 'glovo': 'glovoapp.com', 'talabat': 'talabat.com',
    'doordash': 'doordash.com', 'avito': 'avito.ru', 'okru': 'ok.ru',
    'kakaotalk': 'kakaocorp.com', 'wechat': 'wechat.com', 'grab': 'grab.com'
}

os.makedirs('app/static/logos', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0'}
success = 0

for icon, domain in domain_map.items():
    url = f"https://www.google.com/s2/favicons?sz=128&domain={domain}"
    out_path = f"app/static/logos/{icon}.png"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response, open(out_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded {icon}.png")
        success += 1
        time.sleep(0.1)
    except Exception as e:
        print(f"Failed {icon}: {e}")

print(f"Done! {success}/{len(domain_map)} downloaded.")
