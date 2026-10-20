# CheckerLeak Rust Crate (`checkerleak`)

Official Rust client for **[CheckerLeak.com](https://checkerleak.com)** — High-throughput Phone Number Intelligence, Carrier HLR Lookup, and VoIP Fraud Detection.

[![Crates.io](https://img.shields.io/crates/v/checkerleak.svg)](https://crates.io/crates/checkerleak)
[![Documentation](https://docs.rs/checkerleak/badge.svg)](https://docs.rs/checkerleak)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ⚡ Quick Start

Add to your `Cargo.toml`:

```toml
[dependencies]
checkerleak = "0.1.0"
```

### Usage Example

```rust
use checkerleak::Client;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new("clk_live_your_api_key_here")?;
    
    let res = client.verify("+14155552671", Some("full"))?;
    
    println!("Phone: {}", res.phone);
    println!("Carrier: {:?}", res.carrier_name);
    println!("Is VoIP: {:?}", res.is_voip);
    println!("Country: {:?}", res.country_code);
    
    Ok(())
}
```

---

## 🔑 API Key & Pricing

API access requires an active key from **[CheckerLeak.com](https://checkerleak.com)**:
* Pay-as-you-go from **$0.90 per 10,000 checks**
* No minimum subscription or monthly commitments
* Instant Bitcoin, USDT, and Card payment methods
