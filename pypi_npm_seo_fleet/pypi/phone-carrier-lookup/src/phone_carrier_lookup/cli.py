import sys
import os
import argparse
import json
from .client import Client

def main():
    parser = argparse.ArgumentParser(description="Ultra-fast Phone Carrier & Line Type Detector. Identifies Verizon, AT&T, T-Mobile, Vodafone, Orange, VoIP, and Prepaid SIMs. (CheckerLeak.com)")
    parser.add_argument("phone", help="International phone number (e.g. +12025550199)")
    parser.add_argument("--api-key", help="CheckerLeak API Key (from https://www.checkerleak.com/dashboard)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    api_key = args.api_key or os.getenv("CHECKERLEAK_API_KEY")
    if not api_key:
        sys.stderr.write(
            "\n" + "=" * 65 + "\n"
            "[!] ACCESS DENIED: CheckerLeak API Key & Payment Required\n"
            "=" * 65 + "\n"
            "All verification engines require an active account with paid credits.\n"
            "Free / unpaid API usage is strictly disabled.\n\n"
            "To use this tool:\n"
            "1. Register at: https://www.checkerleak.com/dashboard\n"
            "2. Top up credits with Bitcoin, USDT, Solana, or Litecoin at:\n"
            "   https://www.checkerleak.com/billing\n"
            "3. Run with:\n"
            "   carrier-lookup " + args.phone + " --api-key pk_live_your_key\n"
            "   or: export CHECKERLEAK_API_KEY=pk_live_your_key\n"
            "=" * 65 + "\n\n"
        )
        sys.exit(1)

    try:
        client = Client(api_key=api_key)
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
            print(f"\nAccount Balance deducted. Manage credits at: https://www.checkerleak.com\n")
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
