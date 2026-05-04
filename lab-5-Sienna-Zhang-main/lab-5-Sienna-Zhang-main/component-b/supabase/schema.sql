-- Component B: Return Items Assistant
-- Run this SQL in the Supabase SQL Editor to create all tables.
-- RLS is disabled for this lab (no auth required).

-- 1. Return sessions (one per return event)
create table if not exists return_sessions (
  id uuid primary key default gen_random_uuid(),
  event_name text not null,
  staff_name text not null,
  created_at timestamptz not null default now()
);

alter table return_sessions disable row level security;

-- 2. Return items (many per session)
create table if not exists return_items (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references return_sessions(id) on delete cascade,
  team_name text not null,
  raw_name text not null,
  clean_name text not null default '',
  asset_tag text not null default '',
  category text not null check (category in ('IT', 'Makerspace', 'Discard')),
  status text not null default 'pending' check (status in ('pending', 'returned', 'missing')),
  created_at timestamptz not null default now()
);

alter table return_items disable row level security;

-- 3. Events (Component E)
create table if not exists events (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text not null default '',
  category text not null check (category in ('guest_lecture', 'workshop', 'career_panel', 'other')),
  event_date date not null,
  location text not null default '',
  created_at timestamptz not null default now()
);

alter table events disable row level security;

-- Seed a few sample events for Component E demo
insert into events (title, description, category, event_date, location) values
  ('AI in Product Design', 'A guest lecture exploring how AI tools are reshaping product workflows.', 'guest_lecture', '2026-05-15', 'GIX Studio'),
  ('Prototyping Workshop', 'Hands-on session with laser cutters and 3D printers.', 'workshop', '2026-05-20', 'Makerspace'),
  ('Career Panel: Tech & Design', 'Industry professionals share career insights and advice.', 'career_panel', '2026-05-28', 'Main Hall'),
  ('UX Research Methods', 'Deep dive into user research techniques used at top tech companies.', 'workshop', '2026-06-03', 'GIX Lab B'),
  ('Entrepreneurship Talk', 'Founder stories and lessons learned from building startups.', 'guest_lecture', '2026-06-10', 'GIX Auditorium')
on conflict do nothing;
