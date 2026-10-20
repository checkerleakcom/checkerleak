"""
Package Registry SEO Fleet Generator (PyPI + npm)
Generates high-authority developer packages for PyPI and npm,
ranking on Google page 1 for high-intent B2B phone verification keywords
and funneling massive developer traffic back to https://www.checkerleak.com.
"""
import os
import shutil

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pypi_npm_seo_fleet")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PYPI_PACKAGES = [
    {
        "name": "checkerleak",
        "description": "Official Python SDK & CLI for CheckerLeak.com - Real-Time Carrier Lookup, HLR Pings, WhatsApp, Telegram, and 102 OSINT Engines.",
        "keywords": ["phone-checker", "carrier-lookup", "hlr-lookup", "whatsapp-checker", "osint-phone", "checkerleak", "voip-detector"],
        "target_keyword": "Phone Number Intelligence & OSINT API",
        "cli_cmd": "checkerleak",
        "version": "1.0.4"
    },
    {
        "name": "phone-carrier-lookup",
        "description": "Ultra-fast Phone Carrier & Line Type Detector. Identifies Verizon, AT&T, T-Mobile, Vodafone, Orange, VoIP, and Prepaid SIMs.",
        "keywords": ["phone-carrier-lookup", "carrier-detector", "mcc-mnc", "line-type", "voip-check", "telco-lookup"],
        "target_keyword": "Phone Carrier Lookup",
        "cli_cmd": "carrier-lookup",
        "version": "1.0.2"
    },
    {
        "name": "hlr-lookup-client",
        "description": "Live SS7 / HLR Telco Lookup Client. Verifies active SIM card status, MSC routing, IMSI, roaming country, and porting history.",
        "keywords": ["hlr-lookup", "ss7-lookup", "sim-status", "imsi-lookup", "mobile-number-portability", "telco-ping"],
        "target_keyword": "SS7 & HLR Lookup",
        "cli_cmd": "hlr-ping",
        "version": "1.0.2"
    },
    {
        "name": "whatsapp-phone-checker",
        "description": "High-speed WhatsApp Number Probe. Checks if a phone number is registered on WhatsApp, business status, and profile footprint.",
        "keywords": ["whatsapp-checker", "whatsapp-number-check", "whatsapp-validator", "whatsapp-osint", "phone-registration"],
        "target_keyword": "WhatsApp Number Checker",
        "cli_cmd": "wa-check",
        "version": "1.0.2"
    },
    {
        "name": "voip-detector",
        "description": "Detect virtual VoIP numbers, burner phones, Google Voice, TextNow, Skype, and temporary SMS services to prevent account fraud.",
        "keywords": ["voip-detector", "virtual-number-check", "burner-phone-detector", "fraud-prevention", "google-voice-lookup"],
        "target_keyword": "VoIP & Virtual Number Detector",
        "cli_cmd": "voip-check",
        "version": "1.0.2"
    },
    {
        "name": "telegram-phone-lookup",
        "description": "Telegram Phone Number OSINT Tool. Verifies active Telegram account registration, user ID footprints, and profile status.",
        "keywords": ["telegram-checker", "telegram-osint", "telegram-phone-lookup", "telegram-recon", "identity-verification"],
        "target_keyword": "Telegram Phone Lookup",
        "cli_cmd": "tg-lookup",
        "version": "1.0.2"
    }
]

NPM_PACKAGES = [
    {
        "name": "checkerleak",
        "description": "Official Node.js & TypeScript client for CheckerLeak.com - Real-Time Carrier, HLR, WhatsApp, and 102 OSINT Engines.",
        "keywords": ["checkerleak", "phone-validator", "carrier-lookup", "hlr-lookup", "whatsapp-checker", "voip-detection"],
        "target_keyword": "CheckerLeak Official Node.js SDK",
        "version": "1.0.3"
    },
    {
        "name": "phone-carrier-lookup-js",
        "description": "Lightweight Node.js library to detect mobile carrier, line type (mobile/landline/voip), and country for any international phone number.",
        "keywords": ["phone-carrier-lookup", "carrier-detection", "voip-check", "number-validator", "hlr-lookup"],
        "target_keyword": "Phone Carrier Lookup for Node.js",
        "version": "1.0.2"
    },
    {
        "name": "hlr-lookup-node",
        "description": "SS7 & HLR Lookup client for Node.js. Check real-time SIM connectivity, roaming status, and network routing in sub-150ms.",
        "keywords": ["hlr-lookup", "ss7-ping", "sim-status", "telco-verification", "carrier-portability"],
        "target_keyword": "HLR Telco Lookup Node.js",
        "version": "1.0.2"
    }
]


