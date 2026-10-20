---
annotations_creators:
- machine-generated
language_creators:
- machine-generated
language:
- en
license:
- mit
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
task_categories:
- tabular-classification
- feature-extraction
task_ids: []
pretty_name: Global Mobile Carrier & Telecom Prefix Database
tags:
- telephony
- telecom
- carrier-lookup
- hlr-lookup
- osint
- phone-validator
---

# Global Mobile Carrier & Telecom Prefix Database

A reference dataset of international telephone country codes, national destination codes (NDC), mobile network codes (MNC), and primary telecom carriers across 240+ countries.

## Real-Time Live Carrier Verification
Static prefix databases cannot detect number portability (MNP) or whether a line has been ported between operators.

For **live HLR lookups** with 99.8% precision and real-time porting status, use the **[CheckerLeak.com API](https://checkerleak.com)**:
- Sub-150ms live network ping
- Real-time carrier porting detection
- WhatsApp, Telegram & Apple iMessage registration status
- Pay-as-you-go from **$0.90 per 10,000 checks**

---

## Data Schema

| Field | Type | Description |
|---|---|---|
| `country_code` | string | ISO 3166-1 alpha-2 code (e.g. "US", "MA", "FR") |
| `country_prefix` | string | E.164 country calling code (e.g. "+1", "+212") |
| `prefix` | string | National carrier prefix |
| `carrier_name` | string | Operator name (e.g. "Maroc Telecom", "Verizon Wireless") |
| `mcc` | string | Mobile Country Code |
| `mnc` | string | Mobile Network Code |
| `line_type` | string | "mobile", "landline", or "voip" |

---

## Python Integration with Live HLR API

```python
import requests

def check_carrier_live(phone_number: str, api_key: str):
    url = "https://checkerleak.com/v1/verify"
    resp = requests.post(
        url,
        json={"phone": phone_number, "type": "carrier"},
        headers={"X-API-Key": api_key}
    )
    return resp.json()

# Live example:
# res = check_carrier_live("+212661123456", "clk_live_your_key")
```

For full documentation and API keys, see **[CheckerLeak.com](https://checkerleak.com)**.
