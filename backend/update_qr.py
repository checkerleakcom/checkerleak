import os
import re

new_layout = """
          <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 mb-6 flex flex-col items-center text-center">
            <div class="bg-white p-3 rounded-2xl shadow-sm mb-4 inline-block border border-slate-100">
              <img src="/static/usdt_qr.png" alt="USDT TRC20 QR Code" class="w-32 h-32 object-contain">
            </div>
            <h4 class="text-sm font-bold text-slate-900 mb-1">Your USDT Address</h4>
            <p class="text-xs text-slate-500 mb-4 leading-relaxed max-w-xs">
              Use this address only to receive or deposit USDT on the Tron network.<br>
              Lost funds cannot be recovered.
            </p>
            
            <div class="w-full bg-white border border-slate-200 rounded-xl p-3 flex flex-col items-start relative text-left shadow-sm">
              <span class="text-[11px] font-bold text-slate-900 mb-1">Wallet Address</span>
              <code class="text-xs font-mono text-slate-600 break-all pr-8" id="cryptoAddress">TQoCuYoSMadJRo18K6D6HMrZEjb8zTFygN</code>
              <button onclick="navigator.clipboard.writeText('TQoCuYoSMadJRo18K6D6HMrZEjb8zTFygN'); const i = this.querySelector('i'); i.setAttribute('data-lucide', 'check'); lucide.createIcons(); setTimeout(() => { i.setAttribute('data-lucide', 'copy'); lucide.createIcons(); }, 2000);" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-800 transition p-1">
                <i data-lucide="copy" class="w-4 h-4"></i>
              </button>
            </div>
          </div>
"""

# The old block to replace starts with <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-6">
# and ends with the closing </div> right before <div class="space-y-4">

files = ['app/static/dashboard.html', 'app/static/billing.html', 'app/static/index.html']

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Try to find the block
        start_idx = content.find('<div class="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-6">')
        end_idx = content.find('<div class="space-y-4">', start_idx)
        
        if start_idx != -1 and end_idx != -1:
            # We replace from start_idx to end_idx with new_layout
            new_content = content[:start_idx] + new_layout.strip() + '\n\n          ' + content[end_idx:]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
