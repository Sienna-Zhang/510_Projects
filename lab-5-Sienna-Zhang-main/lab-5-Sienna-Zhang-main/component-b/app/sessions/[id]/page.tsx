"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ReturnItem, ReturnSession } from "@/lib/supabase";

type Category = "IT" | "Makerspace" | "Discard";
type Status = "pending" | "returned" | "missing";

const STATUS_COLORS: Record<Status, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  returned: "bg-green-100 text-green-800",
  missing: "bg-red-100 text-red-800",
};

const CATEGORY_OPTIONS: Category[] = ["IT", "Makerspace", "Discard"];

export default function SessionPage() {
  const { id: sessionId } = useParams<{ id: string }>();

  const [session, setSession] = useState<ReturnSession | null>(null);
  const [items, setItems] = useState<ReturnItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [teamName, setTeamName] = useState("");
  const [rawName, setRawName] = useState("");
  const [assetTag, setAssetTag] = useState("");
  const [category, setCategory] = useState<Category>("IT");
  const [cleanName, setCleanName] = useState("");

  const [normalizing, setNormalizing] = useState(false);
  const [saving, setSaving] = useState(false);

  const fetchItems = useCallback(async () => {
    try {
      const res = await fetch(`/api/returns?session_id=${sessionId}`);
      if (!res.ok) throw new Error("Failed to load items");
      const json = await res.json();
      setItems(json.items ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  }, [sessionId]);

  useEffect(() => {
    const init = async () => {
      setLoading(true);
      try {
        // Load session metadata
        const sessRes = await fetch("/api/sessions");
        if (!sessRes.ok) throw new Error("Failed to load session");
        const sessJson = await sessRes.json();
        const found = (sessJson.sessions as ReturnSession[]).find(
          (s) => s.id === sessionId
        );
        if (!found) throw new Error("Session not found");
        setSession(found);
        await fetchItems();
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [sessionId, fetchItems]);

  const handleNormalize = async () => {
    if (!rawName.trim()) return;
    setNormalizing(true);
    setError(null);
    try {
      const res = await fetch("/api/normalize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ raw_name: rawName }),
      });
      if (!res.ok) throw new Error("AI normalization failed");
      const json = await res.json();
      setCleanName(json.clean_name);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setNormalizing(false);
    }
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teamName.trim() || !rawName.trim()) return;
    setSaving(true);
    setError(null);
    try {
      const res = await fetch("/api/returns", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          team_name: teamName,
          raw_name: rawName,
          clean_name: cleanName || rawName,
          asset_tag: assetTag,
          category,
        }),
      });
      if (!res.ok) throw new Error("Failed to add item");
      setRawName("");
      setCleanName("");
      setAssetTag("");
      await fetchItems();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setSaving(false);
    }
  };

  const handleStatusChange = async (itemId: string, newStatus: Status) => {
    try {
      const res = await fetch("/api/returns", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: itemId, status: newStatus }),
      });
      if (!res.ok) throw new Error("Failed to update status");
      setItems((prev) =>
        prev.map((item) =>
          item.id === itemId ? { ...item, status: newStatus } : item
        )
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  };

  const handleExport = () => {
    window.location.href = `/export/${sessionId}`;
  };

  if (loading) {
    return (
      <p className="text-gray-400 text-sm text-center py-16">Loading…</p>
    );
  }

  const returnedCount = items.filter((i) => i.status === "returned").length;
  const missingCount = items.filter((i) => i.status === "missing").length;
  const pendingCount = items.filter((i) => i.status === "pending").length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-3">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Link href="/" className="text-purple-600 hover:text-purple-800 text-sm">
              ← All Sessions
            </Link>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">
            {session?.event_name ?? "Return Session"}
          </h1>
          <p className="text-sm text-gray-500">
            Staff: {session?.staff_name} ·{" "}
            {session && new Date(session.created_at).toLocaleDateString()}
          </p>
        </div>
        {items.length > 0 && (
          <button
            onClick={handleExport}
            className="bg-green-600 hover:bg-green-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          >
            ↓ Export CSV
          </button>
        )}
      </div>

      {/* Stats bar */}
      {items.length > 0 && (
        <div className="grid grid-cols-3 gap-3 text-center">
          {[
            { label: "Pending", count: pendingCount, color: "bg-yellow-50 border-yellow-200 text-yellow-800" },
            { label: "Returned", count: returnedCount, color: "bg-green-50 border-green-200 text-green-800" },
            { label: "Missing", count: missingCount, color: "bg-red-50 border-red-200 text-red-800" },
          ].map(({ label, count, color }) => (
            <div key={label} className={`rounded-xl border px-3 py-3 ${color}`}>
              <p className="text-2xl font-bold">{count}</p>
              <p className="text-xs font-medium mt-0.5">{label}</p>
            </div>
          ))}
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
          {error}
        </div>
      )}

      {/* Add item form */}
      <form
        onSubmit={handleAdd}
        className="bg-white border border-gray-200 rounded-xl p-5 space-y-4 shadow-sm"
      >
        <h2 className="font-semibold text-gray-800">Add Return Item</h2>

        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Team Name *
            </label>
            <input
              type="text"
              value={teamName}
              onChange={(e) => setTeamName(e.target.value)}
              placeholder="e.g. Team Alpha"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Category *
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value as Category)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white"
            >
              {CATEGORY_OPTIONS.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Raw name + normalize */}
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">
            Raw Product Name (Amazon title) *
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={rawName}
              onChange={(e) => {
                setRawName(e.target.value);
                setCleanName("");
              }}
              placeholder="Paste full Amazon product name here…"
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            <button
              type="button"
              onClick={handleNormalize}
              disabled={normalizing || !rawName.trim()}
              className="shrink-0 bg-purple-100 hover:bg-purple-200 disabled:opacity-40 text-purple-800 text-xs font-medium px-3 py-2 rounded-lg transition-colors whitespace-nowrap"
            >
              {normalizing ? "⏳ AI…" : "✨ Clean"}
            </button>
          </div>
        </div>

        {/* Clean name preview */}
        {cleanName && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg px-4 py-3">
            <p className="text-xs text-purple-600 font-medium mb-1">AI cleaned name:</p>
            <input
              type="text"
              value={cleanName}
              onChange={(e) => setCleanName(e.target.value)}
              className="w-full bg-transparent text-sm text-purple-900 font-medium focus:outline-none"
            />
          </div>
        )}

        {/* Asset tag */}
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">
            Asset Tag (8-digit UW tag)
          </label>
          <input
            type="text"
            value={assetTag}
            onChange={(e) => setAssetTag(e.target.value)}
            placeholder="e.g. 12345678"
            maxLength={10}
            className="w-full sm:w-48 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <button
          type="submit"
          disabled={saving}
          className="bg-purple-700 hover:bg-purple-800 disabled:opacity-50 text-white text-sm font-medium px-5 py-2 rounded-lg transition-colors"
        >
          {saving ? "Saving…" : "+ Add Item"}
        </button>
      </form>

      {/* Items list */}
      {items.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          <p className="text-3xl mb-2">📋</p>
          <p className="text-sm">No items yet. Add the first return item above.</p>
        </div>
      ) : (
        <div className="space-y-2">
          <h2 className="font-semibold text-gray-800 text-sm uppercase tracking-wide">
            Items ({items.length})
          </h2>
          {/* Desktop table */}
          <div className="hidden sm:block bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Name</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Tag</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Category</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Team</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <p className="font-medium text-gray-900">
                        {item.clean_name || item.raw_name}
                      </p>
                      {item.clean_name && item.clean_name !== item.raw_name && (
                        <p className="text-xs text-gray-400 truncate max-w-xs">
                          {item.raw_name}
                        </p>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-600 font-mono text-xs">
                      {item.asset_tag || "—"}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{item.category}</td>
                    <td className="px-4 py-3 text-gray-600">{item.team_name}</td>
                    <td className="px-4 py-3">
                      <select
                        value={item.status}
                        onChange={(e) =>
                          handleStatusChange(item.id, e.target.value as Status)
                        }
                        className={`text-xs font-medium px-2 py-1 rounded-full border-0 cursor-pointer focus:outline-none focus:ring-2 focus:ring-purple-500 ${STATUS_COLORS[item.status]}`}
                      >
                        <option value="pending">Pending</option>
                        <option value="returned">Returned</option>
                        <option value="missing">Missing</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile cards */}
          <div className="sm:hidden space-y-3">
            {items.map((item) => (
              <div
                key={item.id}
                className="bg-white border border-gray-200 rounded-xl px-4 py-3 shadow-sm"
              >
                <p className="font-medium text-gray-900 text-sm">
                  {item.clean_name || item.raw_name}
                </p>
                <div className="flex flex-wrap gap-2 mt-2 text-xs text-gray-500">
                  <span>{item.category}</span>
                  <span>·</span>
                  <span>{item.team_name}</span>
                  {item.asset_tag && (
                    <>
                      <span>·</span>
                      <span className="font-mono">{item.asset_tag}</span>
                    </>
                  )}
                </div>
                <div className="mt-2">
                  <select
                    value={item.status}
                    onChange={(e) =>
                      handleStatusChange(item.id, e.target.value as Status)
                    }
                    className={`text-xs font-medium px-2 py-1 rounded-full cursor-pointer focus:outline-none ${STATUS_COLORS[item.status]}`}
                  >
                    <option value="pending">Pending</option>
                    <option value="returned">Returned</option>
                    <option value="missing">Missing</option>
                  </select>
                </div>
              </div>
            ))}
          </div>

          {/* Export button (bottom) */}
          <div className="flex justify-end pt-2">
            <button
              onClick={handleExport}
              className="bg-green-600 hover:bg-green-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
            >
              ↓ Export CSV for BlueTally
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
