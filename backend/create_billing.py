with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

# Replace the entire <div id="clientPortalSection"> ... </div> with the Billing UI
portal_start = dash.find('<div id="clientPortalSection"')
portal_end = dash.find('<!-- ==================== CRYPTO TOP-UP MODAL ==================== -->')

if portal_start != -1 and portal_end != -1:
    head = dash[:portal_start]
    tail = dash[portal_end:]
    
    billing_html = """
    <!-- ==================== BILLING PORTAL ==================== -->
    <div id="billingPortalSection" class="bg-slate-50 border-b border-slate-200 py-8 px-4 sm:px-6 lg:px-8 min-h-screen">
      <div class="max-w-6xl mx-auto">
        
        <h1 class="text-2xl font-black text-slate-900 mb-6">Billing & Payment</h1>
        
        <!-- Tabs -->
        <div class="flex items-center gap-6 border-b border-slate-200 mb-8">
          <button class="pb-3 text-sm font-bold text-[#435ebf] border-b-2 border-[#435ebf]">Overview</button>
          <button class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-800 transition">Charging History</button>
          <button class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-800 transition">Transaction History</button>
        </div>

        <!-- Total Balance -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex items-center justify-between mb-8">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-xl bg-[#435ebf] text-white flex items-center justify-center">
              <i data-lucide="wallet" class="w-6 h-6"></i>
            </div>
            <div>
              <span class="text-xs font-bold text-slate-400 tracking-widest uppercase block mb-1">TOTAL BALANCE</span>
              <div class="text-3xl font-black text-[#435ebf] flex items-center gap-2">
                <span>$</span>
                <span id="billingBalance">0.00</span>
              </div>
            </div>
          </div>
          <button class="text-sm font-bold text-[#435ebf] hover:underline flex items-center gap-1">
            View all transactions <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>

        <!-- Packages -->
        <div class="mb-8">
          <div class="flex items-center gap-3 mb-4">
            <h3 class="font-bold text-slate-900">Recharge more, save more — <span class="text-[#435ebf]">up to 25% bonus</span></h3>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-[#435ebf] flex items-center gap-1 border border-blue-100"><i data-lucide="check" class="w-3 h-3"></i> Credited in full instantly · Funds never expire</span>
            <div class="flex-1"></div>
            <span class="text-xs font-semibold text-slate-400 flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-[#435ebf]"></span> Limited Time</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
            <!-- $100 -->
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-[#435ebf] transition cursor-pointer group flex flex-col justify-between">
              <div>
                <div class="text-2xl font-black text-slate-900 mb-1">$100</div>
                <div class="text-xs text-slate-500 mb-1 font-medium">→ get</div>
                <div class="text-lg font-bold text-slate-900">$105</div>
                <span class="inline-block px-1.5 py-0.5 bg-blue-50 text-[#435ebf] text-[10px] font-black rounded">+5%</span>
              </div>
              <button onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-slate-50 text-slate-600 font-bold text-xs group-hover:bg-blue-50 group-hover:text-[#435ebf] transition">Top up</button>
            </div>
            <!-- $200 -->
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-[#435ebf] transition cursor-pointer group flex flex-col justify-between">
              <div>
                <div class="text-2xl font-black text-slate-900 mb-1">$200</div>
                <div class="text-xs text-slate-500 mb-1 font-medium">→ get</div>
                <div class="text-lg font-bold text-slate-900">$220</div>
                <span class="inline-block px-1.5 py-0.5 bg-blue-50 text-[#435ebf] text-[10px] font-black rounded">+10%</span>
              </div>
              <button onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-slate-50 text-slate-600 font-bold text-xs group-hover:bg-blue-50 group-hover:text-[#435ebf] transition">Top up</button>
            </div>
            <!-- $500 -->
            <div class="bg-white rounded-xl border-2 border-[#435ebf] p-5 shadow-md relative cursor-pointer group flex flex-col justify-between transform hover:-translate-y-1 transition">
              <div class="absolute -top-3 inset-x-0 flex justify-center"><span class="bg-[#435ebf] text-white text-[10px] font-black px-2 py-0.5 rounded-full shadow-sm">Popular</span></div>
              <div>
                <div class="text-2xl font-black text-slate-900 mb-1">$500</div>
                <div class="text-xs text-slate-500 mb-1 font-medium">→ get</div>
                <div class="text-lg font-bold text-slate-900">$575</div>
                <span class="inline-block px-1.5 py-0.5 bg-blue-50 text-[#435ebf] text-[10px] font-black rounded">+15%</span>
              </div>
              <button onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-[#435ebf] text-white font-bold text-xs transition">Top up</button>
            </div>
            <!-- $1000 -->
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-[#435ebf] transition cursor-pointer group flex flex-col justify-between">
              <div>
                <div class="text-2xl font-black text-slate-900 mb-1">$1000</div>
                <div class="text-xs text-slate-500 mb-1 font-medium">→ get</div>
                <div class="text-lg font-bold text-slate-900">$1200</div>
                <span class="inline-block px-1.5 py-0.5 bg-blue-50 text-[#435ebf] text-[10px] font-black rounded">+20%</span>
              </div>
              <button onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-slate-50 text-slate-600 font-bold text-xs group-hover:bg-blue-50 group-hover:text-[#435ebf] transition">Top up</button>
            </div>
            <!-- $2000 -->
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-slate-800 transition cursor-pointer group relative flex flex-col justify-between">
              <div class="absolute -top-3 inset-x-0 flex justify-center"><span class="bg-slate-800 text-white text-[10px] font-black px-2 py-0.5 rounded-full shadow-sm">Best Value</span></div>
              <div>
                <div class="text-2xl font-black text-slate-900 mb-1">$2000</div>
                <div class="text-xs text-slate-500 mb-1 font-medium">→ get</div>
                <div class="text-lg font-bold text-slate-900">$2500</div>
                <span class="inline-block px-1.5 py-0.5 bg-blue-50 text-[#435ebf] text-[10px] font-black rounded">+25%</span>
              </div>
              <button onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-slate-50 text-slate-600 font-bold text-xs group-hover:bg-slate-800 group-hover:text-white transition">Top up</button>
            </div>
          </div>
        </div>

        <!-- Custom Amount -->
        <div class="mb-12">
          <h3 class="font-bold text-slate-900 mb-3 text-sm">Or enter a custom amount</h3>
          <div class="flex items-center gap-2 mb-4">
            <button onclick="document.getElementById('customAmt').value=20" class="px-3 py-1.5 rounded-lg border border-slate-200 bg-white text-xs font-semibold text-slate-600 hover:border-[#435ebf] hover:text-[#435ebf] transition">$20.00</button>
            <button onclick="document.getElementById('customAmt').value=50" class="px-3 py-1.5 rounded-lg border border-slate-200 bg-white text-xs font-semibold text-slate-600 hover:border-[#435ebf] hover:text-[#435ebf] transition">$50.00</button>
            <button onclick="document.getElementById('customAmt').value=100" class="px-3 py-1.5 rounded-lg border border-[#435ebf] bg-blue-50 text-xs font-bold text-[#435ebf] transition">$100.00 <span class="text-[10px] font-black">+5%</span></button>
          </div>
          
          <div class="flex items-center gap-4">
            <div class="relative flex-1 max-w-xl">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold">$</span>
              <input type="number" id="customAmt" placeholder="Enter amount" class="w-full pl-8 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-sm font-bold text-slate-900 focus:border-[#435ebf] focus:ring-1 focus:ring-[#435ebf] focus:outline-none transition">
            </div>
            <button onclick="topUpCredits()" class="px-6 py-3 bg-[#a8b8ff] hover:bg-[#435ebf] text-white font-bold rounded-xl text-sm transition shadow-sm">Add Funds</button>
          </div>
          <p class="text-[11px] text-slate-400 mt-3">Min $20 · Max $10,000</p>
          <p class="text-[11px] text-slate-400 mt-1">Corporate customers who need to pay via bank transfer or credit card, please <a href="#" class="text-[#435ebf] hover:underline">contact our customer service</a>.</p>
        </div>

        <!-- Charging History -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm mb-12">
          <div class="flex items-center justify-between mb-6">
            <h3 class="font-bold text-slate-900">Charging History</h3>
            <button class="text-xs font-bold text-[#435ebf] hover:underline">View more</button>
          </div>
          <div class="flex items-center justify-between py-4 border-t border-slate-100">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="font-bold text-slate-900 text-sm">Charge</span>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-600 border border-amber-100">Created</span>
              </div>
              <p class="text-xs text-slate-400 flex items-center gap-1">October 2, 2026 at 19:26:55 · Crypto <span class="text-[10px]">🪙</span></p>
            </div>
            <div class="flex items-center gap-4">
              <span class="font-bold text-amber-500">+$100.00</span>
              <button onclick="topUpCredits()" class="px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-600 hover:bg-slate-50 transition">View Payment</button>
            </div>
          </div>
        </div>

      </div>
    </div>
    """
    
    with open('app/static/billing.html', 'w', encoding='utf-8') as f:
        f.write(head + billing_html + tail)
    print("Created billing.html")
