document.addEventListener("DOMContentLoaded", async () => {
  const phoneInput = document.getElementById("phoneInput");
  const keyInput = document.getElementById("keyInput");
  const verifyBtn = document.getElementById("verifyBtn");
  const resultCard = document.getElementById("resultCard");

  // Load saved key
  const saved = await chrome.storage.sync.get(["checkerleak_api_key"]);
  if (saved.checkerleak_api_key) {
    keyInput.value = saved.checkerleak_api_key;
  }

  // Auto-save key when modified
  keyInput.addEventListener("change", () => {
    chrome.storage.sync.set({ checkerleak_api_key: keyInput.value.trim() });
  });

  verifyBtn.addEventListener("click", async () => {
    const phone = phoneInput.value.trim();
    const key = keyInput.value.trim();

    if (!phone) {
      alert("Please enter a target phone number.");
      return;
    }
    if (!key) {
      alert("CheckerLeak API Key required. Sign up at https://checkerleak.com to get your key.");
      return;
    }

    chrome.storage.sync.set({ checkerleak_api_key: key });

    verifyBtn.textContent = "Verifying...";
    verifyBtn.disabled = true;

    try {
      const resp = await fetch("https://checkerleak.com/v1/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": key
        },
        body: JSON.stringify({ phone: phone, type: "full" })
      });

      if (resp.status === 401) {
        alert("401 Unauthorized: Invalid API Key. Manage keys at https://checkerleak.com");
        return;
      } else if (resp.status === 402) {
        alert("402 Payment Required: Credit balance depleted. Top up at https://checkerleak.com");
        return;
      } else if (!resp.ok) {
        alert(`Lookup error (${resp.status}): ${await resp.text()}`);
        return;
      }

      const data = await resp.json();
      resultCard.style.display = "block";

      const carrier = data.carrier_name || (data.carrier && data.carrier.name) || "Unknown";
      document.getElementById("resCarrier").textContent = carrier;
      document.getElementById("resLineType").textContent = (data.line_type || "mobile").toUpperCase();
      
      const isVoip = data.is_voip || data.line_type === "voip";
      document.getElementById("resVoip").textContent = isVoip ? "⚠️ YES (Virtual/Burner)" : "✅ NO (Physical SIM)";
      document.getElementById("resVoip").style.color = isVoip ? "#f87171" : "#4ade80";

      document.getElementById("resCountry").textContent = data.country_code || "Unknown";
      document.getElementById("resLatency").textContent = (data.latency_ms || 120) + " ms";

    } catch (err) {
      alert("Network error connecting to CheckerLeak API: " + err.message);
    } finally {
      verifyBtn.textContent = "🔍 Verify Phone Line";
      verifyBtn.disabled = false;
    }
  });
});
