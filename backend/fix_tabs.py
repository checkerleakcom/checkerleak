import re

with open('app/static/billing.html', 'r', encoding='utf-8') as f:
    d = f.read()

tabs_html = """
        <!-- Tabs -->
        <div class="flex items-center gap-6 border-b border-slate-200 mb-8" id="billingTabsMenu">
          <button onclick="switchBillingTab('overview', this)" class="pb-3 text-sm font-bold text-[#435ebf] border-b-2 border-[#435ebf]">Overview</button>
          <button onclick="switchBillingTab('charging', this)" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-800 transition">Charging History</button>
          <button onclick="switchBillingTab('transaction', this)" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-800 transition">Transaction History</button>
        </div>
"""

# Replace Tabs
d = re.sub(r'<!-- Tabs -->.*?</div>', tabs_html, d, flags=re.DOTALL)

# Wrap Overview
overview_start = d.find('<!-- Total Balance -->')
overview_end = d.find('<!-- Charging History -->')
if overview_start != -1 and overview_end != -1:
    d = d[:overview_start] + '<div id="billingOverview">\n' + d[overview_start:overview_end] + '</div>\n' + d[overview_end:]

# Wrap Charging History
charging_start = d.find('<!-- Charging History -->')
charging_end = d.find('</div>\n    </div>\n    <!-- ==================== CRYPTO TOP-UP MODAL ==================== -->')
if charging_start != -1 and charging_end != -1:
    d = d[:charging_start] + '<div id="billingChargingHistory">\n' + d[charging_start:charging_end] + '</div>\n<div id="billingTransactionHistory" class="hidden"><div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm mb-12 text-center text-slate-400 py-12">No transactions recorded yet.</div></div>\n' + d[charging_end:]

# Add JS function
js_func = """
    function switchBillingTab(tab, btnElement) {
      document.getElementById('billingOverview').classList.add('hidden');
      document.getElementById('billingChargingHistory').classList.add('hidden');
      document.getElementById('billingTransactionHistory').classList.add('hidden');
      
      const menu = document.getElementById('billingTabsMenu');
      const buttons = menu.querySelectorAll('button');
      buttons.forEach(b => {
        b.className = 'pb-3 text-sm font-semibold text-slate-500 hover:text-slate-800 transition';
      });

      btnElement.className = 'pb-3 text-sm font-bold text-[#435ebf] border-b-2 border-[#435ebf]';

      if (tab === 'overview') {
        document.getElementById('billingOverview').classList.remove('hidden');
        document.getElementById('billingChargingHistory').classList.remove('hidden'); // Overview shows both
      } else if (tab === 'charging') {
        document.getElementById('billingChargingHistory').classList.remove('hidden');
      } else if (tab === 'transaction') {
        document.getElementById('billingTransactionHistory').classList.remove('hidden');
      }
    }
"""

d = d.replace('function topUpCredits() {', js_func + '\n    function topUpCredits() {')

with open('app/static/billing.html', 'w', encoding='utf-8') as f:
    f.write(d)
print("Tabs fixed!")
