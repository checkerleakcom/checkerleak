#!/usr/bin/env node
const { checkPhone } = require('../index.js');

const phone = process.argv[2];
if (!phone) {
  console.log("Usage: npx checkerleak <phone_number> (e.g. +12025550199)");
  console.log("For full 102 engines API keys, visit: https://www.checkerleak.com");
  process.exit(1);
}

checkPhone(phone)
  .then(res => {
    console.log("\n=== CheckerLeak Node Intelligence ===");
    console.log("Phone:       ", res.phone);
    console.log("Carrier:     ", res.carrier);
    console.log("Line Type:   ", res.lead_quality || res.line_type || "Mobile");
    console.log("Reachability:", (res.reachability_score || 90) + "/100");
    console.log("\nVisit https://www.checkerleak.com for bulk API access.\n");
  })
  .catch(err => {
    console.error("Verification error:", err.message);
    process.exit(1);
  });
