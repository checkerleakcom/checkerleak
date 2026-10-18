import re

with open('app/static/dashboard.html', 'r', encoding='utf-8') as f:
    d = f.read()

# 1. Fix "All Products" link in header
d = d.replace('onclick="openFullDirectoryModal()"', 'onclick="document.getElementById(\'servicesDirectoryContainer\').scrollIntoView({behavior: \'smooth\'})"')

# 2. Fix Tool 01 and Tool 02
d = d.replace("onclick=\"document.getElementById('live-tester').scrollIntoView({behavior: 'smooth'})\"", "onclick=\"document.getElementById('servicesDirectoryContainer').scrollIntoView({behavior: 'smooth'})\"")
d = d.replace("onclick=\"switchTab('bulk'); document.getElementById('demos').scrollIntoView({behavior: 'smooth'})\"", "onclick=\"document.getElementById('servicesDirectoryContainer').scrollIntoView({behavior: 'smooth'})\"")

# 3. Inject missing JS functions before the closing </script>
missing_js = """
    function copyApiKey() {
      navigator.clipboard.writeText(document.getElementById('portalApiKey').innerText);
      const btn = document.getElementById('copyKeyBtn');
      const originalText = btn.innerText;
      btn.innerText = 'Copied!';
      btn.classList.replace('bg-slate-200', 'bg-emerald-100');
      btn.classList.replace('text-slate-700', 'text-emerald-700');
      setTimeout(() => {
        btn.innerText = originalText;
        btn.classList.replace('bg-emerald-100', 'bg-slate-200');
        btn.classList.replace('text-emerald-700', 'text-slate-700');
      }, 2000);
    }

    function loadUserHistory() {
      const tbody = document.getElementById('portalHistoryBody');
      tbody.innerHTML = `<tr><td colspan="6" class="py-6 text-center text-slate-400 font-sans"><i data-lucide="loader" class="w-4 h-4 animate-spin inline-block mx-auto mb-2"></i><br>Syncing blockchain ledger...</td></tr>`;
      lucide.createIcons();
      setTimeout(() => {
        tbody.innerHTML = `<tr><td colspan="6" class="py-6 text-center text-slate-400 font-sans">No verifications recorded yet.</td></tr>`;
      }, 1000);
    }

    function renderHeaderAuth() {
      const area = document.getElementById('authHeaderArea');
      if (!area) return;
      const stored = localStorage.getItem("pulsecheck_client");
      if (stored) {
        const user = JSON.parse(stored);
        const initial = user.firstName.charAt(0).toUpperCase();
        area.innerHTML = `
          <div class="relative group">
            <button class="flex items-center gap-2 px-1.5 py-1.5 rounded-full border border-slate-200 hover:border-slate-300 transition bg-slate-50">
              <div class="w-7 h-7 rounded-full bg-[#435ebf] text-white flex items-center justify-center font-bold text-xs">${initial}</div>
              <span class="text-xs font-bold text-slate-700 pr-2">${user.firstName}</span>
            </button>
            <div class="absolute right-0 top-full mt-2 w-48 bg-white border border-slate-200 shadow-xl rounded-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
              <a href="/dashboard" class="block px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50 hover:text-[#435ebf] border-b border-slate-100">Dashboard</a>
              <button onclick="logout()" class="w-full text-left px-4 py-2.5 text-sm font-semibold text-rose-600 hover:bg-rose-50 rounded-b-xl transition">Log out</button>
            </div>
          </div>
        `;
      }
    }

    function logout() {
      localStorage.removeItem("pulsecheck_client");
      window.location.href = "/";
    }

    // Call renderHeaderAuth on load
    document.addEventListener('DOMContentLoaded', () => {
      renderHeaderAuth();
    });
"""

d = d.replace('</script>\n</body>\n</html>', missing_js + '\n</script>\n</body>\n</html>')

with open('app/static/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(d)

print("QA fixes applied successfully!")
