# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup and Running

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app (also initializes the SQLite DB on first run)
python app.py
```

- Registration: http://127.0.0.1:5000
- Admin panel: http://127.0.0.1:5000/admin
- Excel export: button on admin page (downloads `exports/register.xlsx`)

## Architecture

Single-file Flask app (`app.py`) with SQLite storage. No ORM — raw `sqlite3` with parameterized queries.

**Routes:**
- `GET/POST /` — registration form (`register.html`); validates email (regex) and phone, inserts into DB
- `GET /success` — confirmation page after successful registration
- `GET /admin` — lists all registrations newest-first
- `GET /admin/export-excel` — exports DB to Excel via pandas and streams the file

**Database:** `register.db` (auto-created on startup via `init_db()`). Single table `register` with fields: `id`, `ovog` (last name), `ner` (first name), `utas` (phone), `email` (unique), `created_at`.

**Templates** extend `base.html` (Jinja2). UI language is Mongolian. Flash messages use `"error"` category for validation errors.

**Key constraint:** `email` column has a `UNIQUE` constraint — duplicate emails are caught via `sqlite3.IntegrityError`.
