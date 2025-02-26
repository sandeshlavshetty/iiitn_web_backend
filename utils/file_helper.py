import os
from werkzeug.utils import secure_filename
from flask import current_app
from supabase import create_client
from config import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

def save_file(file):
    """Saves file to local storage and returns file path."""
    if not file or not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)  # Secure filename
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    file_path = file_path.replace("\\", "/")  # Convert backslashes to forward slashes
    print(file_path)
    print(f"Bucket name:- {Config.SUPABASE_BUCKET}")
    # return file_path
    
    #upload_response = supabase.storage.from_(Config.SUPABASE_BUCKET).upload(file_path, file_path)
    with open(file_path, "rb") as f:
        upload_response = supabase.storage.from_("media-uploads").upload(file_path, f)
        
    print(f"upload_response :- {upload_response}")
    
    file_path = os.path.join(Config.SUPABASE_STORAGE_URL,upload_response.full_path)
        
    return file_path

