import os

wallet_address = "TQoCuYoSMadJRo18K6D6HMrZEjb8zTFygN"
old_wallet = "T9yD...[USER_WILL_PROVIDE_HASH]...Xz"

files_to_check = [
    'app/static/dashboard.html',
    'app/static/billing.html',
    'app/static/index.html',
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the displayed text and the copy string
        if old_wallet in content:
            content = content.replace(old_wallet, wallet_address)
            # Make sure we also fix the copy button so it copies the right one
            content = content.replace(f"navigator.clipboard.writeText('{old_wallet}')", f"navigator.clipboard.writeText('{wallet_address}')")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filepath}")
