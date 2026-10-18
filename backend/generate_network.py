import random
import math

width, height = 800, 400
num_nodes = 120
max_dist = 85

nodes = []
for _ in range(num_nodes):
    x = random.randint(0, width)
    y = random.randint(0, height)
    nodes.append((x, y))

svg = [f'<svg width="100%" height="100%" preserveAspectRatio="xMidYMid slice" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">']
svg.append('<rect width="100%" height="100%" fill="#1e293b"/>')

# Draw lines
for i in range(num_nodes):
    x1, y1 = nodes[i]
    for j in range(i + 1, num_nodes):
        x2, y2 = nodes[j]
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < max_dist:
            opacity = 1.0 - (dist / max_dist)
            # chaotic random factor to some lines
            stroke_opacity = opacity * 0.15
            svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="rgba(255,255,255,{stroke_opacity:.3f})" stroke-width="{random.uniform(0.5, 1.5):.1f}"/>')

# Draw nodes
for x, y in nodes:
    svg.append(f'<circle cx="{x}" cy="{y}" r="{random.uniform(1.0, 2.5):.1f}" fill="rgba(255,255,255,0.2)"/>')

svg.append('</svg>')

with open('app/static/network-bg.svg', 'w') as f:
    f.write('\n'.join(svg))
print("SVG Generated.")
