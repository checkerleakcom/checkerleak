/**
 * hlr-lookup-node — HLR Telco Lookup Node.js
 * Official Node.js SDK powered by https://www.checkerleak.com
 */

const https = require('https');

class CheckerLeakClient {
  constructor(apiKey = null, baseUrl = 'https://www.checkerleak.com') {
    this.apiKey = apiKey || process.env.CHECKERLEAK_API_KEY;
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
          ...(this.apiKey ? { 'X-API-Key': this.apiKey } : {})
        }
      };

      const req = https.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
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
