
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "SoftwareApplication",
        "@id": "https://pulsecheck.ai/#software",
        "name": "PulseCheck",
        "url": "https://pulsecheck.ai",
        "applicationCategory": "BusinessApplication, DeveloperApplication, MarketingApplication",
        "operatingSystem": "Web, Cloud, REST API",
        "description": "Enterprise-grade bulk phone number verification, HLR lookup, carrier intelligence, and multi-channel footprint detection.",
        "offers": [
          {
            "@type": "Offer",
            "name": "Starter Plan",
            "price": "19.00",
            "priceCurrency": "USD",
            "description": "1,000 checks with full 90+ checkers access"
          },
          {
            "@type": "Offer",
            "name": "Pro Plan",
            "price": "49.00",
            "priceCurrency": "USD",
            "description": "5,000 checks with fast concurrency and multi-channel enrichment"
          },
          {
            "@type": "Offer",
            "name": "Enterprise Plan",
            "price": "149.00",
            "priceCurrency": "USD",
            "description": "25,000 checks with dedicated throughput and priority SLA"
          }
        ],
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "4.9",
          "ratingCount": "1482",
          "bestRating": "5",
          "worstRating": "1"
        }
      },
      {
        "@type": "Organization",
        "@id": "https://pulsecheck.ai/#organization",
        "name": "PulseCheck",
        "url": "https://pulsecheck.ai",
        "logo": "https://pulsecheck.ai/static/logo.png",
        "sameAs": [
          "https://twitter.com/PulseCheckAI",
          "https://github.com/pulsecheck-ai"
        ]
      },
      {
        "@type": "FAQPage",
        "@id": "https://pulsecheck.ai/#faq",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "How does PulseCheck verify phone numbers without sending an SMS?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "PulseCheck connects directly to international SS7/Diameter cellular signaling networks (HLR lookup) and native protocol handshakes. This verifies whether a SIM card is active, roaming, or ported to another network in real time without sending an SMS or disturbing the subscriber."
            }
          },
          {
            "@type": "Question",
            "name": "Can PulseCheck detect WhatsApp and Apple iMessage simultaneously?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. Our multi-engine cascading pipeline queries WhatsApp's server directory and Apple's IDS Identity Services to report both WhatsApp account status and Apple Blue-bubble iMessage availability concurrently."
            }
          },
          {
            "@type": "Question",
            "name": "What is an HLR carrier lookup and why is it important?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Home Location Register (HLR) is the central database containing details of each mobile phone subscriber. An HLR lookup returns the authentic Mobile Network Operator (MNO/MVNO), detects recent SIM swap porting, and flags disposable burner VoIP numbers."
            }
          },
          {
            "@type": "Question",
            "name": "Which countries and telecom standards are supported?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "PulseCheck supports over 240 countries and territories complying strictly with ITU-T E.164 and E.123 standards, including North America (+1), Europe (+33, +44, +49, +34), MENA (+212, +971, +966, +20), and Asia-Pacific."
            }
          },
          {
            "@type": "Question",
            "name": "How does the smart cascading cost optimization work?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Instead of executing expensive queries for every contact, PulseCheck runs free local ITU syntax and offline dial-plan checks first. Invalid numbers are dropped immediately, saving marketing teams up to 90% in verification costs."
            }
          }
        ]
      }
    ]
  }
  
    
    }

     else if (curr === 'BTC') {
        if (btcBtn) btcBtn.className = activeClass;
        if (qrImg) qrImg.src = "/static/btc_qr.png";
        if (addrCode) addrCode.innerText = "bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu";
        if (title) title.innerText = "Your Bitcoin (BTC) Address";
        if (desc) desc.innerHTML = 'Native SegWit Bitcoin address.<br>View live on <a href="https://mempool.space/address/bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu" target="_blank" class="underline text-[#435ebf] font-semibold">mempool.space Explorer ↗</a>';
      } else if (curr === 'ETH') {
        if (ethBtn) ethBtn.className = activeClass;
        if (qrImg) qrImg.src = "/static/eth_qr.png";
        if (addrCode) addrCode.innerText = "0x35dd60066ae6337b4D0273b129c0E222235B9F8C";
        if (title) title.innerText = "Your Ethereum (ETH / ERC-20) Address";
        if (desc) desc.innerHTML = 'Send <strong>Ethereum (ETH)</strong> or <strong>USDT (ERC-20)</strong> via Ethereum Mainnet.<br>View live on <a href="https://etherscan.io/address/0x35dd60066ae6337b4D0273b129c0E222235B9F8C" target="_blank" class="underline text-[#435ebf] font-semibold">Etherscan Explorer ↗</a>';
      } else if (curr === 'SOL') {
        if (solBtn) solBtn.className = activeClass;
        if (qrImg) qrImg.src = "/static/sol_qr.png";
        if (addrCode) addrCode.innerText = "t9QLb3arVUMcQ8JALe3Ptz318GfZkzmRAXvoM8yANFe";
        if (title) title.innerText = "Your Solana (SOL / SPL) Address";
        if (desc) desc.innerHTML = 'Send <strong>Solana (SOL)</strong> or <strong>USDT (SPL)</strong>.<br>Instant finality (<1 sec) · Near-zero fees.<br>View live on <a href="https://solscan.io/account/t9QLb3arVUMcQ8JALe3Ptz318GfZkzmRAXvoM8yANFe" target="_blank" class="underline text-[#435ebf] font-semibold">Solscan Explorer ↗</a>';
      } else if (curr === 'LTC') {
        if (ltcBtn) ltcBtn.className = activeClass;
        if (qrImg) qrImg.src = "/static/ltc_qr.png";
        if (addrCode) addrCode.innerText = "LVW74nrfMVpsTY7Kd62tkzfNF5aasM7ieS";
        if (title) title.innerText = "Your Litecoin (LTC) Address";
        if (desc) desc.innerHTML = 'Send <strong>Litecoin (LTC)</strong>.<br>Lowest fee (~$0.01) · Fast confirmation.<br>View live on <a href="https://litecoinspace.org/address/LVW74nrfMVpsTY7Kd62tkzfNF5aasM7ieS" target="_blank" class="underline text-[#435ebf] font-semibold">Litecoin Space Explorer ↗</a>';
      } else {
        if (trcBtn) trcBtn.className = activeClass;
        if (qrImg) qrImg.src = "/static/usdt_qr.png";
        if (addrCode) addrCode.innerText = "TT44hVQek5xLh7qz2FhpBdmbMziyBGyzPX";
        if (title) title.innerText = "Your USDT (TRC-20) Address";
        if (desc) desc.innerHTML = 'Use this address only for USDT on the Tron (TRC-20) network.<br>View live on <a href="https://tronscan.org/address/TT44hVQek5xLh7qz2FhpBdmbMziyBGyzPX/transactions" target="_blank" class="underline text-[#435ebf] font-semibold">TronScan Explorer ↗</a>';
      }
    }


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

