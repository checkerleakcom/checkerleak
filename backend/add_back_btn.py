with open('app/static/billing.html', 'r', encoding='utf-8') as f:
    d = f.read()

# 1. Add "Back to Dashboard" button above the title
back_btn = """
        <a href="/dashboard" class="inline-flex items-center gap-1.5 text-sm font-semibold text-slate-500 hover:text-[#435ebf] transition mb-4">
          <i data-lucide="arrow-left" class="w-4 h-4"></i> Back to Dashboard
        </a>
"""

if "Back to Dashboard" not in d:
    d = d.replace('<h1 class="text-2xl font-black text-slate-900 mb-6">Billing & Payment</h1>', back_btn + '        <h1 class="text-2xl font-black text-slate-900 mb-6">Billing & Payment</h1>')

# 2. Fix the "All Products" link in the header of billing.html
# It currently scrolls to the container which doesn't exist. We should point it to /dashboard
wrong_href = 'href="javascript:void(0)" onclick="document.getElementById(\'servicesDirectoryContainer\').scrollIntoView({behavior: \'smooth\'})"'
right_href = 'href="/dashboard"'
d = d.replace(wrong_href, right_href)

# 3. Fix the Logo link to go to /dashboard instead of /
d = d.replace('<a href="/" class="flex items-center gap-2.5">', '<a href="/dashboard" class="flex items-center gap-2.5">')

with open('app/static/billing.html', 'w', encoding='utf-8') as f:
    f.write(d)
    
print("Added Back to Dashboard button!")
