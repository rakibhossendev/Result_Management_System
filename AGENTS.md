# AGENTS.md

Single-package Flask 3 + SQLAlchemy (SQLite) app for role-based academic result management (Admin → Principal → Teacher → Student). No monorepo, **no tests, no linter/typechecker, no CI** (`.github/` does not exist).

## Run & verify

- Dev server: `source venv/bin/activate && python run.py` → http://127.0.0.1:5000 (venv at repo root, Python 3.14).
- Quick smoke check without starting the server: `venv/bin/python -c "from app import create_app; create_app()"` — it imports/registers every blueprint, so it catches typos in `app/__init__.py`.
- Since there is no test suite, verify changes by launching the app and hitting the route manually.
- Docker: `docker build -t result-management-system:dev .` then `docker run --rm -p 5000:5000 result-management-system:dev` (gunicorn `run:app` on port 5000). Vercel deploys via `vercel.json` → `run.py`.
- Dependencies are pinned in `requirements.txt` (`pip install -r requirements.txt`).

## Database: no migrations

- Schema is created only by `db.create_all()` in `run.py` at startup. **Changing a model does not alter an existing `instance/database.db`** — `create_all()` skips existing tables. To apply schema changes: delete `instance/database.db` (keep `database_backup.db`), restart, then optionally reseed.
- Sample data: `sqlite3 instance/database.db < import_students.sql` (45 students; requires teacher id `01` and principal id `2006` to already exist).
- `instance/`, `*.db`, and `.env` are gitignored — a fresh clone starts with no database and no env file.

## Architecture

- App factory `create_app()` in `app/__init__.py`: **every new Blueprint must be imported and registered there manually** — routes are not auto-discovered. A route file that is never imported is dead code.
- Layout: `app/routes/{auth,admin,principal,teacher,student,api,ai}/`, models in `app/models/`, WTForms in `app/utils/*_form.py`, templates in `app/templates/`, static in `app/static/`. (The README's "Project Structure" section is stale: there are no root-level `templates/` or `static/` dirs.)
- Data model and ownership chain (every table carries `principal_id`/`teacher_id` FKs) is documented in `Documentation/database-structure-summary.md` — read that instead of re-reading model files.

## Auth & session quirks

- No Flask-Login and **no shared auth decorator**. Each route guards itself inline, e.g. `if not session.get("teacher"): return redirect(url_for("login.login"))`. Copy this pattern for new routes; note some existing routes lack guards — don't assume they exist.
- Session keys set at login (`app/routes/auth/login.py`): `admin`/`admin_id`, `principal`/`principal_id`/`temp_principal_id`/`shift`, `teacher`/`teacher_id`, `student`/`student_id`/`student_roll`.
- First visit to `/login` auto-creates the default admin account `admin` / `admin123`.
- Students have no password: "login" is searching a roll number on `/` (`app/routes/student/home.py`).
- Teacher data access control = filter every query by `session["teacher_id"]` (never trust client-supplied ids).

## Config & AI assistant

- `.env` is gitignored (`.env.example` only lists `MISTRAL_API_KEY`). `app/config.py` reads `SECRET_KEY`/`DATABASE_URL` with hardcoded fallbacks; the `MISTRAL_API_KEY` line in `Config` is commented out — `app/routes/ai/routes.py` calls `load_dotenv()` itself at import time.
- Mistral AI chat at `/ask`: tool functions live in `app/ai/tools.py`; schema + `TOOLS_SCHEMA` registry + `dispatch_tool_call` live in `app/routes/ai/routes.py`. Adding a tool = add the function, one schema entry, one dispatch branch (comment block at top of `TOOLS_SCHEMA` explains this). Model: `mistral-small-latest`.
- CORS only allows `localhost:5173` origins. Uploaded result PDFs are stored in `instance/cgpa_pdfs/`.

## Git workflow

- Per `workflow.md`: branch off `main` (`backend_*` / `frontend_*`), merge only via GitHub PR + review. Never commit directly to `main`, never force-push. Never commit `__pycache__`, `venv`, `database.db` (already gitignored).
