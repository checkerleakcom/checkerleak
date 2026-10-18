import re

for path in ['app/static/billing.html', 'app/static/dashboard.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Search for orphaned try { const response = await fetch('/api/v1/billing/submit-txid'
    pattern = r'const stored = localStorage\.getItem\("pulsecheck_client"\);\s*const email = stored \? JSON\.parse\(stored\)\.email : \'unknown\';\s*try \{\s*const response = await fetch\(\'/api/v1/billing/submit-txid\'[\s\S]*?showToast\("Network error\. Please try again\.", \'error\'\);\s*\}'
    
    match = re.search(pattern, text)
    if match:
        print(f"Found orphaned block in {path}: len={len(match.group(0))}")
        text = text[:match.start()] + text[match.end():]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Removed orphaned block from {path}")
    else:
        print(f"Orphaned block pattern not matched exactly in {path}")
