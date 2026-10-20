# Phone Carrier Lookup & HLR Microservice — Docker Image

Lightweight Docker microservice to identify real-time mobile carriers, MCC/MNC codes, original vs ported operators, and line types without sending SMS verification.

Powered by **[CheckerLeak.com](https://checkerleak.com)** telephony intelligence.

---

## ⚡ Quick Start

```bash
docker run --rm -e CHECKERLEAK_API_KEY="clk_live_your_key" \
  checkerleak/phone-carrier-lookup +14155552671
```

### Sample Output

```json
{
  "phone": "+14155552671",
  "carrier": "Verizon Wireless",
  "mcc": "311",
  "mnc": "480",
  "country": "US",
  "line_type": "mobile",
  "is_ported": false
}
```

---

## 🔑 API Key & Pricing

Get your API key at **[CheckerLeak.com](https://checkerleak.com)**:
* Pay-as-you-go from **$0.90 per 10,000 checks**
* Zero KYC, Bitcoin / USDT and Card payments supported
* Credits never expire
