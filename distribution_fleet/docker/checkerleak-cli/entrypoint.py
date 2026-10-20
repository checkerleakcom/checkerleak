#!/usr/bin/env python3
import os
import sys
import json
import argparse
import requests

def main():
    parser = argparse.ArgumentParser(
        description="CheckerLeak Official Docker CLI - All-in-One Phone Intelligence & Carrier Verification"
    )
    parser.add_argument("phone", help="Phone number with country code (e.g. +14155552671 or +212661123456)")
    parser.add_argument("--key", default=os.getenv("CHECKERLEAK_API_KEY"), help="CheckerLeak API Key (or set CHECKERLEAK_API_KEY env)")
    parser.add_argument("--type", choices=["full", "carrier", "voip", "hlr"], default="full", help="Lookup depth")
    parser.add_argument("--endpoint", default="https://checkerleak.com/v1/verify", help="API Endpoint URL")

    args = parser.parse_args()

    api_key = args.key
    if not api_key:
        print("\n=======================================================", file=sys.stderr)
        print(" [!] CHECKERLEAK API KEY REQUIRED", file=sys.stderr)
        print(" Commercial API usage requires an active CheckerLeak account.", file=sys.stderr)
        print(" 1. Sign up at https://checkerleak.com", file=sys.stderr)
        print(" 2. Generate your API key in Dashboard (instant pay-as-you-go).", file=sys.stderr)
        print(" 3. Pass via '--key YOUR_KEY' or '-e CHECKERLEAK_API_KEY=YOUR_KEY'.", file=sys.stderr)
        print("=======================================================\n", file=sys.stderr)
        sys.exit(1)

    headers = {
        "X-API-Key": api_key,
        "User-Agent": "CheckerLeak-Docker-CLI/2.0",
        "Content-Type": "application/json"
    }

    payload = {
        "phone": args.phone,
        "type": args.type
    }

    try:
        resp = requests.post(args.endpoint, json=payload, headers=headers, timeout=15)
        if resp.status_code == 401:
            print("\n[-] Error: 401 Unauthorized. Invalid or inactive CheckerLeak API Key.", file=sys.stderr)
            print("[-] Manage keys and top up credits at https://checkerleak.com/dashboard\n", file=sys.stderr)
            sys.exit(1)
        elif resp.status_code == 402:
            print("\n[-] Error: 402 Payment Required. Insufficient credit balance.", file=sys.stderr)
            print("[-] Top up credits starting at $0.90 per 10,000 checks at https://checkerleak.com\n", file=sys.stderr)
            sys.exit(1)
        
        data = resp.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[-] Network or request error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
