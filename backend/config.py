import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    QDRANT_HOST = os.environ.get('QDRANT_HOST') or 'localhost'
    QDRANT_PORT = int(os.environ.get('QDRANT_PORT') or 6333)