"""
CheckerLeak Visitor Traffic Telemetry Router
Receives lightweight beacon hits from the frontend (fire-and-forget via sendBeacon).
Classifies traffic source: AI Search Engines, Google SEO, Dev Hubs, Direct, Social.
Stores anonymized telemetry in visitor_traffic table for admin analytics.
Zero latency impact — always returns 204 immediately.
"""
import hashlib
import os
import re
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, Response, BackgroundTasks
from pydantic import BaseModel, Field
from app.core.database import DatabaseService

telemetry_router = APIRouter(prefix="/v1/telemetry", tags=["Telemetry"])
db_service = DatabaseService()


# =====================================================================
# SOURCE CLASSIFICATION ENGINE
# =====================================================================

AI_ENGINES = {
    "chatgpt.com": "ChatGPT",
    "chat.openai.com": "ChatGPT",
    "openai.com": "ChatGPT",
    "perplexity.ai": "Perplexity",
    "gemini.google.com": "Gemini",
    "bard.google.com": "Gemini",
    "claude.ai": "Claude",
    "anthropic.com": "Claude",
    "copilot.microsoft.com": "Copilot",
    "bing.com/chat": "Copilot",
    "you.com": "You.com AI",
    "phind.com": "Phind",
    "poe.com": "Poe AI",
    "kagi.com": "Kagi AI",
}

SEARCH_ENGINES = {
    "google.com": "Google",
    "google.": "Google",
    "bing.com": "Bing",
    "yahoo.com": "Yahoo",
    "duckduckgo.com": "DuckDuckGo",
    "yandex.ru": "Yandex",
    "yandex.com": "Yandex",
    "ecosia.org": "Ecosia",
    "baidu.com": "Baidu",
    "startpage.com": "Startpage",
}

DEV_HUBS = {
    "github.com": "GitHub",
    "gist.github.com": "GitHub",
    "pypi.org": "PyPI",
    "npmjs.com": "npm",
    "rapidapi.com": "RapidAPI",
    "postman.com": "Postman",
    "dev.to": "Dev.to",
    "stackoverflow.com": "Stack Overflow",
    "hackernews": "Hacker News",
    "news.ycombinator.com": "Hacker News",
    "reddit.com/r/programming": "Reddit Dev",
    "reddit.com/r/python": "Reddit Dev",
    "reddit.com/r/webdev": "Reddit Dev",
    "medium.com": "Medium",
    "hashnode.com": "Hashnode",
}

SOCIAL_PLATFORMS = {
    "twitter.com": "Twitter/X",
    "x.com": "Twitter/X",
    "t.co": "Twitter/X",
    "linkedin.com": "LinkedIn",
    "facebook.com": "Facebook",
    "fb.com": "Facebook",
    "instagram.com": "Instagram",
    "tiktok.com": "TikTok",
    "youtube.com": "YouTube",
    "reddit.com": "Reddit",
    "telegram.org": "Telegram",
    "t.me": "Telegram",
    "discord.com": "Discord",
    "discord.gg": "Discord",
    "whatsapp.com": "WhatsApp",
}


def classify_referrer(referrer: str) -> tuple[str, str]:
    """
    Returns (source_channel, source_engine).
    Channels: AI_SEARCH | DEV_HUB | SEARCH_ENGINE | SOCIAL | CAMPAIGN | DIRECT
    """
    if not referrer or referrer.strip() == "":
        return ("DIRECT", "Direct")

    ref_lower = referrer.lower()

    # Check AI engines first (highest priority for SEO intelligence)
    for domain, engine_name in AI_ENGINES.items():
        if domain in ref_lower:
            return ("AI_SEARCH", engine_name)

    # Check dev platforms
    for domain, engine_name in DEV_HUBS.items():
        if domain in ref_lower:
            return ("DEV_HUB", engine_name)

    # Check standard search engines
    for domain, engine_name in SEARCH_ENGINES.items():
        if domain in ref_lower:
            return ("SEARCH_ENGINE", engine_name)

    # Check social platforms
    for domain, engine_name in SOCIAL_PLATFORMS.items():
        if domain in ref_lower:
            return ("SOCIAL", engine_name)

    return ("REFERRAL", "External Referral")


def extract_search_query(referrer: str, utm_term: Optional[str] = None) -> Optional[str]:
    """Extract search query from referrer URL or utm_term."""
    if utm_term:
        return utm_term[:255]

    if not referrer:
        return None

    # Extract ?q= parameter from search engines
    patterns = [r"[?&]q=([^&]+)", r"[?&]query=([^&]+)", r"[?&]search=([^&]+)", r"[?&]text=([^&]+)"]
    for pattern in patterns:
        match = re.search(pattern, referrer, re.IGNORECASE)
        if match:
            import urllib.parse
            try:
                return urllib.parse.unquote_plus(match.group(1))[:255]
            except Exception:
                return match.group(1)[:255]
    return None


def extract_product_slug(landing_path: str) -> Optional[str]:
    """Extract product slug from /products/{slug} paths."""
    match = re.match(r"^/products/([^/?#]+)", landing_path)
    if match:
        return match.group(1)[:128]
    return None


