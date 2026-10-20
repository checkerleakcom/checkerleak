/**
 * phone-carrier-lookup-js — Phone Carrier Lookup for Node.js
 * Official Node.js SDK powered by https://www.checkerleak.com
 */

const https = require('https');

class CheckerLeakClient {
  constructor(apiKey = null, baseUrl = 'https://www.checkerleak.com') {
    this.apiKey = apiKey || process.env.CHECKERLEAK_API_KEY;
    if (!this.apiKey) {
      throw new Error(
        "CheckerLeak API Key is required. Unpaid access is strictly disabled. Please register and purchase credits with Bitcoin, USDT, Solana, or Litecoin at https://www.checkerleak.com/dashboard"
      );
    }
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  async verify(phone) {
    return new Promise((resolve, reject) => {
      const data = JSON.stringify({ phone });
      const url = new URL(`${this.baseUrl}/v1/verify`);

      const options = {
        hostname: url.hostname,
        port: url.port || 443,
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(data),
          'X-API-Key': this.apiKey,
          'User-Agent': 'checkerleak-node-sdk/1.0.2'
        }
      };

      const req = https.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            if (res.statusCode === 401) {
              return reject(new Error("Invalid CheckerLeak API Key. Check dashboard at https://www.checkerleak.com"));
            }
            if (res.statusCode === 402) {
              return reject(new Error("Payment Required: Insufficient credits. Top up with crypto at https://www.checkerleak.com/billing"));
            }
            resolve(JSON.parse(body));
          } catch (err) {
            reject(new Error(`Failed to parse response: ${body}`));
          }
        });
      });

      req.on('error', reject);
      req.write(data);
      req.end();
    });
  }
}

async function checkPhone(phone, apiKey = null) {
  const client = new CheckerLeakClient(apiKey);
  return client.verify(phone);
}

module.exports = {
  CheckerLeakClient,
  checkPhone
};
