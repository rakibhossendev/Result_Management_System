"""Vercel entry point for the Flask application."""

import os

# Vercel's function filesystem is temporary and the app uses SQLite by default.
# Keep its SQLite file in the writable temporary directory on Vercel only.
if os.environ.get("VERCEL"):
    os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/result-management.db")

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
