with open('app/main.py', 'r', encoding='utf-8') as f:
    m = f.read()

billing_route = """
BILLING_PATH = os.path.join(STATIC_DIR, "billing.html")
@app.get("/billing", include_in_schema=False)
async def serve_billing():
    if os.path.exists(BILLING_PATH):
        return FileResponse(BILLING_PATH)
    return {"message": "Billing not found."}
"""

if '/billing' not in m:
    m = m.replace('return {"message": "Dashboard not found."}', 'return {"message": "Dashboard not found."}\n' + billing_route)
    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(m)
    print("Added /billing to main.py")
