-- Run this in your Supabase SQL editor
-- Project: Redemption Makosa Portfolio

-- ── Contact Messages ──────────────────────────────
CREATE TABLE IF NOT EXISTS contact_messages (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    subject     TEXT NOT NULL,
    message     TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── Project Views ─────────────────────────────────
CREATE TABLE IF NOT EXISTS project_views (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id  TEXT NOT NULL UNIQUE,
    views       INTEGER DEFAULT 0,
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Seed your projects
INSERT INTO project_views (project_id, views) VALUES
    ('campus-key', 0)
ON CONFLICT (project_id) DO NOTHING;

-- ── Blog Posts ────────────────────────────────────
CREATE TABLE IF NOT EXISTS posts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT NOT NULL,
    slug        TEXT NOT NULL UNIQUE,
    excerpt     TEXT NOT NULL,
    content     TEXT NOT NULL,
    published   BOOLEAN DEFAULT FALSE,
    tags        TEXT[] DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── Row Level Security ────────────────────────────
-- contact_messages: only insert from public, read via service key
ALTER TABLE contact_messages ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_insert" ON contact_messages FOR INSERT WITH CHECK (true);
CREATE POLICY "allow_select_service" ON contact_messages FOR SELECT USING (false); -- backend uses service key

-- project_views: public read + update
ALTER TABLE project_views ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_read" ON project_views FOR SELECT USING (true);
CREATE POLICY "allow_update" ON project_views FOR UPDATE USING (true);
CREATE POLICY "allow_insert" ON project_views FOR INSERT WITH CHECK (true);

-- posts: public read published only
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_read_published" ON posts FOR SELECT USING (published = true);
