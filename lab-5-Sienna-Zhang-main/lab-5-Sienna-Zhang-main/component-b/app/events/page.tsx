"use client";

import { useState, useEffect, useCallback } from "react";
import { Event } from "@/lib/supabase";

type Category = "all" | "guest_lecture" | "workshop" | "career_panel" | "other";

const CATEGORY_LABELS: Record<string, string> = {
  all: "All Events",
  guest_lecture: "Guest Lectures",
  workshop: "Workshops",
  career_panel: "Career Panels",
  other: "Other",
};

const CATEGORY_COLORS: Record<string, string> = {
  guest_lecture: "bg-blue-100 text-blue-800",
  workshop: "bg-green-100 text-green-800",
  career_panel: "bg-orange-100 text-orange-800",
  other: "bg-gray-100 text-gray-700",
};

export default function EventsPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [category, setCategory] = useState<Category>("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEvents = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const url =
        category === "all"
          ? "/api/events"
          : `/api/events?category=${category}`;
      const res = await fetch(url);
      if (!res.ok) {
        const json = await res.json().catch(() => ({}));
        throw new Error(json.error ?? `HTTP ${res.status}`);
      }
      const json = await res.json();
      setEvents(json.events ?? []);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load events. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }, [category]);

  useEffect(() => {
    fetchEvents();
  }, [fetchEvents]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">GIX Events</h1>
        <p className="text-sm text-gray-500 mt-1">
          Upcoming events at GIX — filter by category.
        </p>
      </div>

      {/* Category filter */}
      <div className="flex gap-2 flex-wrap">
        {(Object.keys(CATEGORY_LABELS) as Category[]).map((cat) => (
          <button
            key={cat}
            onClick={() => setCategory(cat)}
            className={`text-sm font-medium px-4 py-2 rounded-full transition-colors border ${
              category === cat
                ? "bg-purple-700 text-white border-purple-700"
                : "bg-white text-gray-600 border-gray-300 hover:border-purple-400"
            }`}
          >
            {CATEGORY_LABELS[cat]}
          </button>
        ))}
      </div>

      {/* Error states */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-4 py-4 space-y-2">
          <p className="font-medium">Failed to load events</p>
          <p className="text-xs">{error}</p>
          <button
            onClick={fetchEvents}
            className="text-xs text-red-600 underline"
          >
            Retry
          </button>
        </div>
      )}

      {/* Loading */}
      {loading && !error && (
        <p className="text-gray-400 text-sm">Loading events…</p>
      )}

      {/* Empty state */}
      {!loading && !error && events.length === 0 && (
        <div className="text-center py-16 text-gray-400">
          <p className="text-4xl mb-3">🗓️</p>
          <p className="font-medium">No events found.</p>
          <p className="text-sm mt-1">
            {category === "all"
              ? "No events have been added yet."
              : `No ${CATEGORY_LABELS[category].toLowerCase()} found. Try another filter.`}
          </p>
        </div>
      )}

      {/* Event cards */}
      {!loading && !error && events.length > 0 && (
        <div className="grid sm:grid-cols-2 gap-4">
          {events.map((event) => (
            <div
              key={event.id}
              className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between gap-2 mb-3">
                <span
                  className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                    CATEGORY_COLORS[event.category] ?? "bg-gray-100 text-gray-600"
                  }`}
                >
                  {CATEGORY_LABELS[event.category] ?? event.category}
                </span>
                <span className="text-xs text-gray-400 whitespace-nowrap">
                  {new Date(event.event_date).toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  })}
                </span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm mb-1">
                {event.title}
              </h3>
              {event.description && (
                <p className="text-xs text-gray-500 leading-relaxed mb-2 line-clamp-2">
                  {event.description}
                </p>
              )}
              {event.location && (
                <p className="text-xs text-gray-400 flex items-center gap-1 mt-auto">
                  <span>📍</span> {event.location}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
