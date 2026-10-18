import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the CSS for .wdes-hero to remove the SVG
old_css = """      background-image: 
        radial-gradient(ellipse at top right, rgba(67, 94, 191, 0.4) 0%, transparent 60%),
        radial-gradient(ellipse at bottom left, rgba(55, 81, 181, 0.4) 0%, transparent 60%),
        url("/static/network-bg.svg");"""
new_css = """      background-image: 
        radial-gradient(ellipse at top right, rgba(67, 94, 191, 0.4) 0%, transparent 60%),
        radial-gradient(ellipse at bottom left, rgba(55, 81, 181, 0.4) 0%, transparent 60%);"""
html = html.replace(old_css, new_css)

# 2. Inject the Video Tag
hero_tag = '<section class="wdes-hero pt-4 pb-6 px-4 sm:px-6 lg:px-8 relative overflow-hidden" id="heroSection">'
video_html = """
<section class="wdes-hero pt-4 pb-6 px-4 sm:px-6 lg:px-8 relative overflow-hidden" id="heroSection">
    <!-- Video Background (Optimized) -->
    <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover z-0 opacity-40 pointer-events-none">
      <source src="https://www.designesia.com/themes/cyberguard/video/1.mp4" type="video/mp4">
    </video>
    <!-- Dark overlay for text contrast -->
    <div class="absolute inset-0 bg-slate-900/60 z-0 pointer-events-none"></div>
"""
if '<video autoplay loop' not in html:
    html = html.replace(hero_tag, video_html)

# 3. Add relative z-10 to the content wrapper to appear above the video
html = html.replace('<div class="max-w-7xl mx-auto">', '<div class="max-w-7xl mx-auto relative z-10">')

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Video injected successfully!")
