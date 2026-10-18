with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    d = f.read()

new_checker = '{ id: "custom_crypto_email_checker", cost: 3, name: "Custom Crypto Email", cat: "CRYPTO_EXCHANGE", catTitle: "CRYPTO EXCHANGE CHECKERS", badge: "NEW", icon: "generic_crypto", target: "Email", desc: "Custom crypto exchange account verification by email." },'

if 'custom_crypto_email_checker' not in d:
    # Insert right after kucoin_email_checker
    d = d.replace('{ id: "kucoin_email_checker"', new_checker + '\n      { id: "kucoin_email_checker"')
    with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(d)
        
with open('app/static/index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

if 'custom_crypto_email_checker' not in idx:
    # Insert right after kucoin_email_checker
    idx = idx.replace('{ id: "kucoin_email_checker"', new_checker + '\n      { id: "kucoin_email_checker"')
    with open('app/static/index.html', 'w', encoding='utf-8') as f:
        f.write(idx)
print('Added generic checker')
