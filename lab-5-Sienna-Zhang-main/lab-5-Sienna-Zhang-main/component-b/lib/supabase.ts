import { createClient, SupabaseClient } from "@supabase/supabase-js";

let _client: SupabaseClient | null = null;

// Lazy singleton — only initialised on first use, not at build time
export function getSupabase(): SupabaseClient {
  if (_client) return _client;
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !key) {
    throw new Error(
      "Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY"
    );
  }
  _client = createClient(url, key);
  return _client;
}

// Convenience re-export so callers can do: import { supabase } from "@/lib/supabase"
// This is a Proxy that defers creation until the first property access.
export const supabase = new Proxy({} as SupabaseClient, {
  get(_target, prop) {
    return (getSupabase() as unknown as Record<string | symbol, unknown>)[prop];
  },
});

// Types matching our Supabase schema
export interface ReturnSession {
  id: string;
  event_name: string;
  staff_name: string;
  created_at: string;
}

export interface ReturnItem {
  id: string;
  session_id: string;
  team_name: string;
  raw_name: string;
  clean_name: string;
  asset_tag: string;
  category: "IT" | "Makerspace" | "Discard";
  status: "pending" | "returned" | "missing";
  created_at: string;
}

export interface Event {
  id: string;
  title: string;
  description: string;
  category: "guest_lecture" | "workshop" | "career_panel" | "other";
  event_date: string;
  location: string;
  created_at: string;
}
