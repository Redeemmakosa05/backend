# Portfolio Backend — Setup Guide

## Stack
- **API**: Python + FastAPI (serverless on Vercel)
- **DB**: Supabase (PostgreSQL, free tier)
- **Email**: Resend (free tier — 100 emails/day)
- **Auth**: JWT (admin only)

---

## Step 1 — Supabase

1. Go to [supabase.com](https://supabase.com) → New project
2. Once created, go to **SQL Editor** → paste contents of `supabase_schema.sql` → Run
3. Go to **Settings → API** → copy:
   - `Project URL` → `SUPABASE_URL`
   - `anon/public` key → `SUPABASE_KEY`

---

## Step 2 — Resend

1. Go to [resend.com](https://resend.com) → sign up free
2. Create an API key → `RESEND_API_KEY`
3. Verify your sending domain (or use their sandbox for testing)
4. Set `EMAIL_FROM` to a verified address, `EMAIL_TO` to `redeemmakosa05@gmail.com`

---

## Step 3 — Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in all values. Generate `SECRET_KEY` with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Step 4 — Deploy to Vercel

```bash
npm i -g vercel        # install Vercel CLI
vercel login
vercel                 # deploy (follow prompts)
```

Add all `.env` values as **Environment Variables** in the Vercel dashboard:
- Settings → Environment Variables → add each key/value

---

## Step 5 — Wire up the frontend

In `admin.html`, replace:
```js
const API = 'https://your-api.vercel.app';
```
with your actual Vercel deployment URL.

In `contact.html` (frontend), replace the API URL the same way.

---

## Step 6 — Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API runs at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## API Endpoints

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | `/auth/login` | No | Get JWT token |
| POST | `/contact` | No | Submit contact form |
| GET | `/contact` | Admin | View all messages |
| POST | `/projects/{id}/view` | No | Increment view count |
| GET | `/projects/{id}/view` | No | Get view count |
| GET | `/projects/views` | Admin | All project views |
| GET | `/blog` | No | Get published posts |
| GET | `/blog/{slug}` | No | Get single post |
| POST | `/blog` | Admin | Create post |
| PUT | `/blog/{id}` | Admin | Update post |
| DELETE | `/blog/{id}` | Admin | Delete post |

---

## Admin Dashboard

Open `admin.html` in a browser. Login with the `ADMIN_USERNAME` / `ADMIN_PASSWORD` you set.
Keep this file off your public GitHub repo or add it to `.gitignore`.
