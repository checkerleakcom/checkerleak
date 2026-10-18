with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    d = f.read()

# Change grid-cols-2 back to grid-cols-3
d = d.replace('<div class="grid grid-cols-1 md:grid-cols-2 gap-4">', '<div class="grid grid-cols-1 md:grid-cols-3 gap-4">')

tab3 = """
          <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between cursor-pointer hover:border-[#435ebf] transition" onclick="document.getElementById('ledgerSection').classList.toggle('hidden'); document.getElementById('ledgerSection').scrollIntoView({behavior: 'smooth'})">
            <div>
              <span class="text-xs text-slate-500 font-semibold uppercase block">Tool 03</span>
              <span class="font-bold text-slate-900">Verifications Ledger</span>
            </div>
            <div class="w-8 h-8 rounded-lg bg-blue-50 text-[#435ebf] flex items-center justify-center">
              <i data-lucide="history" class="w-4 h-4"></i>
            </div>
          </div>
"""

tool2_pattern = """<span class="font-bold text-slate-900">Bulk CSV Cleaning Studio</span>
            </div>
            <div class="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <i data-lucide="layers" class="w-4 h-4"></i>
            </div>
          </div>"""

d = d.replace(tool2_pattern, tool2_pattern + tab3)

# Hide the Ledger by default and add id
d = d.replace('<div class="lg:col-span-12 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">', 
              '<div id="ledgerSection" class="hidden lg:col-span-12 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm mb-12">')

with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(d)
print('Updated Layout')
