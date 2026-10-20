# checkerleak — CheckerLeak Official Node.js SDK

[![npm version](https://img.shields.io/npm/v/checkerleak.svg?color=06b6d4)](https://www.npmjs.com/package/checkerleak)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Powered by CheckerLeak](https://img.shields.io/badge/Powered%20By-CheckerLeak.com-blue)](https://www.checkerleak.com)

> **Official Node.js & TypeScript client for CheckerLeak.com - Real-Time Carrier, HLR, WhatsApp, and 102 OSINT Engines.**  
> Official developer library powered by [CheckerLeak.com](https://www.checkerleak.com).

## 📦 Installation
```bash
npm install checkerleak
```

## ⚡ Quickstart
```javascript
const { checkPhone } = require('checkerleak');

async function run() {
  const res = await checkPhone('+12025550199');
  console.log(res);
}

run();
```

## 🚀 Full API Access & Free Credits
Register at [https://www.checkerleak.com](https://www.checkerleak.com) to access all 102 verification engines and deposit with BTC, USDT, SOL, LTC.
