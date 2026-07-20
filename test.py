from app import create_app
from app.extensions import db
from app.models.principal import Principal

app = create_app()
with app.app_context():
    principals = Principal.query.all()
    for p in principals:
        print(f"ID: {p.id}, Username: {p.username}, Name: {p.name}")