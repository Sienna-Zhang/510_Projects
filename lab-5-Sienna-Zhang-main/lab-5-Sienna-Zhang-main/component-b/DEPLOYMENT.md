# Deployment & Setup Guide

## Live URL

**Production:** https://component-b.vercel.app

---

## Environment Variables

All secrets are stored in Vercel's dashboard (never in git). The `.gitignore`
catches `.env*` so `.env.local` is never committed.

| Variable | Exposure | Purpose |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Client + Server | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Client + Server | Supabase anon (public) key |
| `ANTHROPIC_API_KEY` | **Server only** | Claude AI name cleaning |

`ANTHROPIC_API_KEY` has no `NEXT_PUBLIC_` prefix, so it is **never sent to the
browser**. Verified: running `curl https://component-b.vercel.app | grep "sk-ant"`
returns nothing.

---

## Supabase Table Setup (one-time)

The app requires three tables in your Supabase project. Run `supabase/schema.sql`
in the **Supabase SQL Editor**:

1. Go to https://supabase.com/dashboard/project/kumcpnoskfqmdrpwbhln
2. Open **SQL Editor** in the left sidebar
3. Paste the contents of `supabase/schema.sql` and click **Run**
4. This creates `return_sessions`, `return_items`, and `events` tables, and seeds
   five sample events for Component E.

---

## Running Tests

```bash
# Against local dev server (npm run dev must be running)
npm test

# Against production
$env:API_BASE_URL = "https://component-b.vercel.app"
node --test tests/api.test.mjs
```

Expected results **after** Supabase tables are created:

```
# tests 5
# pass 5
# fail 0
```

The 3 input-validation tests pass regardless of Supabase setup (they are caught
before any DB query). The 2 Supabase-dependent tests require the tables to exist.

---

## Re-deploying

```bash
# Deploy with current code + env vars
vercel --prod --yes
```
