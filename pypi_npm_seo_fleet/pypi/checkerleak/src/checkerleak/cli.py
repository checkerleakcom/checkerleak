import sys
import argparse
import json
from .client import Client

def main():
    parser = argparse.ArgumentParser(description="Official Python SDK & CLI for CheckerLeak.com - Real-Time Carrier Lookup, HLR Pings, WhatsApp, Telegram, and 102 OSINT Engines. (CheckerLeak.com)")
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
            print(f"\n=== CheckerLeak Phone Intelligence ===")
            print(f"Number:       {res.phone}")
            print(f"Carrier:      {res.carrier}")
            print(f"Line Type:    {res.line_type}")
            print(f"Reachability: {res.reachability_score}/100")
            print(f"Status:       {'VALID' if res.is_valid else 'INVALID'}")
            print(f"\nFor bulk checks & full 102 engines, visit: https://www.checkerleak.com\n")
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
