"""
Unit and Integration tests for Batch File Upload and CSV Enrichment Export.
"""
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import AuthService

client = TestClient(app)
auth_service = AuthService()


def test_batch_file_upload_and_enrichment():
    unique_email = f"csv_batch_{uuid.uuid4().hex[:8]}@pulsecheck.com"
    user = auth_service.register(unique_email, "pass12345", "CSV Batch User")
    assert user.credits == 0
    auth_service.add_credits(user.id, 50)
    initial_credits = 50

    csv_data = "Phone,Name\n+212661234567,Alice\n+33612345678,Bob\n+14155552671,Charlie\n"
    files = {"file": ("leads.csv", csv_data.encode("utf-8"), "text/csv")}
    data = {
        "user_id": user.id,
        "default_country": "MA",
        "check_whatsapp": True,
        "check_imessage": True,
    }

    response = client.post("/v1/batch/upload-file", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["total_processed"] == 3
    assert res["credits_deducted"] == 3
    assert "csv_export_content" in res
    assert "Normalized_E164" in res["csv_export_content"]
    assert "WhatsApp_Active" in res["csv_export_content"]

    # Verify wallet credits deducted
    user_after = auth_service.get_by_id(user.id)
    assert user_after.credits == initial_credits - 3


def test_batch_file_upload_unsupported_format():
    files = {"file": ("unsupported.pdf", b"%PDF-1.4...", "application/pdf")}
    response = client.post("/v1/batch/upload-file", files=files)
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]
