"""
Developer Router: API Key rotation, usage statistics, and integration code snippets (cURL, Python, Node.js).
"""
import uuid
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from app.core.database import DatabaseService

router = APIRouter(prefix="/v1/developer", tags=["Developer API"])
db = DatabaseService()


class RegenerateKeyRequest(BaseModel):
    user_id: int = Field(..., description="ID of client requesting key rotation")


@router.post("/regenerate-key")
def regenerate_api_key(request: RegenerateKeyRequest):
    """Securely rotate client API key and invalidate previous token."""
    new_key = f"pulse_live_{uuid.uuid4().hex[:24]}"
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (request.user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

        cursor.execute("UPDATE users SET api_key = ? WHERE id = ?", (new_key, request.user_id))
        conn.commit()

    return {
        "success": True,
        "new_api_key": new_key,
        "notice": "Previous API key invalidated. Please update your environment variables.",
    }


@router.get("/snippets")
def get_code_snippets(
    user_id: Optional[int] = Query(None),
    target_sample: str = Query("+212661234567"),
    service_sample: str = Query("whatsapp_advanced"),
) -> Dict[str, Any]:
    """Retrieve personalized, copy-paste code snippets for cURL, Python, and JavaScript/Node.js."""
    api_key = "pulse_live_demo_guest_key_77a9"
    credits = 1000
    effective_user_id = 1

    if user_id is not None:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, api_key, credits FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                api_key = row["api_key"]
                credits = row["credits"]
                effective_user_id = row["id"]

    curl_code = f"""# Verify single contact via cURL
curl -X POST "http://127.0.0.1:8000/v1/verify/service" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: {api_key}" \\
  -d '{{
    "service_id": "{service_sample}",
    "target": "{target_sample}",
    "user_id": {effective_user_id}
  }}'"""

    python_code = f"""import requests

API_URL = "http://127.0.0.1:8000/v1/verify/service"
HEADERS = {{
    "Content-Type": "application/json",
    "X-API-Key": "{api_key}"
}}

payload = {{
    "service_id": "{service_sample}",
    "target": "{target_sample}",
    "user_id": {user_id}
}}

response = requests.post(API_URL, json=payload, headers=HEADERS)
data = response.json()

print(f"Registered: {{data['is_registered']}} | Confidence: {{data['confidence_score']}}%")
print(f"Risk Level: {{data['risk_level']}} | Summary: {{data['status_summary']}}")
"""

    node_code = f"""// Node.js (v18+ with native fetch)
const response = await fetch("http://127.0.0.1:8000/v1/verify/service", {{
  method: "POST",
  headers: {{
    "Content-Type": "application/json",
    "X-API-Key": "{api_key}"
  }},
  body: JSON.stringify({{
    service_id: "{service_sample}",
    target: "{target_sample}",
    user_id: {user_id}
  }})
}});

const result = await response.json();
console.log(`Registered: ${{result.is_registered}} (Confidence: ${{result.confidence_score}}%)`);
"""

    return {
        "api_key": api_key,
        "wallet_credits": credits,
        "base_url": "http://127.0.0.1:8000/v1",
        "docs_url": "http://127.0.0.1:8000/docs",
        "snippets": {
            "curl": curl_code,
            "python": python_code,
            "javascript": node_code,
        },
    }
