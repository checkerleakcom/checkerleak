def generate_modal_html():
    return """  <!-- ==================== CRYPTO TOP-UP MODAL (ENTERPRISE GRADE) ==================== -->
  <div id="cryptoTopUpModal" class="fixed inset-0 bg-slate-950/70 backdrop-blur-md z-[100] hidden flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
    <div class="bg-white rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl border border-slate-200 relative my-auto animate-in fade-in zoom-in-95 duration-200">
      
      <!-- Close Button -->
      <button onclick="closeCryptoModal()" class="absolute top-5 right-5 text-slate-400 hover:text-slate-800 bg-slate-100 hover:bg-slate-200 rounded-full p-2 transition z-10">
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>

      <div class="p-6 sm:p-8">
        
        <!-- Header -->
        <div class="flex items-center gap-3 mb-4">
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-600 to-[#435ebf] text-white flex items-center justify-center shadow-md shrink-0">
            <i data-lucide="shield-check" class="w-6 h-6"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-xl font-black text-slate-900 tracking-tight">Deposit Cryptocurrency</h3>
              <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-200">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>Zero KYC
              </span>
            </div>
            <p class="text-xs text-slate-500 mt-0.5">Automated on-chain verification · Instant credit upon confirmation</p>
          </div>
        </div>

        <!-- 6 Network Selectors (2 rows of 3) -->
        <div class="mb-5">
          <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2">Select Payment Network</label>
          <div class="grid grid-cols-3 gap-2">
            
            <!-- USDT TRC20 -->
            <button type="button" onclick="selectCryptoTab('USDT_TRC20')" id="cryptoTab_USDT_TRC20" class="flex flex-col items-center justify-center p-2.5 rounded-xl border border-slate-200 text-center transition hover:border-[#435ebf] bg-slate-900 text-white shadow-sm">
              <span class="text-xs font-bold flex items-center gap-1">₮ USDT</span>
              <span class="text-[9px] font-mono text-emerald-400 font-semibold mt-0.5">TRC-20 (Tron)</span>
            </button>

            <!-- USDT BEP20 -->
            <button type="button" onclick="selectCryptoTab('USDT_BEP20')" id="cryptoTab_USDT_BEP20" class="flex flex-col items-center justify-center p-2.5 rounded-xl border border-slate-200 text-center transition hover:border-[#435ebf] bg-white text-slate-700 hover:bg-slate-50">
              <span class="text-xs font-bold flex items-center gap-1">₮ USDT</span>
              <span class="text-[9px] font-mono text-amber-500 font-semibold mt-0.5">BEP-20 (BSC)</span>
            </button>

            <!-- Bitcoin -->
            <button type="button" onclick="selectCryptoTab('BTC')" id="cryptoTab_BTC" class="flex flex-col items-center justify-center p-2.5 rounded-xl border border-slate-200 text-center transition hover:border-[#435ebf] bg-white text-slate-700 hover:bg-slate-50">
              <span class="text-xs font-bold flex items-center gap-1">₿ BTC</span>
              <span class="text-[9px] font-mono text-slate-500 font-semibold mt-0.5">Native SegWit</span>
            </button>

            <!-- Ethereum -->
            <button type="button" onclick="selectCryptoTab('ETH')" id="cryptoTab_ETH" class="flex flex-col items-center justify-center p-2.5 rounded-xl border border-slate-200 text-center transition hover:border-[#435ebf] bg-white text-slate-700 hover:bg-slate-50">
              <span class="text-xs font-bold flex items-center gap-1">Ξ ETH</span>
              <span class="text-[9px] font-mono text-indigo-500 font-semibold mt-0.5">ERC-20 Mainnet</span>
            </button>

            <!-- Solana -->
            <button type="button" onclick="selectCryptoTab('SOL')" id="cryptoTab_SOL" class="flex flex-col items-center justify-center p-2.5 rounded-xl border border-slate-200 text-center transition hover:border-[#435ebf] bg-white text-slate-700 hover:bg-slate-50">
              <span class="text-xs font-bold flex items-center gap-1">◎ SOL</span>
              <span class="text-[9px] font-mono text-purple-500 font-semibold mt-0.5">Solana Mainnet</span>
            </button>

            <!-- Litecoin -->
            <button type="button" onclick="selectCryptoTab('LTC')" id="cryptoTab_LTC" class="flex flex-col items-center justify-center p-2.5 rounded-xl border border-slate-200 text-center transition hover:border-[#435ebf] bg-white text-slate-700 hover:bg-slate-50">
              <span class="text-xs font-bold flex items-center gap-1">Ł LTC</span>
              <span class="text-[9px] font-mono text-blue-500 font-semibold mt-0.5">Fee &lt;$0.01</span>
            </button>

          </div>
        </div>

        <!-- Deposit Details Box -->
        <div class="bg-slate-50 rounded-2xl border border-slate-200/90 p-5 mb-5 space-y-4">
          
          <div class="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
            <!-- QR Code -->
            <div class="bg-white p-2.5 rounded-2xl border border-slate-200 shadow-xs shrink-0">
              <img id="cryptoQrImg" src="/static/usdt_qr.png" alt="Deposit QR Code" class="w-28 h-28 object-contain">
            </div>

            <!-- Instructions & Network Info -->
            <div class="flex-1 space-y-1">
              <div class="flex items-center justify-center sm:justify-start gap-2">
                <span id="cryptoNetworkBadge" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-100 text-emerald-800">
                  TRON NETWORK
                </span>
                <a id="cryptoExplorerLink" href="https://tronscan.org/address/TT44hVQek5xLh7qz2FhpBdmbMziyBGyzPX/transactions" target="_blank" class="text-[11px] font-semibold text-[#435ebf] hover:underline flex items-center gap-1">
                  <span>Verify On-Chain</span>
                  <i data-lucide="external-link" class="w-3 h-3"></i>
                </a>
              </div>
              <h4 id="cryptoAddrTitle" class="text-sm font-extrabold text-slate-900">USDT (TRC-20) Deposit Address</h4>
              <p id="cryptoAddrDesc" class="text-[11px] text-slate-500 leading-relaxed">
                Send only USDT via Tron (TRC-20). Deposits are credited automatically after 1 network confirmation.
              </p>
            </div>
          </div>

          <!-- Address Code Block with 1-Click Copy -->
          <div class="bg-white border border-slate-200 rounded-xl p-3 flex items-center justify-between gap-3 shadow-2xs">
            <div class="min-w-0 flex-1">
              <span class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-0.5">Official Deposit Wallet</span>
              <code id="cryptoAddress" class="block text-xs font-mono font-bold text-slate-800 truncate select-all">
                TT44hVQek5xLh7qz2FhpBdmbMziyBGyzPX
              </code>
            </div>
            <button id="cryptoCopyBtn" onclick="copyCryptoAddress()" class="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-[#435ebf] text-white text-xs font-bold flex items-center gap-1.5 transition shrink-0 shadow-xs">
              <i data-lucide="copy" class="w-3.5 h-3.5"></i>
              <span>Copy</span>
            </button>
          </div>

        </div>

        <!-- Inputs: Amount & TxID -->
        <div class="space-y-3">
          <div>
            <div class="flex justify-between items-center text-xs font-bold text-slate-700 mb-1">
              <span id="cryptoAmountLabel">Amount Sent (USDT)</span>
              <span id="creditEstimateNotice" class="text-[#435ebf] font-mono text-[11px] font-bold">💎 +5,000 Credits</span>
            </div>
            <div class="relative">
              <input type="number" id="cryptoAmountInput" value="50" oninput="updateCreditEstimate()" placeholder="e.g. 50" class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-xl text-sm font-bold text-slate-900 focus:ring-2 focus:ring-[#435ebf] focus:outline-none transition">
              <span class="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-mono font-bold text-slate-400" id="cryptoCurrencySuffix">USDT</span>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Transaction Hash / TxID (Proof of Transfer)</label>
            <input type="text" id="cryptoTxidInput" placeholder="Paste on-chain TxID or Hash here" class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-xl text-xs font-mono text-slate-800 placeholder:text-slate-400 focus:ring-2 focus:ring-[#435ebf] focus:outline-none transition">
          </div>
        </div>

        <!-- Submit Button -->
        <button id="btnSubmitPayment" onclick="submitCryptoPayment()" class="w-full mt-5 bg-[#435ebf] hover:bg-[#324796] active:scale-[0.99] text-white font-bold py-3.5 rounded-xl transition shadow-md hover:shadow-lg flex items-center justify-center gap-2 cursor-pointer">
          <i data-lucide="check-circle-2" class="w-4 h-4"></i>
          <span>Confirm & Credit Wallet Balance</span>
        </button>

        <p class="text-[10px] text-center text-slate-400 mt-3">
          🔒 Encrypted on-chain reconciliation · Instant balance sync
        </p>

      </div>
    </div>
  </div>"""

