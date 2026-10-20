#!/usr/bin/env node
const { checkPhone } = require('../index.js');

const phone = process.argv[2];
const apiKey = process.env.CHECKERLEAK_API_KEY || (process.argv.indexOf('--api-key') !== -1 ? process.argv[process.argv.indexOf('--api-key') + 1] : null);

if (!phone || !apiKey) {
  console.error("\n==============================================================");
  console.error("[!] ACCESS DENIED: CheckerLeak API Key & Payment Required");
  console.error("==============================================================");
  console.error("Commercial API access requires an active account with paid credits.");
  console.error("1. Register at: https://www.checkerleak.com/dashboard");
  console.error("2. Purchase credits with BTC/USDT/SOL/LTC: https://www.checkerleak.com/billing");
  console.error("3. Usage: npx checkerleak <phone> --api-key pk_live_your_key");
  console.error("==============================================================\n");
  process.exit(1);
}

checkPhone(phone, apiKey)
  .then(res => {
    console.log("\n=== CheckerLeak Node Intelligence ===");
    console.log("Phone:       ", res.phone);
    console.log("Carrier:     ", res.carrier);
    console.log("Line Type:   ", res.lead_quality || res.line_type || "Mobile");
    console.log("Reachability:", (res.reachability_score || 90) + "/100");
    console.log("\nAccount balance deducted. Visit https://www.checkerleak.com/billing for more credits.\n");
  })
  .catch(err => {
    console.error("Verification error:", err.message);
    process.exit(1);
  });