def classify_device(user_agent: str) -> str:
    """Classify device from User-Agent string."""
    if not user_agent:
        return "Unknown"
    ua_lower = user_agent.lower()
    # Detect bots first
    bot_patterns = ["bot", "crawler", "spider", "slurp", "fetch", "curl", "wget", "python", "node", "go-http", "axios", "scrapy"]
    if any(p in ua_lower for p in bot_patterns):
        return "Bot/Crawler"
    if any(p in ua_lower for p in ["mobile", "android", "iphone", "ipad", "ipod"]):
        return "Mobile"
    if "tablet" in ua_lower:
        return "Tablet"
    return "Desktop"


def anonymize_ip(ip: str) -> str:
    """SHA256 hash of IP — GDPR compliant."""
    return hashlib.sha256(ip.encode("utf-8")).hexdigest()[:32]


def _store_beacon_bg(data: dict):
    """Background task: persist beacon to visitor_traffic table."""
    try:
        with db_service.get_connection() as conn:
            cursor = db_service.get_cursor(conn)
            cursor.execute("""
                INSERT INTO visitor_traffic (
                    session_id, ip_hash, country,
                    source_channel, source_engine,
                    referrer_url, landing_path, product_slug,
                    search_query, utm_source, utm_medium, utm_campaign,
                    device_type, user_agent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("session_id"),
                data.get("ip_hash"),
                data.get("country", "XX"),
                data.get("source_channel"),
                data.get("source_engine"),
                data.get("referrer_url"),
                data.get("landing_path"),
                data.get("product_slug"),
                data.get("search_query"),
                data.get("utm_source"),
                data.get("utm_medium"),
                data.get("utm_campaign"),
                data.get("device_type"),
                data.get("user_agent"),
            ))
    except Exception as e:
        print(f"[Telemetry] Background store error: {e}")


# =====================================================================
# BEACON ENDPOINT — FIRE AND FORGET
# =====================================================================

class BeaconPayload(BaseModel):
    session_id: Optional[str] = Field(None, max_length=64)
    referrer: Optional[str] = Field("", max_length=512)
    landing_path: str = Field("/", max_length=255)
    utm_source: Optional[str] = Field(None, max_length=64)
    utm_medium: Optional[str] = Field(None, max_length=64)
    utm_campaign: Optional[str] = Field(None, max_length=64)
    utm_term: Optional[str] = Field(None, max_length=128)


@telemetry_router.post("/beacon", status_code=204, include_in_schema=False)
async def receive_beacon(
    request: Request,
    background_tasks: BackgroundTasks,
    response: Response
):
    """
    Fire-and-forget visitor telemetry endpoint.
    Accepts application/json, text/plain (navigator.sendBeacon), or raw bytes.
    Returns 204 immediately; DB write happens in background.
    """
    import json
    data_dict = {}
    try:
        raw_body = await request.body()
        if raw_body:
            data_dict = json.loads(raw_body.decode("utf-8", errors="ignore"))
    except Exception:
        data_dict = {}

    session_id = str(data_dict.get("session_id") or "")[:64]
    referrer = str(data_dict.get("referrer") or "")[:512]
    landing_path = str(data_dict.get("landing_path") or "/")[:255]
    utm_source = str(data_dict.get("utm_source") or "")[:64] or None
    utm_medium = str(data_dict.get("utm_medium") or "")[:64] or None
    utm_campaign = str(data_dict.get("utm_campaign") or "")[:64] or None
    utm_term = str(data_dict.get("utm_term") or "")[:128] or None

    # Get client IP from Cloudflare / Render proxy headers
    ip = (
        request.headers.get("CF-Connecting-IP") or
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
        getattr(request.client, "host", "0.0.0.0")
    )

    # Anonymize IP for GDPR compliance
    ip_hash = anonymize_ip(ip)

    # Country from Cloudflare header
    country = request.headers.get("CF-IPCountry", "XX")[:8]
    if not country or country == "XX":
        country = request.headers.get("X-Country", "XX")[:8]

    # User-Agent
    user_agent = request.headers.get("User-Agent", "")[:256]

    # Classify source from referrer
    source_channel, source_engine = classify_referrer(referrer)

    # Override channel if utm_source explicitly set
    if utm_source:
        utm_lower = utm_source.lower()
        matched_ai = False
        for domain, engine_name in AI_ENGINES.items():
            if domain in utm_lower:
                source_channel = "AI_SEARCH"
                source_engine = engine_name
                matched_ai = True
                break
        if not matched_ai:
            if source_channel == "DIRECT":
                source_channel = "CAMPAIGN"
            source_engine = utm_source

    # Extract search query
    search_query = extract_search_query(referrer, utm_term)

    # Extract product slug
    product_slug = extract_product_slug(landing_path)

    # Device classification
    device_type = classify_device(user_agent)

    # Don't track bots in analytics
    if device_type == "Bot/Crawler":
        response.status_code = 204
        return

    # Redact sensitive referrer data (strip query params except known safe ones)
    safe_referrer = None
    if referrer:
        try:
            from urllib.parse import urlparse
            parsed = urlparse(referrer)
            safe_referrer = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"[:255]
        except Exception:
            safe_referrer = referrer[:64]

    data = {
        "session_id": session_id,
        "ip_hash": ip_hash,
        "country": country,
        "source_channel": source_channel,
        "source_engine": source_engine,
        "referrer_url": safe_referrer,
        "landing_path": landing_path,
        "product_slug": product_slug,
        "search_query": search_query,
        "utm_source": utm_source,
        "utm_medium": utm_medium,
        "utm_campaign": utm_campaign,
        "device_type": device_type,
        "user_agent": user_agent[:256],
    }

    background_tasks.add_task(_store_beacon_bg, data)
    return Response(status_code=204)
