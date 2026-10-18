import os
import re
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.universal_engine import UniversalCheckerEngine
from app.core.services_catalog import ServiceCategory

router = APIRouter(tags=["SEO pages"])
engine = UniversalCheckerEngine()

@router.get("/products", include_in_schema=False)
@router.get("/services", include_in_schema=False)
async def redirect_to_services():
    return RedirectResponse(url="/#servicesDirectorySection", status_code=301)

@router.get("/categories", include_in_schema=False)
async def redirect_to_categories():
    return RedirectResponse(url="/#servicesDirectorySection", status_code=301)

# Initialize Jinja2 Templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)
templates = Jinja2Templates(directory=TEMPLATES_DIR)

def slugify(text: str) -> str:
    # Basic slugification
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

ALIASES = {
    "whatsapp-checker": "whatsapp_advanced",
    "whatsapp": "whatsapp_advanced",
    "imessage-checker": "imessage_checker",
    "imessage": "imessage_checker",
    "telegram-checker": "telegram_basic",
    "telegram": "telegram_basic",
    "binance-email-checker": "binance",
    "binance-checker": "binance",
    "binance": "binance",
    "revolut-checker": "revolut",
    "revolut": "revolut",
    "carrier-detection": "carrier_detection",
    "carrier-checker": "carrier_detection",
    "carrier": "carrier_detection",
    "phone-validation": "phone_validation",
    "number-active": "number_active",
}

@router.get("/products/{service_slug}", include_in_schema=False)
async def seo_product_page(request: Request, service_slug: str):
    target_service = None
    target_id = None
    service_slug_clean = service_slug.lower().strip()
    
    # 1. Direct Alias Match
    if service_slug_clean in ALIASES and ALIASES[service_slug_clean] in engine._services_map:
        target_id = ALIASES[service_slug_clean]
        target_service = engine._services_map[target_id]

    # 2. Exact match by name_slug or id_slug or service_id
    if not target_service:
        for sid, srv in engine._services_map.items():
            name_slug = slugify(srv.name)
            id_slug = slugify(sid)
            if service_slug_clean in (name_slug, id_slug, sid):
                target_service = srv
                target_id = sid
                break

    # 3. Fuzzy partial match fallback
    if not target_service:
        clean_norm = service_slug_clean.replace("-and-", "-").replace("-", "").replace("_", "")
        for sid, srv in engine._services_map.items():
            sid_norm = sid.replace("-", "").replace("_", "")
            name_norm = slugify(srv.name).replace("-", "")
            name_norm_no_and = name_norm.replace("and", "")
            clean_norm_no_and = clean_norm.replace("and", "")
            if (clean_norm in sid_norm or sid_norm in clean_norm or 
                clean_norm in name_norm or name_norm in clean_norm or
                clean_norm_no_and == name_norm_no_and):
                target_service = srv
                target_id = sid
                break
            
    if not target_service:
        # Default to first service or 404
        raise HTTPException(status_code=404, detail="Product not found")
        
    product_slug = slugify(target_service.name)
    canonical_url = f"https://checkerleak.com/products/{product_slug}"

    return templates.TemplateResponse(
        request,
        "product_page.html",
        {
            "service": target_service,
            "service_id": target_id,
            "category_name": target_service.category.name.replace("_", " ").title(),
            "category_slug": slugify(target_service.category.name),
            "product_slug": product_slug,
            "canonical_url": canonical_url
        }
    )

@router.get("/categories/{category_slug}", include_in_schema=False)
async def seo_category_page(request: Request, category_slug: str):
    category_enum = None
    for cat in ServiceCategory:
        if slugify(cat.name) == category_slug:
            category_enum = cat
            break
            
    if not category_enum:
        raise HTTPException(status_code=404, detail="Category not found")
        
    services_in_cat = [
        {"id": sid, "service": srv, "slug": slugify(srv.name)} 
        for sid, srv in engine._services_map.items() 
        if srv.category == category_enum
    ]
    
    canonical_url = f"https://checkerleak.com/categories/{category_slug}"

    return templates.TemplateResponse(
        request,
        "category_page.html",
        {
            "category_name": category_enum.name.replace("_", " ").title(),
            "category_slug": category_slug,
            "canonical_url": canonical_url,
            "services": services_in_cat
        }
    )
