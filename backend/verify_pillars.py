import urllib.request
import json

def run_tests():
    # 1. Homepage HTML
    res = urllib.request.urlopen("http://127.0.0.1:8000/")
    html = res.read().decode("utf-8")
    assert "topUpModal" in html, "topUpModal missing"
    assert "developerModal" in html, "developerModal missing"
    assert "csvDropZone" in html, "csvDropZone missing"
    print("1. Homepage HTML verified with all 3 pillars: OK")

    # 2. Billing plans
    res = urllib.request.urlopen("http://127.0.0.1:8000/v1/billing/plans")
    plans = json.loads(res.read().decode("utf-8"))
    assert len(plans) == 3, f"Expected 3 plans, got {len(plans)}"
    plan_names = [p["name"] for p in plans]
    print(f"2. Billing plans: {plan_names}: OK")

    # 3. User Register or Login
    import uuid
    random_email = f"client_{uuid.uuid4().hex[:6]}@company.com"
    req = urllib.request.Request(
        "http://127.0.0.1:8000/v1/auth/register",
        data=json.dumps({"email": random_email, "password": "password123", "full_name": "Hamza Lead"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    u = json.loads(res.read().decode("utf-8"))["user"]
    user_id = u["id"]
    print(f"3. Authenticated client {random_email} with ID {user_id}, initial credits: {u['credits']}: OK")

    # 4. Pillar 1: Confirm Top-Up (Pro Plan - $49)
    topup_payload = json.dumps({"user_id": user_id, "plan_id": "pro", "payment_method": "STRIPE_CARD"}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/v1/billing/confirm-topup",
        data=topup_payload,
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    topup_data = json.loads(res.read().decode("utf-8"))
    assert topup_data["success"] is True
    print(f"4. Pillar 1 (Top-Up): Added {topup_data['credits_added']} credits, new balance: {topup_data['new_wallet_balance']}: OK")

    # 5. Pillar 2: Developer Key Rotation & Snippets
    req = urllib.request.Request(
        "http://127.0.0.1:8000/v1/developer/regenerate-key",
        data=json.dumps({"user_id": user_id}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    regen_data = json.loads(res.read().decode("utf-8"))
    assert regen_data["success"] is True
    new_api_key = regen_data["new_api_key"]
    print(f"5a. Pillar 2 (API Rotation): New key {new_api_key[:16]}...: OK")

    res = urllib.request.urlopen(f"http://127.0.0.1:8000/v1/developer/snippets?user_id={user_id}")
    snip_data = json.loads(res.read().decode("utf-8"))
    assert new_api_key in snip_data["snippets"]["curl"]
    assert new_api_key in snip_data["snippets"]["python"]
    assert new_api_key in snip_data["snippets"]["javascript"]
    print("5b. Pillar 2 (Live Snippets): All 3 language snippets populated with real key: OK")

    # 6. Pillar 3: Batch Multipart File Upload
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    csv_content = "Phone,Name\n+212661123456,Yassine\n+33612345678,Marc\n+14155552671,Sarah\n"
    
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="leads.csv"\r\n'
        f"Content-Type: text/csv\r\n\r\n"
        f"{csv_content}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="user_id"\r\n\r\n'
        f"{user_id}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="default_country"\r\n\r\n'
        f"MA\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="check_whatsapp"\r\n\r\n'
        f"true\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="check_imessage"\r\n\r\n'
        f"true\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:8000/v1/batch/upload-file",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    res = urllib.request.urlopen(req)
    batch_data = json.loads(res.read().decode("utf-8"))
    assert batch_data["success"] is True
    assert batch_data["total_processed"] == 3
    assert "csv_export_content" in batch_data
    assert "Normalized_E164" in batch_data["csv_export_content"]
    print(f"6. Pillar 3 (Batch Upload): Processed {batch_data['total_processed']} rows, deducted {batch_data['credits_deducted']} credits, CSV exported: OK")

    print("\nSUCCESS: ALL 3 PILLARS FULLY VALIDATED AND PASSING!")

if __name__ == "__main__":
    run_tests()
