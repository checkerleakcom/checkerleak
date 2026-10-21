"""
FastAPI Main Application Entrypoint.
Production-ready configuration with CORS, auth endpoints, static SPA mounting, and OpenAPI documentation.
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api.router import router
from app.api.auth_router import auth_router
from app.api.billing_router import router as billing_router
from app.api.developer_router import router as developer_router
from app.api.batch_upload_router import router as batch_upload_router
from app.api.geo_router import geo_router
from app.api.seo_router import router as seo_router
from app.api.blog_router import blog_router
from app.api.admin_router import admin_router

app = FastAPI(
    title="Next-Gen Contact Intelligence API",
    description="High-concurrency bulk phone number and multi-platform identity validation platform. Outperforms NumberChecker.AI with smart cascading cost optimization.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Cross-Origin Resource Sharing (CORS) - Hardened for production & local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "https://checkerleak.com",
        "https://www.checkerleak.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://leakchecker.com",
        "https://www.leakchecker.com"
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enterprise Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

app.include_router(router)
app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(billing_router, prefix="/api")
app.include_router(developer_router)
app.include_router(batch_upload_router)
app.include_router(geo_router)
app.include_router(seo_router)
app.include_router(blog_router)
app.include_router(admin_router)

# Mount static folder for assets like logos, css, images
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
INDEX_PATH = os.path.join(STATIC_DIR, "index.html")
ROBOTS_PATH = os.path.join(STATIC_DIR, "robots.txt")
SITEMAP_PATH = os.path.join(STATIC_DIR, "sitemap.xml")
LLMS_PATH = os.path.join(STATIC_DIR, "llms.txt")
LLMS_FULL_PATH = os.path.join(STATIC_DIR, "llms-full.txt")


DASHBOARD_PATH = os.path.join(STATIC_DIR, "dashboard.html")

@app.get("/", include_in_schema=False)
async def serve_index():
    """Serves the public landing page."""
    if os.path.exists(INDEX_PATH):
        return FileResponse(INDEX_PATH)
    return {"message": "API Online."}

@app.get("/dashboard", include_in_schema=False)
async def serve_dashboard():
    """Serves the CheckerLeak client portal."""
    if os.path.exists(DASHBOARD_PATH):
        return FileResponse(DASHBOARD_PATH)
    return {"message": "Dashboard not found."}

BILLING_PATH = os.path.join(STATIC_DIR, "billing.html")
@app.get("/billing", include_in_schema=False)
async def serve_billing():
    if os.path.exists(BILLING_PATH):
        return FileResponse(BILLING_PATH)
    return {"message": "Billing not found."}

ADMIN_PATH = os.path.join(STATIC_DIR, "admin.html")
@app.get("/admin", include_in_schema=False)
@app.get("/admin/login", include_in_schema=False)
async def serve_admin():
    if os.path.exists(ADMIN_PATH):
        return FileResponse(ADMIN_PATH)
    return {"message": "Admin interface not found."}



@app.get("/robots.txt", include_in_schema=False)
async def serve_robots_txt():
    """Serves crawler guidance for Googlebot, Bingbot, and AI search crawlers."""
    if os.path.exists(ROBOTS_PATH):
        return FileResponse(ROBOTS_PATH, media_type="text/plain")
    return FileResponse(INDEX_PATH)


@app.get("/sitemap.xml", include_in_schema=False)
async def serve_sitemap_xml():
    """Serves canonical XML sitemap for search engine indexation."""
    if os.path.exists(SITEMAP_PATH):
        return FileResponse(SITEMAP_PATH, media_type="application/xml")
    return FileResponse(INDEX_PATH)


@app.get("/llms.txt", include_in_schema=False)
async def serve_llms_txt():
    """Serves Generative Engine Optimization (GEO) summary for Perplexity, ChatGPT, and Claude."""
    if os.path.exists(LLMS_PATH):
        return FileResponse(LLMS_PATH, media_type="text/plain")
    return FileResponse(INDEX_PATH)


@app.get("/llms-full.txt", include_in_schema=False)
async def serve_llms_full_txt():
    """Serves full technical reference for AI context windows."""
    if os.path.exists(LLMS_FULL_PATH):
        return FileResponse(LLMS_FULL_PATH, media_type="text/plain")
    return FileResponse(INDEX_PATH)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
