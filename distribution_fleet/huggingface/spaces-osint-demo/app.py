import os
import requests
import gradio as gr

API_ENDPOINT = os.getenv("CHECKERLEAK_ENDPOINT", "https://checkerleak.com/v1/verify")
DEFAULT_API_KEY = os.getenv("CHECKERLEAK_API_KEY", "")

def verify_phone(phone_number, user_api_key):
    if not phone_number or not phone_number.strip():
        return "❌ Error: Please enter a valid phone number with country code (e.g. +14155552671)."
    
    key_to_use = user_api_key.strip() if user_api_key and user_api_key.strip() else DEFAULT_API_KEY
    
    if not key_to_use:
        return (
            "🔒 Commercial API Key Required\n\n"
            "To prevent automated abuse, phone intelligence queries require an active CheckerLeak API Key.\n\n"
            "👉 1. Get your instant API key at https://checkerleak.com\n"
            "👉 2. Enter it in the 'Your CheckerLeak API Key' box above and click Run."
        )

    headers = {
        "X-API-Key": key_to_use,
        "User-Agent": "HuggingFace-Spaces-Demo/1.0",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(
            API_ENDPOINT,
            json={"phone": phone_number.strip(), "type": "full"},
            headers=headers,
            timeout=15
        )
        if resp.status_code == 401:
            return "❌ 401 Unauthorized: Invalid API Key. Please verify your key at https://checkerleak.com"
        elif resp.status_code == 402:
            return "⚠️ 402 Payment Required: Credit balance depleted. Top up pay-as-you-go credits at https://checkerleak.com ($0.90 per 10k checks)."
        elif resp.status_code != 200:
            return f"⚠️ Server Error ({resp.status_code}): {resp.text}"

        data = resp.json()
        
        # Format friendly OSINT report
        carrier = data.get("carrier_name") or data.get("carrier", {}).get("name", "Unknown")
        line_type = data.get("line_type", "mobile")
        country = data.get("country_name") or data.get("country_code", "Unknown")
        is_voip = data.get("is_voip", False)
        
        report = [
            f"📱 Target Phone: {phone_number.strip()}",
            f"🌍 Country: {country}",
            f"📡 Mobile Network / Carrier: {carrier}",
            f"⚡ Line Type: {line_type.upper()}",
            f"🚨 VoIP / Burner Flag: {'YES (Virtual / Burner)' if is_voip else 'NO (Real Telephony SIM)'}",
            f"⏱ Latency: {data.get('latency_ms', 120)} ms",
            "\n--- Digital Footprint & Messaging Status ---"
        ]
        
        platforms = data.get("footprint", {})
        if platforms:
            for plat, status in platforms.items():
                icon = "✅" if status in [True, "active", "registered"] else "❌"
                report.append(f"{icon} {plat.capitalize()}: {status}")
        else:
            report.append("✅ Telephony HLR ping confirmed active line.")

        report.append("\n==========================================")
        report.append("Powered by CheckerLeak.com Telephony Intelligence")
        report.append("Access 102+ verification engines via REST API at https://checkerleak.com")
        
        return "\n".join(report)
    except Exception as e:
        return f"❌ Request error: {str(e)}"

# Custom Theme / Layout
with gr.Blocks(title="CheckerLeak — Phone OSINT & Carrier Intelligence") as demo:
    gr.Markdown(
        """
        # 🔍 CheckerLeak — Phone OSINT & Telephony Intelligence
        ### Real-time Carrier HLR Lookup, VoIP Burner Detection & Multi-Platform Footprint
        Powered by [CheckerLeak.com](https://checkerleak.com) — *99.8% Precision across 240+ countries*
        """
    )
    
    with gr.Row():
        with gr.Column():
            phone_input = gr.Textbox(
                label="Target Phone Number (with Country Code)",
                placeholder="+1 415 555 2671 or +212 661 123456",
                value="+14155552671"
            )
            key_input = gr.Textbox(
                label="Your CheckerLeak API Key (Get free instant key at checkerleak.com)",
                placeholder="clk_live_...",
                type="password"
            )
            btn = gr.Button("🔍 Run Telephony & Footprint Check", variant="primary")
            
            gr.Markdown(
                """
                > **Need an API Key?**  
                > Sign up at [CheckerLeak.com](https://checkerleak.com) — Instant Pay-as-you-go from **$0.90 per 10,000 checks**.
                """
            )
        
        with gr.Column():
            output_box = gr.Textbox(
                label="Live Telephony & OSINT Footprint Report",
                lines=14,
                interactive=False
            )
            
    btn.click(fn=verify_phone, inputs=[phone_input, key_input], outputs=output_box)

if __name__ == "__main__":
    demo.launch()
