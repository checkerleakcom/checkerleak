with open('app/static/index.html', 'r', encoding='utf-8') as f:
    d = f.read()

# 1. Reduce top padding of the hero section
d = d.replace('class="wdes-hero pt-14 pb-20 px-4 sm:px-6 lg:px-8 relative overflow-hidden"', 
              'class="wdes-hero pt-8 pb-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden"')

# 2. Reduce margin-top of the console wrapper
d = d.replace('<div class="mt-12 max-w-4xl mx-auto relative" id="live-tester">', 
              '<div class="mt-8 max-w-4xl mx-auto relative" id="live-tester">')

# 3. Fix Floating Chip Left (move it up so it doesn't overlap)
d = d.replace('absolute -left-8 top-12 wdes-chip', 'absolute -left-6 -top-4 wdes-chip')

# 4. Fix Floating Chip Right (move it out so it doesn't overlap)
d = d.replace('absolute -right-6 bottom-16 wdes-chip', 'absolute -right-6 bottom-8 wdes-chip')

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(d)
    
print("Hero section adjusted!")
