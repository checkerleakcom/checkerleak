import os

with open('app/main.py', 'r', encoding='utf-8') as f:
    main_code = f.read()

# Add import if missing
if 'from fastapi.staticfiles import StaticFiles' not in main_code:
    main_code = main_code.replace('from fastapi.responses import HTMLResponse, FileResponse', 
                                  'from fastapi.responses import HTMLResponse, FileResponse\nfrom fastapi.staticfiles import StaticFiles')

# Add mount
if 'app.mount("/static"' not in main_code:
    mount_code = """
app.include_router(geo_router)
app.include_router(seo_router)

# Mount static folder for assets like logos, css, images
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
"""
    main_code = main_code.replace("""
app.include_router(geo_router)
app.include_router(seo_router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
""", mount_code)

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(main_code)
