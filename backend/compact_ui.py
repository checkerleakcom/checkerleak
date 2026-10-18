with open('app/static/index.html', 'r', encoding='utf-8') as f:
    d = f.read()

# 1. Reduce hero section padding
d = d.replace('class="wdes-hero pt-8 pb-12', 'class="wdes-hero pt-4 pb-6')

# 2. Reduce space-y in the text container
d = d.replace('<div class="max-w-3xl mx-auto text-center space-y-5">', '<div class="max-w-3xl mx-auto text-center space-y-3">')

# 3. Reduce margin-top of the visual preview frame
d = d.replace('<div class="mt-8 max-w-4xl mx-auto relative" id="live-tester">', '<div class="mt-4 max-w-4xl mx-auto relative" id="live-tester">')

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(d)


with open('app/templates/product_page.html', 'r', encoding='utf-8') as f:
    p = f.read()

p = p.replace('class="wdes-hero pt-8 pb-12', 'class="wdes-hero pt-4 pb-6')
p = p.replace('<div class="max-w-4xl mx-auto text-center space-y-5">', '<div class="max-w-4xl mx-auto text-center space-y-3">')
p = p.replace('mt-8 max-w-4xl mx-auto', 'mt-4 max-w-4xl mx-auto')

with open('app/templates/product_page.html', 'w', encoding='utf-8') as f:
    f.write(p)
