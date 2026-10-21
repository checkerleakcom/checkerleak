"use client";

import React, { useState, useMemo } from "react";
import { Search, ArrowUpDown, ArrowUp, ArrowDown, ShieldCheck, ShieldAlert, CheckCircle2 } from "lucide-react";

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
    <section className="mb-6">
      <div className="rounded-xl bg-[#0d111a] border border-white/[0.08] overflow-hidden">
        {/* Table Control Header */}
        <div className="p-4 sm:p-5 border-b border-white/[0.06] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-semibold text-white tracking-tight flex items-center gap-2">
              <span>Telemetry Verification Ledger</span>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/[0.06] text-slate-300 border border-white/[0.08]">
                {filteredData.length} records matching
              </span>
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Real-time audit log of international carrier queries, VoIP fraud flags, and caller deductions
            </p>
          </div>

          {/* Search + Filter Controls */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search phone, caller, carrier..."
                className="pl-8 pr-3 py-1.5 bg-[#07090e] border border-white/[0.08] focus:border-cyan-400 rounded-lg text-xs font-mono text-slate-200 placeholder-slate-500 outline-none transition w-56 sm:w-64"
              />
            </div>

            {/* Filter Tabs */}
            <div className="flex items-center bg-[#07090e] p-0.5 rounded-lg border border-white/[0.06] text-xs font-mono">
              {(["all", "mobile", "voip"] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => setFilterType(t)}
                  className={`px-2.5 py-1 rounded transition-colors uppercase ${
                    filterType === t
                      ? "bg-white/[0.12] text-white font-semibold"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Scrollable Data Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <caption className="sr-only">Live verification and carrier lookup audit ledger</caption>
            <thead>
              <tr className="border-b border-white/[0.06] bg-[#07090e]/60 font-mono text-[11px] text-slate-400 uppercase tracking-wider">
                <th scope="col" className="py-3 px-4">
                  <button onClick={() => handleSort("phone")} className="flex items-center gap-1 hover:text-white transition">
                    <span>Target Phone</span>
                    {sortKey === "phone" ? (
                      sortOrder === "asc" ? <ArrowUp className="w-3 h-3 text-cyan-400" /> : <ArrowDown className="w-3 h-3 text-cyan-400" />
                    ) : (
                      <ArrowUpDown className="w-3 h-3 opacity-40" />
                    )}
                  </button>
                </th>
                <th scope="col" className="py-3 px-4">Carrier / MNO</th>
                <th scope="col" className="py-3 px-4">Account / Caller</th>
                <th scope="col" className="py-3 px-4">Line Type</th>
                <th scope="col" className="py-3 px-4">
                  <button onClick={() => handleSort("latency")} className="flex items-center gap-1 hover:text-white transition">
                    <span>Latency</span>
                    {sortKey === "latency" ? (
                      sortOrder === "asc" ? <ArrowUp className="w-3 h-3 text-cyan-400" /> : <ArrowDown className="w-3 h-3 text-cyan-400" />
                    ) : (
                      <ArrowUpDown className="w-3 h-3 opacity-40" />
                    )}
                  </button>
                </th>
                <th scope="col" className="py-3 px-4">Status</th>
                <th scope="col" className="py-3 px-4 text-right">
                  <button onClick={() => handleSort("timestamp")} className="inline-flex items-center gap-1 hover:text-white transition ml-auto">
                    <span>Timestamp</span>
                    {sortKey === "timestamp" ? (
                      sortOrder === "asc" ? <ArrowUp className="w-3 h-3 text-cyan-400" /> : <ArrowDown className="w-3 h-3 text-cyan-400" />
                    ) : (
                      <ArrowUpDown className="w-3 h-3 opacity-40" />
                    )}
                  </button>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.04] font-mono text-slate-300">
              {filteredData.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-slate-500 font-mono">
                    No matching records found for query "{search}".
                  </td>
                </tr>
              ) : (
                filteredData.map((row) => (
                  <tr key={row.id} className="hover:bg-white/[0.02] transition-colors">
                    {/* Phone Number */}
                    <td className="py-3 px-4 font-semibold text-white whitespace-nowrap">
                      <span className="flex items-center gap-1.5">
                        <span className="text-[10px] px-1 py-0.2 rounded bg-white/[0.06] text-slate-400">
                          {row.country}
                        </span>
                        <span>{row.phone}</span>
                      </span>
                    </td>

                    {/* Carrier */}
                    <td className="py-3 px-4 text-slate-200 whitespace-nowrap">
                      {row.carrier}
                    </td>

                    {/* User */}
                    <td className="py-3 px-4 text-slate-400 whitespace-nowrap">
                      {row.user}
                    </td>

                    {/* Line Type */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      {row.lineType === "voip" ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[10px]">
                          VOIP BURNER
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px]">
                          PHYSICAL SIM
                        </span>
                      )}
                    </td>

                    {/* Latency */}
                    <td className="py-3 px-4 tabular-nums text-slate-300 whitespace-nowrap">
                      <span className="flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                        {row.latency} ms
                      </span>
                    </td>

                    {/* Status */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      {row.status === "verified" ? (
                        <span className="inline-flex items-center gap-1 text-emerald-400 text-[11px]">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                          VERIFIED
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-rose-400 text-[11px]">
                          <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
                          FLAGGED
                        </span>
                      )}
                    </td>

                    {/* Timestamp */}
                    <td className="py-3 px-4 text-right text-slate-500 tabular-nums whitespace-nowrap text-[11px]">
                      {row.timestamp}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Table Footer info */}
        <div className="p-3 border-t border-white/[0.04] bg-[#07090e]/40 flex items-center justify-between text-[11px] font-mono text-slate-500">
          <span>Showing {filteredData.length} of {INITIAL_DATA.length} cached telemetry events</span>
          <span className="text-slate-400">PAGE 1 OF 1 · AUDIT STREAM VERIFIED</span>
        </div>
      </div>
    </section>
  );
}
