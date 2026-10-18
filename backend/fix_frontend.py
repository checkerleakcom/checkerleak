import re

def fix_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add Toast Container if not exists
    if '<div id="toast-container"' not in html:
        toast_html = """
  <!-- Toast Notification Container -->
  <div id="toast-container" class="fixed bottom-5 right-5 z-[200] flex flex-col gap-2"></div>
        """
        html = html.replace('<!-- ==================== CRYPTO TOP-UP MODAL ==================== -->', toast_html + '\n  <!-- ==================== CRYPTO TOP-UP MODAL ==================== -->')

    # 2. Update Copy Button to use Toast and check icon (for both addresses)
    # The modal code has: navigator.clipboard.writeText('TQoCuYoSMadJRo18K6D6HMrZEjb8zTFygN'); ...
    html = re.sub(r'alert\(\'Copied!\'\)', 'showToast(\'Wallet address copied successfully!\', \'success\')', html)
    
    # 3. Add Custom Amount Add Funds onClick if it's billing.html
    if 'billing.html' in filepath:
        # Pre-fill modal for packages
        html = html.replace('onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-slate-50', 'onclick="topUpCredits(100, 105)" class="w-full mt-4 py-2 rounded-lg bg-slate-50', 1)
        html = html.replace('onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-slate-50', 'onclick="topUpCredits(200, 220)" class="w-full mt-4 py-2 rounded-lg bg-slate-50', 1)
        html = html.replace('onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-[#435ebf]', 'onclick="topUpCredits(500, 575)" class="w-full mt-4 py-2 rounded-lg bg-[#435ebf]', 1)
        html = html.replace('onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-slate-50', 'onclick="topUpCredits(1000, 1200)" class="w-full mt-4 py-2 rounded-lg bg-slate-50', 1)
        html = html.replace('onclick="topUpCredits()" class="w-full mt-4 py-2 rounded-lg bg-slate-50', 'onclick="topUpCredits(2000, 2500)" class="w-full mt-4 py-2 rounded-lg bg-slate-50', 1)
        
        # Replace custom "Add Funds" button logic
        custom_btn_pattern = r'<button onclick="topUpCredits\(\)" class="px-6 py-3 bg-\[#a8b8ff\].*?>Add Funds</button>'
        custom_btn_replacement = '<button onclick="const a = parseFloat(document.getElementById(\'customAmt\').value); if(a>=20) { topUpCredits(a, a>99?a*1.05:a); } else { showToast(\'Minimum amount is $20\', \'error\'); }" class="px-6 py-3 bg-[#a8b8ff] hover:bg-[#435ebf] text-white font-bold rounded-xl text-sm transition shadow-sm">Add Funds</button>'
        html = re.sub(custom_btn_pattern, custom_btn_replacement, html)
        
        # Add Bonus Notice to Modal
        if 'id="bonusNotice"' not in html:
            html = html.replace('<label class="block text-xs font-semibold text-slate-700 mb-1">Amount Sent (USDT)</label>', '<label class="flex justify-between items-center text-xs font-semibold text-slate-700 mb-1"><span>Amount Sent (USDT)</span><span id="bonusNotice" class="text-emerald-600 font-bold text-[10px]"></span></label>')

    # 4. Replace JS Logic
    js_to_replace = r'function topUpCredits\(\) \{.*\}'
    new_js = """
    function showToast(message, type = 'success') {
      const container = document.getElementById('toast-container');
      if (!container) return;
      const toast = document.createElement('div');
      toast.className = `px-4 py-3 rounded-lg shadow-lg text-sm font-bold text-white transform transition-all duration-300 translate-y-10 opacity-0 flex items-center gap-2 ${type === 'success' ? 'bg-emerald-500' : 'bg-rose-500'}`;
      toast.innerHTML = `<i data-lucide="${type === 'success' ? 'check-circle-2' : 'alert-circle'}" class="w-4 h-4"></i> ${message}`;
      container.appendChild(toast);
      lucide.createIcons();
      
      // Animate in
      setTimeout(() => {
        toast.classList.remove('translate-y-10', 'opacity-0');
      }, 10);
      
      // Animate out
      setTimeout(() => {
        toast.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
      }, 3000);
    }

    function topUpCredits(amount = null, finalCredits = null) {
      if (amount !== null) {
        document.getElementById('cryptoAmountInput').value = amount;
      }
      const notice = document.getElementById('bonusNotice');
      if (notice && finalCredits !== null && finalCredits > amount) {
        notice.innerText = `+ You will receive $${finalCredits} Credits!`;
      } else if (notice) {
        notice.innerText = '';
      }
      document.getElementById('cryptoTopUpModal').classList.remove('hidden');
    }

    function closeCryptoModal() {
      document.getElementById('cryptoTopUpModal').classList.add('hidden');
    }

    async function submitCryptoPayment() {
      const amt = document.getElementById('cryptoAmountInput').value;
      const txid = document.getElementById('cryptoTxidInput').value;
      
      if (!amt || !txid) {
        showToast("Please enter both the Amount and the TxID.", 'error');
        return;
      }

      const stored = localStorage.getItem("pulsecheck_client");
      const email = stored ? JSON.parse(stored).email : 'unknown';
      
      try {
        const response = await fetch('/api/v1/billing/submit-txid', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ amount: parseFloat(amt), txid: txid, client_email: email })
        });
        
        if (response.ok) {
          showToast("Payment submitted successfully!", 'success');
          
          // Update persistence state
          if (stored) {
             const user = JSON.parse(stored);
             user.pendingTx = true;
             localStorage.setItem("pulsecheck_client", JSON.stringify(user));
          }
          
          closeCryptoModal();
          updatePendingUI();
        } else {
          showToast("Error submitting payment.", 'error');
        }
      } catch (err) {
        showToast("Network error. Please try again.", 'error');
      }
    }

    function updatePendingUI() {
      const stored = localStorage.getItem("pulsecheck_client");
      if (stored) {
         const user = JSON.parse(stored);
         if (user.pendingTx) {
            const walletCount = document.getElementById('portalCreditCount');
            const bBalance = document.getElementById('billingBalance');
            if (walletCount) {
              walletCount.innerHTML = `<span class="text-[10px] text-amber-500 font-bold ml-2 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">⏳ PENDING VERIFICATION</span>`;
            }
            if (bBalance) {
              bBalance.innerHTML = `<span class="text-amber-500 font-bold text-lg px-2 py-1 bg-amber-50 rounded border border-amber-200 mt-2 block">⏳ Transaction Pending Verification...</span>`;
            }
         }
      }
    }
    """
    
    # We must cleanly replace topUpCredits, closeCryptoModal, submitCryptoPayment
    # Let's find the script block
    start_js = html.find('function topUpCredits() {')
    end_js = html.find('// Load user details')
    if start_js != -1 and end_js != -1:
        html = html[:start_js] + new_js + '\n    ' + html[end_js:]
        
    # Hook updatePendingUI into DOMContentLoaded
    load_pattern = r'document\.addEventListener\("DOMContentLoaded", \(\) => \{'
    if 'updatePendingUI()' not in html:
        html = re.sub(load_pattern, 'document.addEventListener("DOMContentLoaded", () => {\n      updatePendingUI();', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed {filepath}")

fix_html('app/static/billing.html')
fix_html('app/static/dashboard.html')
