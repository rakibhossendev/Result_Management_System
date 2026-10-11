import os

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
    MISTRAL_API_BASE = os.environ.get(
        "MISTRAL_API_BASE",
        "https://api.mistral.ai"
    )

# Old code     


# class Config: 
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key' 
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db' 
#     SQLALCHEMY_TRACK_MODIFICATIONS = False 
#     # Mistral AI settings MISTRAL_API_KEY = os.environ.get('MISTRAL_API_KEY') or None 
#     MISTRAL_API_BASE = os.environ.get('MISTRAL_API_BASE') or 'https://api.mistral.ai'