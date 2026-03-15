-- ═══════════════════════════════════════════════════════
-- Portfolio API — Supabase Schema
-- Run this in your Supabase project → SQL Editor
-- ═══════════════════════════════════════════════════════

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- ── Contact Messages ──────────────────────────────────
create table if not exists contact_messages (
  id          uuid primary key default uuid_generate_v4(),
  name        text not null,
  email       text not null,
  subject     text not null,
  message     text not null,
  read        boolean not null default false,
  created_at  timestamptz not null default now()
);

-- ── Project Views ─────────────────────────────────────
create table if not exists project_views (
  project_id  text primary key,
  views       integer not null default 0,
  updated_at  timestamptz not null default now()
);

-- ── Blog Posts ────────────────────────────────────────
create table if not exists blog_posts (
  id          uuid primary key default uuid_generate_v4(),
  title       text not null,
  slug        text not null unique,
  excerpt     text not null,
  content     text not null,
  tags        text[] not null default '{}',
  published   boolean not null default false,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- ── Row Level Security ────────────────────────────────
-- contact_messages: only service role can read, anyone can insert
alter table contact_messages enable row level security;

create policy "Anyone can submit contact" on contact_messages
  for insert with check (true);

create policy "Service role reads messages" on contact_messages
  for select using (auth.role() = 'service_role');

create policy "Service role updates messages" on contact_messages
  for update using (auth.role() = 'service_role');

create policy "Service role deletes messages" on contact_messages
  for delete using (auth.role() = 'service_role');

-- project_views: public read, service role write
alter table project_views enable row level security;

create policy "Anyone can read views" on project_views
  for select using (true);

create policy "Service role writes views" on project_views
  for all using (auth.role() = 'service_role');

-- blog_posts: public can read published only, service role full access
alter table blog_posts enable row level security;

create policy "Anyone reads published posts" on blog_posts
  for select using (published = true);

create policy "Service role full access posts" on blog_posts
  for all using (auth.role() = 'service_role');
