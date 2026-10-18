with open('app/static/index.html', 'r', encoding='utf-8') as f:
    d = f.read()
    start = d.find('function getBrandSvg')
    end = d.find('function renderGeoProfile')
with open('svgs_out.txt', 'w', encoding='utf-8') as f:
    f.write(d[start:end])
