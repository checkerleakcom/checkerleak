import re

css_bg = '''.wdes-hero {
      background-color: #1e293b;
      background-image: 
        radial-gradient(ellipse at top right, rgba(67, 94, 191, 0.4) 0%, transparent 60%),
        radial-gradient(ellipse at bottom left, rgba(55, 81, 181, 0.4) 0%, transparent 60%),
        url("/static/network-bg.svg");
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
      color: #ffffff;
    }'''

files = ['app/static/index.html', 'app/templates/product_page.html', 'app/templates/category_page.html']
for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace .wdes-hero block
        content = re.sub(r'\.wdes-hero\s*\{[^}]+\}', css_bg, content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except FileNotFoundError:
        pass
print('Done updating backgrounds!')
