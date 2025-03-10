import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

class Config:
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Secret for JWT
    SESSION_TYPE = "filesystem"
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 1 day
    
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit file size to 16MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "mp4"}  # Allowed file types
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET') 
    SUPABASE_STORAGE_URL = os.getenv('SUPABASE_STORAGE_URL')
