# CheckerLeak CLI — Official Docker Image

The official Docker image for **[CheckerLeak.com](https://checkerleak.com)** — the enterprise all-in-one phone number intelligence, carrier HLR lookup, VoIP fraud detection, and 102+ platform footprint verification engine.

[![Docker Pulls](https://img.shields.io/docker/pulls/checkerleak/cli.svg)](https://hub.docker.com/r/checkerleak/cli)
[![Docker Image Size](https://img.shields.io/docker/image-size/checkerleak/cli/latest.svg)](https://hub.docker.com/r/checkerleak/cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://checkerleak.com)

---

## ⚡ Quick Start

Verify any international phone number directly from your terminal:

```bash
docker run --rm -e CHECKERLEAK_API_KEY="clk_live_your_api_key_here" \
  checkerleak/cli +14155552671
```

Or pass the key via CLI flag:

```bash
docker run --rm checkerleak/cli +212661123456 --key "clk_live_your_api_key_here"
```

---

## 🚀 Key Features

* **Real-time HLR Carrier Lookup**: Identify active mobile networks, MCC, MNC, and original vs ported carrier without sending SMS.
* **VoIP & Burner Fraud Detection**: Instant detection of Google Voice, TextNow, Twilio, Skype, and temporary burner numbers.
* **102+ Platform Footprint Probes**: Check registration across WhatsApp, Telegram, Apple iMessage, Viber, Binance, PayPal, and more.
* **Sub-150ms Response Time**: High-throughput distributed carrier connectivity across 240+ countries.
* **Zero-Log Privacy Architecture**: No query data or verified numbers are ever logged or retained.

---

## 🔑 Obtaining an API Key

Commercial usage requires an active CheckerLeak account:

1. Create a free account at **[CheckerLeak.com](https://checkerleak.com)**.
2. Generate your production API key in the Dashboard.
3. Top up pay-as-you-go credits starting at **$0.90 per 10,000 checks** (Instant Bitcoin, USDT, or Card invoicing).

---

## 📋 Lookup Types

```bash
# Full phone intelligence & footprint (Default)
docker run --rm -e CHECKERLEAK_API_KEY=$KEY checkerleak/cli +14155552671 --type full

# Fast carrier & HLR lookup only
docker run --rm -e CHECKERLEAK_API_KEY=$KEY checkerleak/cli +14155552671 --type carrier

# VoIP & virtual fraud score only
docker run --rm -e CHECKERLEAK_API_KEY=$KEY checkerleak/cli +14155552671 --type voip
```

---

## 🌐 Official Resources

* **Web Console & API Keys**: [https://checkerleak.com](https://checkerleak.com)
* **REST API Documentation**: [https://checkerleak.com/docs](https://checkerleak.com/docs)
* **Python SDK (PyPI)**: [pypi.org/project/checkerleak](https://pypi.org/project/checkerleak/)
* **Node.js SDK (npm)**: [npmjs.com/package/checkerleak](https://www.npmjs.com/package/checkerleak)
* **Support**: support@checkerleak.com
