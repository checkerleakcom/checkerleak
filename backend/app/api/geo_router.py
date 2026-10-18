"""
Geo Router: Endpoints for visitor geolocation detection, country catalogs, and carrier intelligence.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Request
from app.core.geo_intelligence import GeoIntelligenceService, CountryTelecomProfile

geo_router = APIRouter(prefix="/v1/geo", tags=["Geo & Telecom Intelligence"])
geo_service = GeoIntelligenceService()


@geo_router.get("/detect", response_model=CountryTelecomProfile)
def detect_visitor_location(request: Request):
    """
    Auto-detect visitor's country and local telecom carrier profile
    using Cloudflare, Reverse-Proxy headers, or Accept-Language.
    """
    headers = {k.lower(): v for k, v in request.headers.items()}
    return geo_service.detect_visitor_geo(headers)


@geo_router.get("/countries", response_model=List[Dict[str, Any]])
def list_supported_countries():
    """Retrieve catalog of primary geographic verification hubs with flags and dial codes."""
    return geo_service.get_supported_countries()


@geo_router.get("/country/{iso}", response_model=CountryTelecomProfile)
def get_country_telecom_details(iso: str):
    """Fetch telecom infrastructure, WhatsApp penetration, and top MNO carriers for an ISO code."""
    profile = geo_service.get_country_profile(iso)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Country profile not found for ISO code: '{iso}'.",
        )
    return profile
