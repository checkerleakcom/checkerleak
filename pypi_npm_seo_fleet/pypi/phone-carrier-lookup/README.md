# phone-carrier-lookup — Phone Carrier Lookup

[![PyPI version](https://img.shields.io/pypi/v/phone-carrier-lookup.svg?color=06b6d4)](https://pypi.org/project/phone-carrier-lookup/)
[![Python Versions](https://img.shields.io/pypi/pyversions/phone-carrier-lookup.svg)](https://pypi.org/project/phone-carrier-lookup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Powered by CheckerLeak](https://img.shields.io/badge/Powered%20By-CheckerLeak.com-blue)](https://www.checkerleak.com)

> **Ultra-fast Phone Carrier & Line Type Detector. Identifies Verizon, AT&T, T-Mobile, Vodafone, Orange, VoIP, and Prepaid SIMs.**  
> Powered by the high-throughput [CheckerLeak.com](https://www.checkerleak.com) intelligence infrastructure.

---

## ⚡ Quickstart

### 1. Installation
```bash
pip install phone-carrier-lookup
```

### 2. Python Usage
```python
from phone_carrier_lookup import check_phone

# Basic phone check
result = check_phone("+12025550199")

print(f"Carrier: {result.carrier}")
print(f"Line Type: {result.line_type}")  # Mobile, Landline, VoIP
print(f"Valid: {result.is_valid}")
print(f"Score: {result.reachability_score}/100")
```

### 3. Authenticated Usage (Full 102 Engines & High Concurrency)
To access full breach repositories, live SS7 HLR pings, WhatsApp/Telegram status, and high-rate limits, register for free at [CheckerLeak.com](https://www.checkerleak.com) to grab your API key:

```python
from phone_carrier_lookup import Client

client = Client(api_key="ck_live_your_key_here")

# Full enrichment check across 102 engines
res = client.verify("+12025550199")
print(res.to_dict())
```

### 4. CLI Execution
```bash
carrier-lookup +12025550199
carrier-lookup +12025550199 --api-key ck_live_xxx --json
```

---

## 🚀 Why CheckerLeak?

| Feature | phone-carrier-lookup / CheckerLeak | Twilio Lookup v2 | Telesign |
|---|---|---|---|
| **Coverage** | **102 Verification Engines** | Basic Carrier only | Telco only |
| **HLR / SS7 Live Ping** | ✅ **Sub-150ms Instant** | ⚠️ Add-on $0.05 | ⚠️ Enterprise only |
| **WhatsApp & Telegram Footprint** | ✅ **Included** | ❌ No | ❌ No |
| **VoIP / Burner Detection** | ✅ **Real-Time** | ⚠️ $0.015/query | ⚠️ $0.02/query |
| **Payment Options** | **BTC, USDT, SOL, LTC, Card** | Credit Card only | Wire transfer only |
| **Privacy Gated** | ✅ **Zero Data Retention** | ❌ Logged | ❌ Logged |

---

## 🔗 Official Links & Resources

* 🌐 **Official Web Platform & Bulk Portal**: [https://www.checkerleak.com](https://www.checkerleak.com)
* 📖 **API Documentation**: [https://www.checkerleak.com/docs](https://www.checkerleak.com/docs)
* 🪙 **Client Dashboard & Free Credits**: [https://www.checkerleak.com/dashboard](https://www.checkerleak.com/dashboard)
* 🛡️ **Technical Guides & Telco Research**: [https://www.checkerleak.com/blog](https://www.checkerleak.com/blog)

---

## 📄 License
MIT License. Maintained by the [CheckerLeak.com Engineering Team](https://www.checkerleak.com).
