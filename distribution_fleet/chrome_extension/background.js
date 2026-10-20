// Background Service Worker for CheckerLeak Chrome Extension

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "checkerleak-check-selection",
    title: "Verify '%s' with CheckerLeak",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "checkerleak-check-selection" && info.selectionText) {
    const rawNumber = info.selectionText.trim();
    
    // Retrieve API key from storage
    const data = await chrome.storage.sync.get(["checkerleak_api_key"]);
    const apiKey = data.checkerleak_api_key;

    if (!apiKey) {
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icons/icon128.png",
        title: "CheckerLeak API Key Required",
        message: "Please click the CheckerLeak extension icon and enter your API key from checkerleak.com."
      });
      return;
    }

    try {
      const resp = await fetch("https://checkerleak.com/v1/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": apiKey
        },
        body: JSON.stringify({ phone: rawNumber, type: "full" })
      });

      if (resp.status === 401) {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icons/icon128.png",
          title: "CheckerLeak: 401 Unauthorized",
          message: "Your API key is invalid or expired. Check checkerleak.com/dashboard"
        });
        return;
      } else if (resp.status === 402) {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icons/icon128.png",
          title: "CheckerLeak: 402 Insufficient Balance",
          message: "Please top up credits at checkerleak.com"
        });
        return;
      }

      const resJson = await resp.json();
      const carrier = resJson.carrier_name || (resJson.carrier && resJson.carrier.name) || "Unknown Carrier";
      const isVoip = resJson.is_voip ? "⚠️ VoIP / Burner" : "✅ Real Mobile SIM";
      const country = resJson.country_code || "";

      chrome.notifications.create({
        type: "basic",
        iconUrl: "icons/icon128.png",
        title: `${rawNumber} (${country})`,
        message: `Carrier: ${carrier}\nStatus: ${isVoip}\nLine: ${resJson.line_type || "mobile"}`
      });
    } catch (err) {
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icons/icon128.png",
        title: "CheckerLeak Lookup Failed",
        message: "Network error connecting to CheckerLeak API."
      });
    }
  }
});
