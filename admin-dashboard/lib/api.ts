// Live API Client for CheckerLeak Production Backend

export const getApiUrl = (): string => {
  if (typeof window !== "undefined") {
    const saved = localStorage.getItem("checkerleak_api_url");
    if (saved) return saved.replace(/\/$/, "");
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return "http://localhost:8000";
    }
  }
  return process.env.NEXT_PUBLIC_API_URL || "https://checkerleak.com";
};

export const setApiUrl = (url: string) => {
  if (typeof window !== "undefined") {
    localStorage.setItem("checkerleak_api_url", url.trim().replace(/\/$/, ""));
  }
};

export const getAdminKey = (): string => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("checkerleak_admin_key") || "checkerleak_admin_master_2025";
  }
  return "checkerleak_admin_master_2025";
};

export const setAdminKey = (key: string) => {
  if (typeof window !== "undefined") {
    localStorage.setItem("checkerleak_admin_key", key.trim());
  }
};

const authHeaders = () => {
  return {
    "Content-Type": "application/json",
    "X-Admin-Key": getAdminKey(),
    "Authorization": `Bearer ${getAdminKey()}`,
  };
};

export interface LiveStatsResponse {
  revenue: {
    total_usd: number;
    breakdown: Record<string, { amount_usd: number; count: number }>;
    pending_deposits_count: number;
  };
  users: {
    total_count: number;
    new_24h: number;
    circulating_credits: number;
    credit_liability_usd: number;
  };
  verifications: {
    all_time: number;
    today: number;
    engines_active: number;
    engines_total: number;
  };
  system: {
    status: string;
    db_engine: string;
    server_time: string;
  };
}

export interface LiveUser {
  id: number;
  email: string;
  name: string;
  credits: number;
  status: "active" | "banned";
  email_verified: boolean;
  api_key_masked: string;
  api_key_full: string;
  created_at: string;
  total_checks: number;
  total_spent_usd: number;
}

export interface LiveTransaction {
  id: number;
  user_id: number;
  user_email: string;
  plan_id: string;
  amount_usd: number;
  credits_added: number;
  payment_method: string;
  status: "COMPLETED" | "PENDING" | "FAILED";
  tx_hash: string;
  explorer_url?: string;
  created_at: string;
}

export async function fetchLiveStats(): Promise<LiveStatsResponse> {
  const url = `${getApiUrl()}/v1/admin/stats`;
  const res = await fetch(url, {
    method: "GET",
    headers: authHeaders(),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch live stats (${res.status}): ${await res.text()}`);
  }
  return res.json();
}

export async function fetchLiveUsers(search?: string, status?: string): Promise<{ total: number; users: LiveUser[] }> {
  const params = new URLSearchParams();
  if (search) params.append("search", search);
  if (status && status !== "all") params.append("status", status);
  params.append("limit", "100");

  const url = `${getApiUrl()}/v1/admin/users?${params.toString()}`;
  const res = await fetch(url, {
    method: "GET",
    headers: authHeaders(),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch live users (${res.status})`);
  }
  return res.json();
}

export async function fetchLiveTransactions(status?: string): Promise<{ transactions: LiveTransaction[] }> {
  const params = new URLSearchParams();
  if (status && status !== "ALL") params.append("status", status);
  params.append("limit", "100");

  const url = `${getApiUrl()}/v1/admin/transactions?${params.toString()}`;
  const res = await fetch(url, {
    method: "GET",
    headers: authHeaders(),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch transactions (${res.status})`);
  }
  return res.json();
}

export async function adjustUserCreditsLive(userId: number, delta: number, reason: string) {
  const url = `${getApiUrl()}/v1/admin/users/${userId}/adjust-credits`;
  const res = await fetch(url, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ delta_credits: delta, reason }),
  });
  if (!res.ok) {
    throw new Error(`Credit adjustment failed (${res.status})`);
  }
  return res.json();
}

export async function toggleUserStatusLive(userId: number, newStatus: "active" | "banned") {
  const url = `${getApiUrl()}/v1/admin/users/${userId}/toggle-status`;
  const res = await fetch(url, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ status: newStatus }),
  });
  if (!res.ok) {
    throw new Error(`Toggle status failed (${res.status})`);
  }
  return res.json();
}

export async function overrideTransactionLive(txId: number) {
  const url = `${getApiUrl()}/v1/admin/transactions/${txId}/override-confirm`;
  const res = await fetch(url, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ admin_note: "Manual confirm approved via Next.js Admin Cockpit" }),
  });
  if (!res.ok) {
    throw new Error(`Manual override failed (${res.status})`);
  }
  return res.json();
}

export async function overrideUserEmailVerifiedLive(userId: number, verified: boolean) {
  const url = `${getApiUrl()}/v1/admin/users/${userId}/verify-email`;
  const res = await fetch(url, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ verified }),
  });
  if (!res.ok) {
    throw new Error(`Failed to update email verification status (${res.status})`);
  }
  return res.json();
}
