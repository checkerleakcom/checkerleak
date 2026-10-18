from modal_template import generate_script_js

new_script = generate_script_js()

for path in ['app/static/billing.html', 'app/static/dashboard.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Clean out the misplaced script from the json-ld area
    # The misplaced script starts with `let currentCryptoMethod = 'USDT_TRC20';`
    pos = text.find("let currentCryptoMethod = 'USDT_TRC20';")
    while pos != -1 and pos < 25000: # It was inside json-ld before line 25000
        end_pos = text.find("</script>", pos)
        text = text[:pos] + text[end_pos:]
        print(f"Removed misplaced script from JSON-LD in {path}")
        pos = text.find("let currentCryptoMethod = 'USDT_TRC20';")

    # 2. Also remove any duplicate at the end if present
    pos_end = text.rfind("let currentCryptoMethod = 'USDT_TRC20';")
    if pos_end != -1:
        # Find the end of this block
        end_script = text.find("</script>", pos_end)
        text = text[:pos_end] + text[end_script:]
        print(f"Cleaned duplicate from bottom in {path}")

    # 3. Now insert the clean script right before the LAST `</script>` tag
    last_script_close = text.rfind("</script>")
    if last_script_close != -1:
        text = text[:last_script_close] + "\n\n" + new_script + "\n" + text[last_script_close:]
        print(f"Inserted clean script before last </script> in {path}")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

print("Saved cleanly to both files!")
