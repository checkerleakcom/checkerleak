import re
from modal_template import generate_modal_html, generate_script_js

new_modal_html = generate_modal_html()
new_script_js = generate_script_js()

def update_page(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace the entire <div id="cryptoTopUpModal">...</div>
    # Locate from `<!-- ==================== CRYPTO TOP-UP MODAL` or `<div id="cryptoTopUpModal"`
    pattern_modal = r'(<!-- ==================== CRYPTO TOP-UP MODAL[\s\S]*?<\/div>\s*<\/div>\s*<\/div>)'
    if re.search(pattern_modal, content):
        content = re.sub(pattern_modal, new_modal_html, content, count=1)
        print(f"Replaced modal HTML in {file_path}")
    else:
        # Try finding `<div id="cryptoTopUpModal"`
        start = content.find('<div id="cryptoTopUpModal"')
        if start != -1:
            # find end
            end = content.find('<script src="https://unpkg.com/lucide@latest"></script>', start)
            if end != -1:
                content = content[:start] + new_modal_html + "\n\n  " + content[end:]
                print(f"Replaced modal HTML via substring in {file_path}")

    # 2. Replace the script functions: selectCryptoTab, copyCryptoAddress, submitCryptoPayment
    # Remove existing definitions of these functions
    funcs_to_remove = [
        r'function selectCryptoTab\(curr\)\s*\{[\s\S]*?^\s*\}',
        r'function copyCryptoAddress\(\)\s*\{[\s\S]*?^\s*\}',
        r'async function submitCryptoPayment\(\)\s*\{[\s\S]*?^\s*\}',
        r'function submitCryptoPayment\(\)\s*\{[\s\S]*?^\s*\}'
    ]
    for r_pat in funcs_to_remove:
        content = re.sub(r_pat, '', content, flags=re.MULTILINE)

    # Insert new script before </script>
    if "let currentCryptoMethod = 'USDT_TRC20';" not in content:
        content = content.replace("</script>", new_script_js + "\n</script>", 1)
        print(f"Inserted new JS functions into {file_path}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully saved {file_path}")

update_page("app/static/billing.html")
update_page("app/static/dashboard.html")