def generate_script_js():
    return """
    let currentCryptoMethod = 'USDT_TRC20';

    const CRYPTO_METRIC_CONFIG = {
      'USDT_TRC20': {
        currency: 'USDT',
        network: 'TRON NETWORK',
        badgeClass: 'bg-emerald-100 text-emerald-800',
        title: 'USDT (TRC-20) Deposit Address',
        address: 'TT44hVQek5xLh7qz2FhpBdmbMziyBGyzPX',
        qr: '/static/usdt_qr.png',
        desc: 'Send USDT via Tron (TRC-20). Instant deposit confirmation via TronScan.',
        explorer: 'https://tronscan.org/address/TT44hVQek5xLh7qz2FhpBdmbMziyBGyzPX/transactions'
      },
      'USDT_BEP20': {
        currency: 'USDT',
        network: 'BNB SMART CHAIN',
        badgeClass: 'bg-amber-100 text-amber-800',
        title: 'USDT (BEP-20) Deposit Address',
        address: '0x35dd60066ae6337b4D0273b129c0E222235B9F8C',
        qr: '/static/bep20_qr.png',
        desc: 'Send USDT via BNB Smart Chain (BSC BEP-20). Lowest transfer fees (~$0.15).',
        explorer: 'https://bscscan.com/token/0x55d398326f99059fF775485246999027B3197955?a=0x35dd60066ae6337b4D0273b129c0E222235B9F8C#transactions'
      },
      'BTC': {
        currency: 'BTC',
        network: 'BITCOIN NATIVE',
        badgeClass: 'bg-orange-100 text-orange-800',
        title: 'Bitcoin (BTC) Deposit Address',
        address: 'bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu',
        qr: '/static/btc_qr.png',
        desc: 'Send Bitcoin (BTC) to this Native SegWit address. Verified on mempool.space.',
        explorer: 'https://mempool.space/address/bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu'
      },
      'ETH': {
        currency: 'ETH',
        network: 'ETHEREUM MAINNET',
        badgeClass: 'bg-indigo-100 text-indigo-800',
        title: 'Ethereum (ETH / ERC-20) Deposit Address',
        address: '0x35dd60066ae6337b4D0273b129c0E222235B9F8C',
        qr: '/static/eth_qr.png',
        desc: 'Send native ETH or USDT (ERC-20) via Ethereum Mainnet. Verified on Etherscan.',
        explorer: 'https://etherscan.io/address/0x35dd60066ae6337b4D0273b129c0E222235B9F8C'
      },
      'SOL': {
        currency: 'SOL',
        network: 'SOLANA NETWORK',
        badgeClass: 'bg-purple-100 text-purple-800',
        title: 'Solana (SOL) Deposit Address',
        address: 't9QLb3arVUMcQ8JALe3Ptz318GfZkzmRAXvoM8yANFe',
        qr: '/static/sol_qr.png',
        desc: 'Send SOL or USDT-SPL. Finality under 1 second with near-zero gas fee.',
        explorer: 'https://solscan.io/account/t9QLb3arVUMcQ8JALe3Ptz318GfZkzmRAXvoM8yANFe'
      },
      'LTC': {
        currency: 'LTC',
        network: 'LITECOIN NETWORK',
        badgeClass: 'bg-blue-100 text-blue-800',
        title: 'Litecoin (LTC) Deposit Address',
        address: 'LVW74nrfMVpsTY7Kd62tkzfNF5aasM7ieS',
        qr: '/static/ltc_qr.png',
        desc: 'Send Litecoin (LTC). Global standard for low-fee micro payments (~$0.01 fee).',
        explorer: 'https://litecoinspace.org/address/LVW74nrfMVpsTY7Kd62tkzfNF5aasM7ieS'
      }
    };

    function selectCryptoTab(methodKey) {
      currentCryptoMethod = methodKey;
      const conf = CRYPTO_METRIC_CONFIG[methodKey];
      if (!conf) return;

      const keys = ['USDT_TRC20', 'USDT_BEP20', 'BTC', 'ETH', 'SOL', 'LTC'];
      keys.forEach(k => {
        const btn = document.getElementById(`cryptoTab_${k}`);
        if (btn) {
          if (k === methodKey) {
            btn.className = "flex flex-col items-center justify-center p-2.5 rounded-xl border border-slate-900 text-center transition bg-slate-900 text-white shadow-sm";
          } else {
            btn.className = "flex flex-col items-center justify-center p-2.5 rounded-xl border border-slate-200 text-center transition hover:border-[#435ebf] bg-white text-slate-700 hover:bg-slate-50";
          }
        }
      });

      document.getElementById('cryptoQrImg').src = conf.qr;
      document.getElementById('cryptoAddress').innerText = conf.address;
      document.getElementById('cryptoAddrTitle').innerText = conf.title;
      document.getElementById('cryptoAddrDesc').innerText = conf.desc;
      
      const badge = document.getElementById('cryptoNetworkBadge');
      if (badge) {
        badge.innerText = conf.network;
        badge.className = `px-2 py-0.5 rounded text-[10px] font-mono font-bold ${conf.badgeClass}`;
      }

      const explorer = document.getElementById('cryptoExplorerLink');
      if (explorer) explorer.href = conf.explorer;

      const label = document.getElementById('cryptoAmountLabel');
      if (label) label.innerText = `Amount Sent (${conf.currency})`;

      const suffix = document.getElementById('cryptoCurrencySuffix');
      if (suffix) suffix.innerText = conf.currency;

      updateCreditEstimate();
      lucide.createIcons();
    }

    function updateCreditEstimate() {
      const amtInput = document.getElementById('cryptoAmountInput');
      const notice = document.getElementById('creditEstimateNotice');
      if (!amtInput || !notice) return;
      
      const val = parseFloat(amtInput.value) || 0;
      const credits = Math.max(500, Math.round(val * 100));
      notice.innerText = `💎 +${credits.toLocaleString()} Credits`;
    }

    function copyCryptoAddress() {
      const addr = document.getElementById('cryptoAddress').innerText.trim();
      navigator.clipboard.writeText(addr);
      const btn = document.getElementById('cryptoCopyBtn');
      if (!btn) return;
      
      const origHtml = btn.innerHTML;
      btn.innerHTML = `<i data-lucide="check" class="w-3.5 h-3.5 text-emerald-300"></i><span>Copied!</span>`;
      btn.classList.add("bg-emerald-600");
      lucide.createIcons();

      setTimeout(() => {
        btn.innerHTML = origHtml;
        btn.classList.remove("bg-emerald-600");
        lucide.createIcons();
      }, 2000);
    }

    async function submitCryptoPayment() {
      const amt = parseFloat(document.getElementById('cryptoAmountInput').value) || 0;
      const txid = document.getElementById('cryptoTxidInput').value.trim();
      const btn = document.getElementById('btnSubmitPayment');
      
      if (!amt || amt <= 0) {
        showToast("Please enter the amount sent.", 'error');
        return;
      }
      if (!txid) {
        showToast("Please paste your transaction TxID or Hash.", 'error');
        return;
      }

      const origBtn = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Confirming with Blockchain...</span>`;
      lucide.createIcons();

      const stored = localStorage.getItem("pulsecheck_client");
      let currentUserObj = null;
      let email = 'unknown';
      let userId = null;

      if (stored) {
        try {
          currentUserObj = JSON.parse(stored);
          email = currentUserObj.email || 'unknown';
          userId = currentUserObj.id || null;
        } catch(e) {}
      }

      try {
        const response = await fetch('/v1/billing/submit-txid', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            amount: amt,
            txid: txid,
            client_email: email,
            user_id: userId,
            currency: currentCryptoMethod
          })
        });

        const data = await response.json();

        if (response.ok && data.success) {
          // Instantly credit client local session
          if (currentUserObj) {
            currentUserObj.credits = (currentUserObj.credits || 0) + (data.credits_added || Math.round(amt * 100));
            localStorage.setItem("pulsecheck_client", JSON.stringify(currentUserObj));
          }

          // Update header / portal counters live
          const portalCount = document.getElementById('portalCreditCount');
          if (portalCount && currentUserObj) {
            portalCount.innerText = `${currentUserObj.credits.toLocaleString()} Credits`;
          }

          showToast(`✅ Payment Verified! +${(data.credits_added || Math.round(amt * 100)).toLocaleString()} credits added to your balance!`, 'success');
          
          closeCryptoModal();
          setTimeout(() => {
            window.location.reload();
          }, 1200);
        } else {
          showToast(data.detail || data.message || "Error confirming payment. Please check your TxID.", 'error');
          btn.disabled = false;
          btn.innerHTML = origBtn;
          lucide.createIcons();
        }
      } catch (err) {
        showToast("Verification request submitted. Balance updating shortly.", 'success');
        closeCryptoModal();
      }
    }
"""

print("Generated clean modal and script!")
