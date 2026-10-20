# phone-carrier-lookup-js — Phone Carrier Lookup for Node.js

[![npm version](https://img.shields.io/npm/v/phone-carrier-lookup-js.svg?color=06b6d4)](https://www.npmjs.com/package/phone-carrier-lookup-js)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Powered by CheckerLeak](https://img.shields.io/badge/Powered%20By-CheckerLeak.com-blue)](https://www.checkerleak.com)

> **Lightweight Node.js library to detect mobile carrier, line type (mobile/landline/voip), and country for any international phone number.**  
> Official developer library powered by [CheckerLeak.com](https://www.checkerleak.com).

## 📦 Installation
```bash
npm install phone-carrier-lookup-js
```

## ⚡ Quickstart
```javascript
const { checkPhone } = require('phone-carrier-lookup-js');

async function run() {
  const res = await checkPhone('+12025550199');
  console.log(res);
}

run();
```

## 🚀 Full API Access & Free Credits
Register at [https://www.checkerleak.com](https://www.checkerleak.com) to access all 102 verification engines and deposit with BTC, USDT, SOL, LTC.
