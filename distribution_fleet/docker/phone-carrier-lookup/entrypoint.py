#!/usr/bin/env python3
import os
import sys
import json
import argparse
import requests

def main():
    parser = argparse.ArgumentParser(
        description="High-Speed Phone Carrier & HLR Lookup Microservice via CheckerLeak"
    )
    parser.add_argument("phone", help="E.164 phone number (e.g. +14155552671)")
    parser.add_argument("--key", default=os.getenv("CHECKERLEAK_API_KEY"), help="CheckerLeak API Key")
    parser.add_argument("--endpoint", default="https://checkerleak.com/v1/verify", help="API Endpoint URL")

    args = parser.parse_args()
    api_key = args.key

    if not api_key:
        print("\n[!] API Key required. Sign up at https://checkerleak.com and set CHECKERLEAK_API_KEY.\n", file=sys.stderr)
        sys.exit(1)

    try:
        resp = requests.post(
            args.endpoint,
            json={"phone": args.phone, "type": "carrier"},
            headers={"X-API-Key": api_key, "User-Agent": "Docker-PhoneCarrierLookup/1.0"},
            timeout=15
        )
        if resp.status_code == 401:
            print("[-] Error 401: Invalid API Key. Manage keys at https://checkerleak.com", file=sys.stderr)
            sys.exit(1)
        elif resp.status_code == 402:
            print("[-] Error 402: Insufficient credits. Top up at https://checkerleak.com", file=sys.stderr)
            sys.exit(1)
        
        data = resp.json()
        print(json.dumps({
            "phone": args.phone,
            "carrier": data.get("carrier", {}).get("name") or data.get("carrier_name", "Unknown"),
            "mcc": data.get("carrier", {}).get("mcc"),
            "mnc": data.get("carrier", {}).get("mnc"),
            "country": data.get("country_code"),
            "line_type": data.get("line_type", "mobile"),
            "is_ported": data.get("carrier", {}).get("ported", False)
        }, indent=2))
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
