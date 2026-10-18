import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import date
from app.core.universal_engine import UniversalCheckerEngine
from app.core.services_catalog import ServiceCategory
from app.api.seo_router import slugify

def build_sitemap():
    engine = UniversalCheckerEngine()
    today = date.today().isoformat()

    categories = [slugify(c.name) for c in ServiceCategory]
    
    products = []
    seen_slugs = set()
    for sid, srv in engine._services_map.items():
        s = slugify(srv.name)
        if s not in seen_slugs:
            seen_slugs.add(s)
            products.append((s, srv.name))

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    lines.append('')
    lines.append('  <!-- Primary Landing Page with International Hreflang -->')
    lines.append('  <url>')
    lines.append('    <loc>https://checkerleak.com/</loc>')
    lines.append(f'    <lastmod>{today}</lastmod>')
    lines.append('    <changefreq>daily</changefreq>')
    lines.append('    <priority>1.0</priority>')
    lines.append('    <xhtml:link rel="alternate" hreflang="x-default" href="https://checkerleak.com/" />')
    lines.append('    <xhtml:link rel="alternate" hreflang="en" href="https://checkerleak.com/" />')
    lines.append('    <xhtml:link rel="alternate" hreflang="es" href="https://checkerleak.com/?lang=es" />')
    lines.append('    <xhtml:link rel="alternate" hreflang="pt" href="https://checkerleak.com/?lang=pt" />')
    lines.append('    <xhtml:link rel="alternate" hreflang="id" href="https://checkerleak.com/?lang=id" />')
    lines.append('    <xhtml:link rel="alternate" hreflang="de" href="https://checkerleak.com/?lang=de" />')
    lines.append('    <xhtml:link rel="alternate" hreflang="tr" href="https://checkerleak.com/?lang=tr" />')
    lines.append('    <xhtml:link rel="alternate" hreflang="ru" href="https://checkerleak.com/?lang=ru" />')
    lines.append('    <xhtml:link rel="alternate" hreflang="zh-CN" href="https://checkerleak.com/?lang=zh-CN" />')
    lines.append('  </url>')
    lines.append('')
    lines.append('  <!-- Developer Documentation -->')
    lines.append('  <url>')
    lines.append('    <loc>https://checkerleak.com/docs</loc>')
    lines.append(f'    <lastmod>{today}</lastmod>')
    lines.append('    <changefreq>weekly</changefreq>')
    lines.append('    <priority>0.85</priority>')
    lines.append('  </url>')
    lines.append('')
    lines.append('  <!-- Generative Engine Optimization (GEO) Endpoints -->')
    lines.append('  <url>')
    lines.append('    <loc>https://checkerleak.com/llms.txt</loc>')
    lines.append(f'    <lastmod>{today}</lastmod>')
    lines.append('    <changefreq>weekly</changefreq>')
    lines.append('    <priority>0.80</priority>')
    lines.append('  </url>')
    lines.append('  <url>')
    lines.append('    <loc>https://checkerleak.com/llms-full.txt</loc>')
    lines.append(f'    <lastmod>{today}</lastmod>')
    lines.append('    <changefreq>weekly</changefreq>')
    lines.append('    <priority>0.75</priority>')
    lines.append('  </url>')
    lines.append('')
    lines.append('  <!-- Geo Telecom Hubs -->')
    for geo in ['MA', 'FR', 'US', 'AE', 'GB', 'SA', 'DE', 'BR', 'ID']:
        lines.append('  <url>')
        lines.append(f'    <loc>https://checkerleak.com/?geo={geo}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        lines.append('    <changefreq>weekly</changefreq>')
        lines.append('    <priority>0.75</priority>')
        lines.append('  </url>')
    lines.append('')
    lines.append('  <!-- Programmatic Category Hubs -->')
    for cat in sorted(categories):
        lines.append('  <url>')
        lines.append(f'    <loc>https://checkerleak.com/categories/{cat}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        lines.append('    <changefreq>weekly</changefreq>')
        lines.append('    <priority>0.85</priority>')
        lines.append('  </url>')
    lines.append('')
    lines.append('  <!-- Programmatic Product & Engine Pages (102 Engines) -->')
    for slug, name in sorted(products, key=lambda x: x[0]):
        lines.append('  <url>')
        lines.append(f'    <loc>https://checkerleak.com/products/{slug}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        lines.append('    <changefreq>weekly</changefreq>')
        lines.append('    <priority>0.80</priority>')
        lines.append('  </url>')
    lines.append('')
    lines.append('</urlset>')

    sitemap_content = '\n'.join(lines) + '\n'
    out_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'sitemap.xml')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f'Successfully wrote complete sitemap.xml to {out_path} with {len(lines)} lines and {len(products)} products.')

if __name__ == '__main__':
    build_sitemap()
