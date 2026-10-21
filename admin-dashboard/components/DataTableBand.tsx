"use client";

import React, { useState, useMemo } from "react";
import { Search, ArrowUpDown, ArrowUp, ArrowDown, CheckCircle2, ShieldAlert } from "lucide-react";

interface RecordItem {
  id: string;
  phone: string;
  user: string;
  carrier: string;
  country: string;
  lineType: "mobile" | "voip" | "landline";
  latency: number;
  cost: number;
  status: "verified" | "burner_flagged" | "balance_gated";
  timestamp: string;
}

const INITIAL_DATA: RecordItem[] = [
  {
    id: "tx_90124",
    phone: "+1 415 555 2671",
    user: "alex@enterprise-lead.io",
    carrier: "Verizon Wireless",
    country: "US",
    lineType: "mobile",
    latency: 112,
    cost: 0.00009,
    status: "verified",
    timestamp: "2026-10-21 00:44:12",
  },
  {
    id: "tx_90123",
    phone: "+44 7911 123456",
    user: "data-sync@fintech-os.uk",
    carrier: "Vodafone UK",
    country: "GB",
    lineType: "mobile",
    latency: 124,
    cost: 0.00009,
    status: "verified",
    timestamp: "2026-10-21 00:43:55",
  },
  {
    id: "tx_90122",
    phone: "+1 206 555 0192",
    user: "growth@agency-scrapers.com",
    carrier: "Twilio / Bandwidth.com",
    country: "US",
    lineType: "voip",
    latency: 98,
    cost: 0.00009,
    status: "burner_flagged",
    timestamp: "2026-10-21 00:42:10",
  },
  {
    id: "tx_90121",
    phone: "+212 661 123456",
    user: "tarik@maroc-telecoms.ma",
    carrier: "Maroc Telecom (IAM)",
    country: "MA",
    lineType: "mobile",
    latency: 142,
    cost: 0.00009,
    status: "verified",
    timestamp: "2026-10-21 00:41:40",
  },
  {
    id: "tx_90120",
    phone: "+49 151 23456789",
    user: "compliance@berlin-pay.de",
    carrier: "Telekom Deutschland",
    country: "DE",
    lineType: "mobile",
    latency: 118,
    cost: 0.00009,
    status: "verified",
    timestamp: "2026-10-21 00:40:02",
  },
  {
    id: "tx_90119",
    phone: "+1 312 555 7789",
    user: "trial-guest@unknown.net",
    carrier: "Google Voice / Bandwidth",
    country: "US",
    lineType: "voip",
    latency: 89,
    cost: 0.00000,
    status: "burner_flagged",
    timestamp: "2026-10-21 00:39:15",
  },
  {
    id: "tx_90118",
    phone: "+33 6 12 34 56 78",
    user: "sec-ops@paris-identity.fr",
    carrier: "Orange France",
    country: "FR",
    lineType: "mobile",
    latency: 135,
    cost: 0.00009,
    status: "verified",
    timestamp: "2026-10-21 00:38:22",
  },
  {
    id: "tx_90117",
    phone: "+971 50 123 4567",
    user: "dubai-crypto@fund.ae",
    carrier: "Etisalat (e&)",
    country: "AE",
    lineType: "mobile",
    latency: 154,
    cost: 0.00009,
    status: "verified",
    timestamp: "2026-10-21 00:37:11",
  },
];

type SortKey = "timestamp" | "latency" | "phone" | "cost";

