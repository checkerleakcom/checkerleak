import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

correct_grid = """      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        
        <!-- Card 1: WhatsApp -->
        <div class="bg-white hover:border-[#435ebf] border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition cursor-pointer group flex flex-col justify-between" onclick="window.location.href='/products/whatsapp-checker'">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
                <img src="/static/logos/whatsapp.png" class="w-8 h-8 object-contain" alt="WhatsApp">
              </div>
              <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase rounded bg-rose-500 text-white tracking-wider">HOT</span>
            </div>
            <h3 class="text-base font-bold text-slate-900 group-hover:text-[#435ebf] transition">WhatsApp Business & Personal</h3>
            <p class="text-xs text-slate-500 mt-2 leading-relaxed">
              Verify active accounts, profile photo availability, and business catalog presence. Eliminates dead outreach numbers.
            </p>
          </div>
          <div class="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="font-mono text-emerald-600 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-500"></span>Active Probe</span>
            <span class="font-semibold text-[#435ebf] group-hover:underline">Test Live &rarr;</span>
          </div>
        </div>

        <!-- Card 2: Apple iMessage -->
        <div class="bg-white hover:border-[#435ebf] border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition cursor-pointer group flex flex-col justify-between" onclick="window.location.href='/products/imessage-checker'">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
                <img src="/static/logos/apple.png" class="w-8 h-8 object-contain" alt="Apple">
              </div>
              <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase rounded bg-blue-600 text-white tracking-wider">BLUE BUBBLE</span>
            </div>
            <h3 class="text-base font-bold text-slate-900 group-hover:text-[#435ebf] transition">Apple iMessage & FaceTime</h3>
            <p class="text-xs text-slate-500 mt-2 leading-relaxed">
              Direct Apple IDS lookup to detect iPhone devices. Prioritize premium US & Europe sales leads with zero SMS carrier costs.
            </p>
          </div>
          <div class="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="font-mono text-blue-600 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-blue-500"></span>Apple IDS Probe</span>
            <span class="font-semibold text-[#435ebf] group-hover:underline">Test Live &rarr;</span>
          </div>
        </div>
  
        <!-- Card 3: Telegram -->
        <div class="bg-white hover:border-[#435ebf] border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition cursor-pointer group flex flex-col justify-between" onclick="window.location.href='/products/telegram-checker'">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center font-bold">
                <img src="/static/logos/telegram.png" class="w-8 h-8 object-contain" alt="Telegram">
              </div>
              <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase rounded bg-purple-600 text-white tracking-wider">NEW</span>
            </div>
            <h3 class="text-base font-bold text-slate-900 group-hover:text-[#435ebf] transition">Telegram & Handle Discovery</h3>
            <p class="text-xs text-slate-500 mt-2 leading-relaxed">
              Verify active Telegram peers via native MTProto. Estimate account age in days and inspect public @handles.
            </p>
          </div>
          <div class="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="font-mono text-sky-600 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-sky-500"></span>MTProto Active</span>
            <span class="font-semibold text-[#435ebf] group-hover:underline">Test Live &rarr;</span>
          </div>
        </div>
  
        <!-- Card 4: Binance Crypto -->
        <div class="bg-white hover:border-[#435ebf] border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition cursor-pointer group flex flex-col justify-between" onclick="window.location.href='/products/binance-email-checker'">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
                <img src="/static/logos/binance.png" class="w-8 h-8 object-contain" alt="Binance">
              </div>
              <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase rounded bg-amber-500 text-white tracking-wider">CRYPTO</span>
            </div>
            <h3 class="text-base font-bold text-slate-900 group-hover:text-[#435ebf] transition">Binance & Exchange Verification</h3>
            <p class="text-xs text-slate-500 mt-2 leading-relaxed">
              Multi-layer crypto verification: SMTP deliverability exclusion, Web3 cryptographic footprinting, and upstream cluster checking.
            </p>
          </div>
          <div class="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="font-mono text-amber-600 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500"></span>Web3 Probe</span>
            <span class="font-semibold text-[#435ebf] group-hover:underline">Test Live &rarr;</span>
          </div>
        </div>
  
        <!-- Card 5: Revolut Neobank -->
        <div class="bg-white hover:border-[#435ebf] border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition cursor-pointer group flex flex-col justify-between" onclick="window.location.href='/products/revolut-checker'">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 rounded-xl bg-white border border-slate-200 flex items-center justify-center font-bold">
                  <img src="/static/logos/revolut.png" class="w-8 h-8 object-contain drop-shadow-sm" alt="Revolut">
              </div>
              <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase rounded bg-emerald-600 text-white tracking-wider">NEOBANK</span>
            </div>
            <h3 class="text-base font-bold text-slate-900 group-hover:text-[#435ebf] transition">Revolut & Neobank Pay</h3>
            <p class="text-xs text-slate-500 mt-2 leading-relaxed">
              Detect active Revtag payments across Europe, UK, and Americas. Verify financial buying power without credit agency delays.
            </p>
          </div>
          <div class="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="font-mono text-slate-800 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-slate-800"></span>FinTech Ready</span>
            <span class="font-semibold text-[#435ebf] group-hover:underline">Test Live &rarr;</span>
          </div>
        </div>
  
        <!-- Card 6: Carrier & Fraud -->
        <div class="bg-white hover:border-[#435ebf] border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition cursor-pointer group flex flex-col justify-between" onclick="window.location.href='/products/carrier-detection'">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center font-bold">
                <svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#DC2626"/><path d="M12 6l5 2v5c0 3-2.5 5.5-5 6.5-2.5-1-5-3.5-5-6.5V8l5-2z" fill="#fff"/></svg>
              </div>
              <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase rounded bg-rose-600 text-white tracking-wider">FRAUD SHIELD</span>
            </div>
            <h3 class="text-base font-bold text-slate-900 group-hover:text-[#435ebf] transition">Carrier HLR & VoIP Shield</h3>
            <p class="text-xs text-slate-500 mt-2 leading-relaxed">
              Identify authentic Mobile Network Operators (MNOs), MVNOs, recent SIM swaps, and eliminate temporary burner fraud.
            </p>
          </div>
          <div class="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs">
            <span class="font-mono text-rose-600 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-rose-500"></span>SS7 / HLR Probe</span>
            <span class="font-semibold text-[#435ebf] group-hover:underline">Test Live &rarr;</span>
          </div>
        </div>
  
      </div>"""

# Find the start of the grid
start_idx = html.find('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">')
# Find the end by looking for the CTA button after it
end_idx = html.find('<!-- The Central High-Impact CTA Button')

if start_idx != -1 and end_idx != -1:
    new_html = html[:start_idx] + correct_grid + '\n\n      ' + html[end_idx:]
    with open('app/static/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Fixed grid!")
else:
    print("Could not find bounds.")
