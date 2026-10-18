for path in ['app/static/billing.html', 'app/static/dashboard.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    bad_seq = """function closeCryptoModal() {
      document.getElementById('cryptoTopUpModal').classList.add('hidden');
    }

    

      
    }"""

    good_seq = """function closeCryptoModal() {
      document.getElementById('cryptoTopUpModal').classList.add('hidden');
    }"""

    if bad_seq in text:
        text = text.replace(bad_seq, good_seq)
        print(f"Removed dangling brace in {path}")
    else:
        # Regex replacement
        import re
        text = re.sub(r'function closeCryptoModal\(\) \{\s*document\.getElementById\(\'cryptoTopUpModal\'\)\.classList\.add\(\'hidden\'\);\s*\}\s*\}', good_seq, text)
        print(f"Regex replaced dangling brace in {path}")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved {path}")
