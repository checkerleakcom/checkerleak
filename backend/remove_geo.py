import os

filepath = 'app/static/index.html'

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # 1. Remove HTML Section
    start_html = '<!-- ==================== GEO & TELECOM INTELLIGENCE HUB ==================== -->'
    end_html = '<!-- ==================== ENTERPRISE COMPLIANCE & SECURITY BADGES ==================== -->'
    
    start_idx = html.find(start_html)
    end_idx = html.find(end_html)
    
    if start_idx != -1 and end_idx != -1:
        html = html[:start_idx] + html[end_idx:]
        
    # 2. Remove JS Section
    start_js = '// ==================== GEO & TELECOM INTELLIGENCE ===================='
    end_js = '// ==================== SEO FAQ ACCORDION ===================='
    
    start_j_idx = html.find(start_js)
    end_j_idx = html.find(end_js)
    
    if start_j_idx != -1 and end_j_idx != -1:
        html = html[:start_j_idx] + html[end_j_idx:]
        
    # 3. Remove function call
    html = html.replace('autoDetectVisitorGeo();', '')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Geo Intelligence section removed successfully!")
else:
    print("File not found")
