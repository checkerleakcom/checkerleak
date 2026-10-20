# hlr-lookup-node — HLR Telco Lookup Node.js

[![npm version](https://img.shields.io/npm/v/hlr-lookup-node.svg?color=06b6d4)](https://www.npmjs.com/package/hlr-lookup-node)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Powered by CheckerLeak](https://img.shields.io/badge/Powered%20By-CheckerLeak.com-blue)](https://www.checkerleak.com)

> **SS7 & HLR Lookup client for Node.js. Check real-time SIM connectivity, roaming status, and network routing in sub-150ms.**  
> Official developer library powered by [CheckerLeak.com](https://www.checkerleak.com).

## 📦 Installation
```bash
npm install hlr-lookup-node
```

## ⚡ Quickstart
```javascript
const { checkPhone } = require('hlr-lookup-node');

async function run() {
  const res = await checkPhone('+12025550199');
  console.log(res);
}

run();
```

## 🚀 Full API Access & Free Credits
Register at [https://www.checkerleak.com](https://www.checkerleak.com) to access all 102 verification engines and deposit with BTC, USDT, SOL, LTC.