export function DataTableBand() {
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState<"all" | "mobile" | "voip">("all");
  const [sortKey, setSortKey] = useState<SortKey>("timestamp");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortOrder("desc");
    }
  };

  const filteredData = useMemo(() => {
    return INITIAL_DATA.filter((row) => {
      const matchSearch =
        row.phone.toLowerCase().includes(search.toLowerCase()) ||
        row.user.toLowerCase().includes(search.toLowerCase()) ||
        row.carrier.toLowerCase().includes(search.toLowerCase()) ||
        row.country.toLowerCase().includes(search.toLowerCase());

      const matchFilter = filterType === "all" ? true : row.lineType === filterType;

      return matchSearch && matchFilter;
    }).sort((a, b) => {
      let cmp = 0;
      if (sortKey === "timestamp") cmp = a.timestamp.localeCompare(b.timestamp);
      if (sortKey === "latency") cmp = a.latency - b.latency;
      if (sortKey === "cost") cmp = a.cost - b.cost;
      if (sortKey === "phone") cmp = a.phone.localeCompare(b.phone);

      return sortOrder === "asc" ? cmp : -cmp;
    });
  }, [search, filterType, sortKey, sortOrder]);

  return (
    <section className="mb-10">
      <div className="rounded-2xl bg-[#0d111a] border border-white/[0.07] overflow-hidden">
        {/* Table Header & Search Bar */}
        <div className="p-6 sm:p-8 border-b border-white/[0.06] flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h3 className="text-base font-semibold text-white tracking-tight flex items-center gap-2.5">
              <span>Live Verification Audit Ledger</span>
              <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-white/[0.06] text-slate-300 border border-white/[0.08]">
                {filteredData.length} active records
              </span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Real-time feed of international carrier queries, VoIP fraud flags, and account deductions
            </p>
          </div>

          {/* Search + Filter Tabs */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search phone, carrier, account..."
                className="pl-9 pr-4 py-2 bg-[#07090e] border border-white/[0.08] focus:border-cyan-400 rounded-xl text-xs font-mono text-slate-200 placeholder-slate-500 outline-none transition w-64 sm:w-72"
              />
            </div>

            {/* Filter Pills */}
            <div className="flex items-center bg-[#07090e] p-1 rounded-xl border border-white/[0.06] text-xs font-mono">
              {(["all", "mobile", "voip"] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => setFilterType(t)}
                  className={`px-3 py-1 rounded-lg transition-all uppercase ${
                    filterType === t
                      ? "bg-white/[0.12] text-white font-semibold shadow-xs"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Spacious Data Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <caption className="sr-only">Live verification and carrier lookup audit ledger</caption>
            <thead>
              <tr className="border-b border-white/[0.06] bg-[#07090e]/40 font-mono text-xs text-slate-400 uppercase tracking-wider">
                <th scope="col" className="py-4 px-6">
                  <button onClick={() => handleSort("phone")} className="flex items-center gap-1.5 hover:text-white transition">
                    <span>Target Phone</span>
                    {sortKey === "phone" ? (
                      sortOrder === "asc" ? <ArrowUp className="w-3.5 h-3.5 text-cyan-400" /> : <ArrowDown className="w-3.5 h-3.5 text-cyan-400" />
                    ) : (
                      <ArrowUpDown className="w-3.5 h-3.5 opacity-30" />
                    )}
                  </button>
                </th>
                <th scope="col" className="py-4 px-6">Carrier / MNO</th>
                <th scope="col" className="py-4 px-6">Caller Account</th>
                <th scope="col" className="py-4 px-6">Line Type</th>
                <th scope="col" className="py-4 px-6">
                  <button onClick={() => handleSort("latency")} className="flex items-center gap-1.5 hover:text-white transition">
                    <span>Latency</span>
                    {sortKey === "latency" ? (
                      sortOrder === "asc" ? <ArrowUp className="w-3.5 h-3.5 text-cyan-400" /> : <ArrowDown className="w-3.5 h-3.5 text-cyan-400" />
                    ) : (
                      <ArrowUpDown className="w-3.5 h-3.5 opacity-30" />
                    )}
                  </button>
                </th>
                <th scope="col" className="py-4 px-6">Status</th>
                <th scope="col" className="py-4 px-6 text-right">
                  <button onClick={() => handleSort("timestamp")} className="inline-flex items-center gap-1.5 hover:text-white transition ml-auto">
                    <span>Timestamp</span>
                    {sortKey === "timestamp" ? (
                      sortOrder === "asc" ? <ArrowUp className="w-3.5 h-3.5 text-cyan-400" /> : <ArrowDown className="w-3.5 h-3.5 text-cyan-400" />
                    ) : (
                      <ArrowUpDown className="w-3.5 h-3.5 opacity-30" />
                    )}
                  </button>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.03] font-mono text-slate-300">
              {filteredData.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500 font-mono text-sm">
                    No matching records found for "{search}".
                  </td>
                </tr>
              ) : (
                filteredData.map((row) => (
                  <tr key={row.id} className="hover:bg-white/[0.02] transition-colors">
                    {/* Phone Number */}
                    <td className="py-4 px-6 font-semibold text-white whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-white/[0.08] text-slate-300">
                          {row.country}
                        </span>
                        <span className="text-sm tracking-tight">{row.phone}</span>
                      </div>
                    </td>

                    {/* Carrier */}
                    <td className="py-4 px-6 text-slate-200 whitespace-nowrap text-xs">
                      {row.carrier}
                    </td>

                    {/* User */}
                    <td className="py-4 px-6 text-slate-400 whitespace-nowrap text-xs">
                      {row.user}
                    </td>

                    {/* Line Type */}
                    <td className="py-4 px-6 whitespace-nowrap">
                      {row.lineType === "voip" ? (
                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[11px] font-medium">
                          VoIP Burner
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[11px] font-medium">
                          Physical SIM
                        </span>
                      )}
                    </td>

                    {/* Latency */}
                    <td className="py-4 px-6 tabular-nums text-slate-300 whitespace-nowrap text-xs">
                      <span className="flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                        {row.latency} ms
                      </span>
                    </td>

                    {/* Status */}
                    <td className="py-4 px-6 whitespace-nowrap">
                      {row.status === "verified" ? (
                        <span className="inline-flex items-center gap-1.5 text-emerald-400 text-xs">
                          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                          Verified
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1.5 text-rose-400 text-xs">
                          <ShieldAlert className="w-4 h-4 text-rose-400" />
                          Burner Flag
                        </span>
                      )}
                    </td>

                    {/* Timestamp */}
                    <td className="py-4 px-6 text-right text-slate-500 tabular-nums whitespace-nowrap text-xs">
                      {row.timestamp}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Table Footer */}
        <div className="p-4 sm:p-5 border-t border-white/[0.04] bg-[#07090e]/30 flex items-center justify-between text-xs font-mono text-slate-500">
          <span>Showing {filteredData.length} of {INITIAL_DATA.length} telemetry transactions</span>
          <span className="text-slate-400">Page 1 of 1 · Audit Stream Verified</span>
        </div>
      </div>
    </section>
  );
}