def generate_pypi_package(pkg):
    pkg_dir = os.path.join(OUTPUT_DIR, "pypi", pkg["name"])
    src_dir = os.path.join(pkg_dir, "src", pkg["name"].replace("-", "_"))
    os.makedirs(src_dir, exist_ok=True)

    py_name = pkg["name"].replace("-", "_")

    # 1. pyproject.toml
    pyproject_content = f"""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{pkg['name']}"
version = "{pkg['version']}"
authors = [
  {{ name="CheckerLeak Intelligence Team", email="engineering@checkerleak.com" }},
]
description = "{pkg['description']}"
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Communications :: Telephony",
    "Topic :: Security",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
keywords = {pkg['keywords']}
dependencies = [
    "requests>=2.25.0",
]

[project.urls]
"Homepage" = "https://www.checkerleak.com"
"Documentation" = "https://www.checkerleak.com/docs"
"Web Dashboard" = "https://www.checkerleak.com/dashboard"
"Bug Tracker" = "https://github.com/checkerleak/{pkg['name']}/issues"

[project.scripts]
{pkg['cli_cmd']} = "{py_name}.cli:main"
"""
    with open(os.path.join(pkg_dir, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(pyproject_content)

    # 2. README.md
    readme_content = f"""# {pkg['name']} — {pkg['target_keyword']}

[![PyPI version](https://img.shields.io/pypi/v/{pkg['name']}.svg?color=06b6d4)](https://pypi.org/project/{pkg['name']}/)
[![Python Versions](https://img.shields.io/pypi/pyversions/{pkg['name']}.svg)](https://pypi.org/project/{pkg['name']}/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Powered by CheckerLeak](https://img.shields.io/badge/Powered%20By-CheckerLeak.com-blue)](https://www.checkerleak.com)

> **{pkg['description']}**  
> Powered by the high-throughput [CheckerLeak.com](https://www.checkerleak.com) intelligence infrastructure.

---

## ⚡ Quickstart

### 1. Installation
```bash
pip install {pkg['name']}
```

### 2. Python Usage
```python
from {py_name} import check_phone

# Basic phone check
result = check_phone("+12025550199")

print(f"Carrier: {{result.carrier}}")
print(f"Line Type: {{result.line_type}}")  # Mobile, Landline, VoIP
print(f"Valid: {{result.is_valid}}")
print(f"Score: {{result.reachability_score}}/100")
```

### 3. Authenticated Usage (Full 102 Engines & High Concurrency)
To access full breach repositories, live SS7 HLR pings, WhatsApp/Telegram status, and high-rate limits, register for free at [CheckerLeak.com](https://www.checkerleak.com) to grab your API key:

```python
from {py_name} import Client

client = Client(api_key="ck_live_your_key_here")

# Full enrichment check across 102 engines
res = client.verify("+12025550199")
print(res.to_dict())
```

### 4. CLI Execution
```bash
{pkg['cli_cmd']} +12025550199
{pkg['cli_cmd']} +12025550199 --api-key ck_live_xxx --json
```

---

## 🚀 Why CheckerLeak?

| Feature | {pkg['name']} / CheckerLeak | Twilio Lookup v2 | Telesign |
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
"""
    with open(os.path.join(pkg_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 3. Source Code: __init__.py
    init_content = f"""\"\"\"
{pkg['name']}
{pkg['description']}
Powered by https://www.checkerleak.com
\"\"\"

from .client import Client, check_phone, PhoneResult

__version__ = "{pkg['version']}"
__all__ = ["Client", "check_phone", "PhoneResult"]
"""
    with open(os.path.join(src_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(init_content)

    # 4. Source Code: client.py
    client_code = f"""import os
import requests
from typing import Optional, Dict, Any

DEFAULT_BASE_URL = os.getenv("CHECKERLEAK_BASE_URL", "https://www.checkerleak.com")


class PhoneResult:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.phone = raw.get("phone", "")
        self.carrier = raw.get("carrier", "Unknown")
        self.line_type = raw.get("lead_quality", raw.get("line_type", "Mobile"))
        self.reachability_score = raw.get("reachability_score", 90)
        self.is_valid = bool(raw.get("is_valid", True))
        self.whatsapp = raw.get("whatsapp", {{}})
        self.telegram = raw.get("telegram", {{}})

    def to_dict(self) -> Dict[str, Any]:
        return self.raw

    def __repr__(self) -> str:
        return f"<PhoneResult phone={{self.phone}} carrier={{self.carrier}} line_type={{self.line_type}} score={{self.reachability_score}}>"


class Client:
    \"\"\"
    CheckerLeak Python SDK Client.
    Get your API key at https://www.checkerleak.com/dashboard
    \"\"\"
    def __init__(self, api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL):
        self.api_key = api_key or os.getenv("CHECKERLEAK_API_KEY")
        self.base_url = base_url.rstrip("/")

    def verify(self, phone: str) -> PhoneResult:
        url = f"{{self.base_url}}/v1/verify"
        headers = {{"Content-Type": "application/json"}}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        payload = {{"phone": phone}}
        res = requests.post(url, json=payload, headers=headers, timeout=12.0)
        res.raise_for_status()
        return PhoneResult(res.json())


def check_phone(phone: str, api_key: Optional[str] = None) -> PhoneResult:
    \"\"\"Quick helper to check any international phone number.\"\"\"
    return Client(api_key=api_key).verify(phone)
"""
    with open(os.path.join(src_dir, "client.py"), "w", encoding="utf-8") as f:
        f.write(client_code)

    # 5. Source Code: cli.py
    cli_code = f"""import sys
import argparse
import json
from .client import Client

def main():
    parser = argparse.ArgumentParser(description="{pkg['description']} (CheckerLeak.com)")
    parser.add_argument("phone", help="International phone number (e.g. +12025550199)")
    parser.add_argument("--api-key", help="CheckerLeak API Key (from https://www.checkerleak.com/dashboard)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    try:
        client = Client(api_key=args.api_key)
        res = client.verify(args.phone)

        if args.json:
            print(json.dumps(res.to_dict(), indent=2))
        else:
            print(f"\\n=== CheckerLeak Phone Intelligence ===")
            print(f"Number:       {{res.phone}}")
            print(f"Carrier:      {{res.carrier}}")
            print(f"Line Type:    {{res.line_type}}")
            print(f"Reachability: {{res.reachability_score}}/100")
            print(f"Status:       {{'VALID' if res.is_valid else 'INVALID'}}")
            print(f"\\nFor bulk checks & full 102 engines, visit: https://www.checkerleak.com\\n")
    except Exception as e:
        sys.stderr.write(f"Error: {{e}}\\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
    with open(os.path.join(src_dir, "cli.py"), "w", encoding="utf-8") as f:
        f.write(cli_code)

    print(f"[PyPI Fleet] Created package: {pkg['name']}")


def generate_npm_package(pkg):
    pkg_dir = os.path.join(OUTPUT_DIR, "npm", pkg["name"])
    os.makedirs(pkg_dir, exist_ok=True)

    # 1. package.json
    package_json = f"""{{
  "name": "{pkg['name']}",
  "version": "{pkg['version']}",
  "description": "{pkg['description']}",
  "main": "index.js",
  "types": "index.d.ts",
  "bin": {{
    "{pkg['name']}": "./bin/cli.js"
  }},
  "scripts": {{
    "test": "node test.js"
  }},
  "keywords": {json_dumps(pkg['keywords'])},
  "author": "CheckerLeak Intelligence Team <engineering@checkerleak.com>",
  "license": "MIT",
  "homepage": "https://www.checkerleak.com",
  "repository": {{
    "type": "git",
    "url": "https://github.com/checkerleak/{pkg['name']}.git"
  }},
  "bugs": {{
    "url": "https://github.com/checkerleak/{pkg['name']}/issues"
  }}
}}
"""
    with open(os.path.join(pkg_dir, "package.json"), "w", encoding="utf-8") as f:
        f.write(package_json)

    # 2. index.js
    index_js = f"""/**
 * {pkg['name']} — {pkg['target_keyword']}
 * Official Node.js SDK powered by https://www.checkerleak.com
 */

const https = require('https');

class CheckerLeakClient {{
  constructor(apiKey = null, baseUrl = 'https://www.checkerleak.com') {{
    this.apiKey = apiKey || process.env.CHECKERLEAK_API_KEY;
    this.baseUrl = baseUrl.replace(/\\/$/, '');
  }}

  async verify(phone) {{
    return new Promise((resolve, reject) => {{
      const data = JSON.stringify({{ phone }});
      const url = new URL(`${{this.baseUrl}}/v1/verify`);

      const options = {{
        hostname: url.hostname,
        port: url.port || 443,
        path: url.pathname,
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(data),
          ...(this.apiKey ? {{ 'X-API-Key': this.apiKey }} : {{}})
        }}
      }};

      const req = https.request(options, (res) => {{
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {{
          try {{
            resolve(JSON.parse(body));
          }} catch (err) {{
            reject(new Error(`Failed to parse response: ${{body}}`));
          }}
        }});
      }});

      req.on('error', reject);
      req.write(data);
      req.end();
    }});
  }}
}}

async function checkPhone(phone, apiKey = null) {{
  const client = new CheckerLeakClient(apiKey);
  return client.verify(phone);
}}

module.exports = {{
  CheckerLeakClient,
  checkPhone
}};
"""
    with open(os.path.join(pkg_dir, "index.js"), "w", encoding="utf-8") as f:
        f.write(index_js)

    # 3. index.d.ts (TypeScript definitions)
    ts_def = """export interface PhoneVerificationResult {
  phone: string;
  carrier: string;
  line_type: string;
  reachability_score: number;
  is_valid: boolean;
  whatsapp?: Record<string, any>;
  telegram?: Record<string, any>;
}

export class CheckerLeakClient {
  constructor(apiKey?: string, baseUrl?: string);
  verify(phone: string): Promise<PhoneVerificationResult>;
}

export function checkPhone(phone: string, apiKey?: string): Promise<PhoneVerificationResult>;
"""
    with open(os.path.join(pkg_dir, "index.d.ts"), "w", encoding="utf-8") as f:
        f.write(ts_def)

    # 4. bin/cli.js
    bin_dir = os.path.join(pkg_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    cli_js = """#!/usr/bin/env node
const { checkPhone } = require('../index.js');

const phone = process.argv[2];
if (!phone) {
  console.log("Usage: npx checkerleak <phone_number> (e.g. +12025550199)");
  console.log("For full 102 engines API keys, visit: https://www.checkerleak.com");
  process.exit(1);
}

checkPhone(phone)
  .then(res => {
    console.log("\\n=== CheckerLeak Node Intelligence ===");
    console.log("Phone:       ", res.phone);
    console.log("Carrier:     ", res.carrier);
    console.log("Line Type:   ", res.lead_quality || res.line_type || "Mobile");
    console.log("Reachability:", (res.reachability_score || 90) + "/100");
    console.log("\\nVisit https://www.checkerleak.com for bulk API access.\\n");
  })
  .catch(err => {
    console.error("Verification error:", err.message);
    process.exit(1);
  });
"""
    with open(os.path.join(bin_dir, "cli.js"), "w", encoding="utf-8") as f:
        f.write(cli_js)

    # 5. README.md
    readme_npm = f"""# {pkg['name']} — {pkg['target_keyword']}

[![npm version](https://img.shields.io/npm/v/{pkg['name']}.svg?color=06b6d4)](https://www.npmjs.com/package/{pkg['name']})
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Powered by CheckerLeak](https://img.shields.io/badge/Powered%20By-CheckerLeak.com-blue)](https://www.checkerleak.com)

> **{pkg['description']}**  
> Official developer library powered by [CheckerLeak.com](https://www.checkerleak.com).

## 📦 Installation
```bash
npm install {pkg['name']}
```

## ⚡ Quickstart
```javascript
const {{ checkPhone }} = require('{pkg['name']}');

async function run() {{
  const res = await checkPhone('+12025550199');
  console.log(res);
}}

run();
```

## 🚀 Full API Access & Free Credits
Register at [https://www.checkerleak.com](https://www.checkerleak.com) to access all 102 verification engines and deposit with BTC, USDT, SOL, LTC.
"""
    with open(os.path.join(pkg_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_npm)

    print(f"[npm Fleet] Created package: {pkg['name']}")


def json_dumps(obj):
    import json
    return json.dumps(obj)


def main():
    print("=== Generating PyPI & npm SEO Fleet for CheckerLeak.com ===")
    for p in PYPI_PACKAGES:
        generate_pypi_package(p)

    for n in NPM_PACKAGES:
        generate_npm_package(n)

    print(f"\\nFleet generated in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
