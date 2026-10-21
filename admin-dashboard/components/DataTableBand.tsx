"use client";

import React, { useState, useMemo } from "react";
import { Search, ArrowUpDown, ArrowUp, ArrowDown, CheckCircle2, ShieldAlert, Plus, Ban, ExternalLink, RefreshCw } from "lucide-react";
import { LiveUser, LiveTransaction } from "@/lib/api";

interface DataTableBandProps {
  users: LiveUser[];
  transactions: LiveTransaction[];
  isLoading: boolean;
  onAdjustCredits: (userId: number, delta: number, reason: string) => Promise<void>;
  onToggleStatus: (userId: number, newStatus: "active" | "banned") => Promise<void>;
  onOverrideTx: (txId: number) => Promise<void>;
  onRefresh: () => void;
}

export function DataTableBand({
  users,
  transactions,
  isLoading,
  onAdjustCredits,
  onToggleStatus,
  onOverrideTx,
  onRefresh,
}: DataTableBandProps) {
  const [activeView, setActiveView] = useState<"users" | "transactions">("users");
  const [search, setSearch] = useState("");
  const [userStatusFilter, setUserStatusFilter] = useState<"all" | "active" | "banned">("all");
  const [txStatusFilter, setTxStatusFilter] = useState<"ALL" | "COMPLETED" | "PENDING">("ALL");

  // Sorting
  const [sortField, setSortField] = useState<string>("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Adjust Credits Modal
  const [modalUser, setModalUser] = useState<LiveUser | null>(null);
  const [deltaCredits, setDeltaCredits] = useState<number>(1000);
  const [adjustReason, setAdjustReason] = useState<string>("Manual admin compensation / topup");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("desc");
    }
  };

  // Filtered Users
  const filteredUsers = useMemo(() => {
    return users.filter((u) => {
      const matchSearch =
        u.email.toLowerCase().includes(search.toLowerCase()) ||
        (u.name && u.name.toLowerCase().includes(search.toLowerCase())) ||
        (u.api_key_masked && u.api_key_masked.toLowerCase().includes(search.toLowerCase()));

      const matchStatus = userStatusFilter === "all" ? true : u.status === userStatusFilter;
      return matchSearch && matchStatus;
    }).sort((a, b) => {
      let cmp = 0;
      if (sortField === "id") cmp = a.id - b.id;
      if (sortField === "credits") cmp = a.credits - b.credits;
      if (sortField === "total_checks") cmp = a.total_checks - b.total_checks;
      if (sortField === "email") cmp = a.email.localeCompare(b.email);
      return sortOrder === "asc" ? cmp : -cmp;
    });
  }, [users, search, userStatusFilter, sortField, sortOrder]);

  // Filtered Transactions
  const filteredTxs = useMemo(() => {
    return transactions.filter((tx) => {
      const matchSearch =
        (tx.user_email && tx.user_email.toLowerCase().includes(search.toLowerCase())) ||
        (tx.tx_hash && tx.tx_hash.toLowerCase().includes(search.toLowerCase())) ||
        (tx.payment_method && tx.payment_method.toLowerCase().includes(search.toLowerCase()));

      const matchStatus = txStatusFilter === "ALL" ? true : tx.status === txStatusFilter;
      return matchSearch && matchStatus;
    }).sort((a, b) => {
      let cmp = 0;
      if (sortField === "id") cmp = a.id - b.id;
      if (sortField === "amount") cmp = a.amount_usd - b.amount_usd;
      if (sortField === "date") cmp = a.created_at.localeCompare(b.created_at);
      return sortOrder === "asc" ? cmp : -cmp;
    });
  }, [transactions, search, txStatusFilter, sortField, sortOrder]);

  const submitAdjustCredits = async () => {
    if (!modalUser) return;
    setIsSubmitting(true);
    try {
      await onAdjustCredits(modalUser.id, deltaCredits, adjustReason);
      setModalUser(null);
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="mb-10">
      <div className="rounded-2xl bg-[#0d111a] border border-white/[0.07] overflow-hidden">
        {/* Table Top Controls */}
        <div className="p-6 sm:p-8 border-b border-white/[0.06] flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              {/* Tab Selector: Users vs Transactions */}
              <button
                onClick={() => { setActiveView("users"); setSearch(""); }}
                className={`text-base font-semibold tracking-tight transition-colors ${
                  activeView === "users" ? "text-white border-b-2 border-cyan-400 pb-1" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                Registered Users Directory ({users.length})
              </button>
              <span className="text-slate-600">|</span>
              <button
                onClick={() => { setActiveView("transactions"); setSearch(""); }}
                className={`text-base font-semibold tracking-tight transition-colors ${
                  activeView === "transactions" ? "text-white border-b-2 border-cyan-400 pb-1" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                Crypto Payment Radar ({transactions.length})
              </button>
            </div>
            <p className="text-xs text-slate-400 mt-1.5">
              {activeView === "users"
                ? "Live user accounts, credit balances, 1-click adjustments, and ban management"
                : "Real-time ledger of on-chain Bitcoin/USDT deposits with transaction hashes & 1-click manual override"}
            </p>
          </div>

          {/* Search + Filter */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={activeView === "users" ? "Search email, name, API key..." : "Search email, TX hash, coin..."}
                className="pl-9 pr-4 py-2 bg-[#07090e] border border-white/[0.08] focus:border-cyan-400 rounded-xl text-xs font-mono text-slate-200 placeholder-slate-500 outline-none transition w-64 sm:w-72"
              />
            </div>

            {/* Filter Pills for Users */}
            {activeView === "users" ? (
              <div className="flex items-center bg-[#07090e] p-1 rounded-xl border border-white/[0.06] text-xs font-mono">
                {(["all", "active", "banned"] as const).map((s) => (
                  <button
                    key={s}
                    onClick={() => setUserStatusFilter(s)}
                    className={`px-3 py-1 rounded-lg transition-all uppercase ${
                      userStatusFilter === s
                        ? "bg-white/[0.12] text-white font-semibold shadow-xs"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            ) : (
              <div className="flex items-center bg-[#07090e] p-1 rounded-xl border border-white/[0.06] text-xs font-mono">
                {(["ALL", "COMPLETED", "PENDING"] as const).map((s) => (
                  <button
                    key={s}
                    onClick={() => setTxStatusFilter(s)}
                    className={`px-3 py-1 rounded-lg transition-all uppercase ${
                      txStatusFilter === s
                        ? "bg-white/[0.12] text-white font-semibold shadow-xs"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}

            <button
              onClick={onRefresh}
              className="p-2 rounded-xl bg-[#07090e] border border-white/[0.08] hover:bg-white/[0.04] text-slate-300 transition"
              title="Refresh ledger"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin text-cyan-400" : ""}`} />
            </button>
          </div>
        </div>

        {/* ================= VIEW 1: USERS TABLE ================= */}
        {activeView === "users" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-white/[0.06] bg-[#07090e]/40 font-mono text-xs text-slate-400 uppercase tracking-wider">
                  <th scope="col" className="py-4 px-6">
                    <button onClick={() => handleSort("id")} className="flex items-center gap-1.5 hover:text-white transition">
                      <span>ID & Account Email</span>
                      <ArrowUpDown className="w-3.5 h-3.5 opacity-30" />
                    </button>
                  </th>
                  <th scope="col" className="py-4 px-6">
                    <button onClick={() => handleSort("credits")} className="flex items-center gap-1.5 hover:text-white transition">
                      <span>Balance</span>
                      <ArrowUpDown className="w-3.5 h-3.5 opacity-30" />
                    </button>
                  </th>
                  <th scope="col" className="py-4 px-6">
                    <button onClick={() => handleSort("total_checks")} className="flex items-center gap-1.5 hover:text-white transition">
                      <span>Total Checks</span>
                      <ArrowUpDown className="w-3.5 h-3.5 opacity-30" />
                    </button>
                  </th>
                  <th scope="col" className="py-4 px-6">API Key</th>
                  <th scope="col" className="py-4 px-6">Status</th>
                  <th scope="col" className="py-4 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/[0.03] font-mono text-slate-300">
                {isLoading ? (
                  <tr>
                    <td colSpan={6} className="py-12 text-center text-slate-500 font-mono text-sm animate-pulse">
                      Syncing live user accounts from database...
                    </td>
                  </tr>
                ) : filteredUsers.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-12 text-center text-slate-500 font-mono text-sm">
                      {search ? `No accounts matching "${search}".` : "No registered accounts yet. Database clean and waiting for live signups."}
                    </td>
                  </tr>
                ) : (
                  filteredUsers.map((u) => (
                    <tr key={u.id} className="hover:bg-white/[0.02] transition-colors">
                      {/* ID & Email */}
                      <td className="py-4 px-6 whitespace-nowrap">
                        <div className="flex items-center gap-2.5">
                          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-white/[0.08] text-slate-300">
                            #{u.id}
                          </span>
                          <div>
                            <span className="text-sm font-semibold text-white block">{u.email}</span>
                            <span className="text-[11px] text-slate-500">{u.name || "Enterprise Lead"} · Joined {u.created_at?.split("T")[0] || u.created_at?.split(" ")[0]}</span>
                          </div>
                        </div>
                      </td>

                      {/* Balance */}
                      <td className="py-4 px-6 whitespace-nowrap">
                        <span className="text-sm font-bold text-white tabular-nums">
                          {u.credits.toLocaleString()}
                        </span>
                        <span className="text-[11px] text-slate-500 block">
                          ${(u.credits * 0.00009).toFixed(2)} USD value
                        </span>
                      </td>

                      {/* Checks */}
                      <td className="py-4 px-6 whitespace-nowrap tabular-nums text-slate-300">
                        {u.total_checks.toLocaleString()} checks run
                      </td>

                      {/* API Key */}
                      <td className="py-4 px-6 whitespace-nowrap text-slate-400">
                        <span className="px-2 py-1 rounded bg-[#07090e] border border-white/[0.06] text-[11px]">
                          {u.api_key_masked || "No active key"}
                        </span>
                      </td>

                      {/* Status */}
                      <td className="py-4 px-6 whitespace-nowrap">
                        {u.status === "active" ? (
                          <span className="inline-flex items-center gap-1.5 text-emerald-400 text-xs">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                            Active
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5 text-rose-400 text-xs">
                            <Ban className="w-3.5 h-3.5 text-rose-400" />
                            Banned
                          </span>
                        )}
                      </td>

                      {/* Actions */}
                      <td className="py-4 px-6 text-right whitespace-nowrap">
                        <div className="inline-flex items-center gap-2">
                          <button
                            onClick={() => setModalUser(u)}
                            className="px-2.5 py-1 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/20 text-xs font-mono transition flex items-center gap-1"
                          >
                            <Plus className="w-3 h-3" />
                            Credits
                          </button>
                          <button
                            onClick={() => onToggleStatus(u.id, u.status === "active" ? "banned" : "active")}
                            className={`px-2.5 py-1 rounded-lg text-xs font-mono border transition ${
                              u.status === "active"
                                ? "bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border-rose-500/20"
                                : "bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border-emerald-500/20"
                            }`}
                          >
                            {u.status === "active" ? "Ban" : "Unban"}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}

        {/* ================= VIEW 2: TRANSACTIONS TABLE ================= */}
        {activeView === "transactions" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-white/[0.06] bg-[#07090e]/40 font-mono text-xs text-slate-400 uppercase tracking-wider">
                  <th scope="col" className="py-4 px-6">ID & User</th>
                  <th scope="col" className="py-4 px-6">Plan / Method</th>
                  <th scope="col" className="py-4 px-6">Amount ($)</th>
                  <th scope="col" className="py-4 px-6">Credits Added</th>
                  <th scope="col" className="py-4 px-6">TX Hash / Explorer</th>
                  <th scope="col" className="py-4 px-6">Status</th>
                  <th scope="col" className="py-4 px-6 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/[0.03] font-mono text-slate-300">
                {isLoading ? (
                  <tr>
                    <td colSpan={7} className="py-12 text-center text-slate-500 font-mono text-sm animate-pulse">
                      Loading crypto deposits ledger...
                    </td>
                  </tr>
                ) : filteredTxs.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-12 text-center text-slate-500 font-mono text-sm">
                      {search ? `No transactions matching "${search}".` : "No crypto deposits yet. Live blockchain radar listening on mempool."}
                    </td>
                  </tr>
                ) : (
                  filteredTxs.map((tx) => (
                    <tr key={tx.id} className="hover:bg-white/[0.02] transition-colors">
                      {/* ID & User */}
                      <td className="py-4 px-6 whitespace-nowrap">
                        <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-white/[0.08] text-slate-300 mr-2">
                          #{tx.id}
                        </span>
                        <span className="text-white font-semibold">{tx.user_email || `User #${tx.user_id}`}</span>
                      </td>

                      {/* Method */}
                      <td className="py-4 px-6 whitespace-nowrap">
                        <span className="text-slate-200 font-semibold">{tx.payment_method}</span>
                        <span className="text-[11px] text-slate-500 block uppercase">{tx.plan_id}</span>
                      </td>

                      {/* Amount */}
                      <td className="py-4 px-6 whitespace-nowrap text-sm font-bold text-white tabular-nums">
                        ${tx.amount_usd.toFixed(2)}
                      </td>

                      {/* Credits */}
                      <td className="py-4 px-6 whitespace-nowrap text-cyan-400 font-semibold tabular-nums">
                        +{tx.credits_added.toLocaleString()}
                      </td>

                      {/* TX Hash */}
                      <td className="py-4 px-6 whitespace-nowrap">
                        {tx.tx_hash ? (
                          <div className="flex items-center gap-1.5">
                            <span className="text-[11px] text-slate-400 font-mono">
                              {tx.tx_hash.slice(0, 8)}...{tx.tx_hash.slice(-6)}
                            </span>
                            {tx.explorer_url && (
                              <a
                                href={tx.explorer_url}
                                target="_blank"
                                rel="noreferrer"
                                className="text-cyan-400 hover:text-cyan-300"
                                title="View on Block Explorer"
                              >
                                <ExternalLink className="w-3 h-3" />
                              </a>
                            )}
                          </div>
                        ) : (
                          <span className="text-slate-600">Off-chain / Direct</span>
                        )}
                      </td>

                      {/* Status */}
                      <td className="py-4 px-6 whitespace-nowrap">
                        {tx.status === "COMPLETED" ? (
                          <span className="inline-flex items-center gap-1 text-emerald-400 text-xs">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                            Completed
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-amber-400 text-xs">
                            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
                            Pending
                          </span>
                        )}
                      </td>

                      {/* Override */}
                      <td className="py-4 px-6 text-right whitespace-nowrap">
                        {tx.status === "PENDING" ? (
                          <button
                            onClick={() => onOverrideTx(tx.id)}
                            className="px-2.5 py-1 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 text-xs font-mono transition"
                          >
                            Confirm Deposit
                          </button>
                        ) : (
                          <span className="text-slate-600 text-xs">Settled</span>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}

        {/* Footer info */}
        <div className="p-4 sm:p-5 border-t border-white/[0.04] bg-[#07090e]/30 flex items-center justify-between text-xs font-mono text-slate-500">
          <span>
            {activeView === "users" ? `${filteredUsers.length} total users in database` : `${filteredTxs.length} billing transactions`}
          </span>
          <span className="text-slate-400">Database Connection Active</span>
        </div>
      </div>

      {/* ================= ADJUST CREDITS MODAL ================= */}
      {modalUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4">
          <div className="rounded-2xl bg-[#0d111a] border border-cyan-500/30 p-6 max-w-md w-full shadow-2xl">
            <h4 className="text-base font-semibold text-white mb-1">
              Adjust Credits for {modalUser.email}
            </h4>
            <p className="text-xs text-slate-400 mb-4">
              Current balance: <strong className="text-white">{modalUser.credits.toLocaleString()}</strong> credits
            </p>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Credits Delta (+ / -)</label>
                <input
                  type="number"
                  value={deltaCredits}
                  onChange={(e) => setDeltaCredits(parseInt(e.target.value) || 0)}
                  className="w-full px-3 py-2 bg-[#07090e] border border-white/[0.1] rounded-xl text-white font-mono text-sm focus:border-cyan-400 outline-none"
                  placeholder="+5000 or -1000"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Audit Log Reason</label>
                <input
                  type="text"
                  value={adjustReason}
                  onChange={(e) => setAdjustReason(e.target.value)}
                  className="w-full px-3 py-2 bg-[#07090e] border border-white/[0.1] rounded-xl text-white font-mono text-xs focus:border-cyan-400 outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 mt-6">
              <button
                onClick={() => setModalUser(null)}
                disabled={isSubmitting}
                className="px-4 py-2 rounded-xl text-xs font-mono text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={submitAdjustCredits}
                disabled={isSubmitting}
                className="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-semibold text-xs font-mono transition"
              >
                {isSubmitting ? "Updating..." : "Save Adjustment"}
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
