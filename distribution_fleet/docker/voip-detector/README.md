# VoIP & Virtual Burner Fraud Detector — Docker Image

Real-time VoIP detector to protect signups, payment gateways, and OTP verification flows against burner numbers, Twilio numbers, TextNow, Google Voice, and disposable virtual lines.

Powered by **[CheckerLeak.com](https://checkerleak.com)**.

---

## ⚡ Quick Start

```bash
docker run --rm -e CHECKERLEAK_API_KEY="clk_live_your_key" \
  checkerleak/voip-detector +14155552671
```

### Sample Output

```json
{
  "phone": "+14155552671",
  "is_voip": true,
  "line_type": "voip",
  "fraud_risk": "HIGH",
  "provider": "Twilio / Bandwidth.com"
}
```

---

## 🔑 API Key & Pricing

Sign up at **[CheckerLeak.com](https://checkerleak.com)** to get your production API key:
* **$0.90 per 10,000 checks** (Under 1 cent per 100 checks)
* Sub-150ms latency
* No subscription lock-in
