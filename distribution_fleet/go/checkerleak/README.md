# CheckerLeak Go SDK (`checkerleak-go`)

Official Go client library for **[CheckerLeak.com](https://checkerleak.com)** — High-performance Phone Number Intelligence, Carrier HLR Lookup, and VoIP Fraud Detection.

[![Go Reference](https://pkg.go.dev/badge/github.com/checkerleak/checkerleak-go.svg)](https://pkg.go.dev/github.com/checkerleak/checkerleak-go)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Installation

```bash
go get github.com/checkerleak/checkerleak-go
```

---

## Quick Example

```go
package main

import (
	"fmt"
	"log"

	"github.com/checkerleak/checkerleak-go"
)

func main() {
	client, err := checkerleak.NewClient("clk_live_your_api_key_here")
	if err != nil {
		log.Fatal(err)
	}

	res, err := client.Verify("+14155552671", "full")
	if err != nil {
		log.Fatalf("Verification failed: %v", err)
	}

	fmt.Printf("Phone: %s\n", res.Phone)
	fmt.Printf("Carrier: %s (MCC: %s, MNC: %s)\n", res.CarrierName, res.Carrier.MCC, res.Carrier.MNC)
	fmt.Printf("Is VoIP Burner: %t\n", res.IsVoIP)
	fmt.Printf("Line Type: %s\n", res.LineType)
}
```

---

## Obtaining an API Key

An active CheckerLeak account is required for API access:
1. Create an account at **[CheckerLeak.com](https://checkerleak.com)**.
2. Generate your production API key in the Dashboard.
3. Pay-as-you-go credits start at **$0.90 per 10,000 checks** (Under $0.0001 per check).
