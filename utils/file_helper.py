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
    
    
    
    with open(file_path, "rb") as f:
        upload_response = supabase.storage.from_(Config.SUPABASE_BUCKET).upload(file_path, f)
        
    
    file_path = upload_response.path    
    return file_path

def delete_file(file_path):
    if not file_path:
        return None  # Ensure early return
    
    delete_response = supabase.storage.from_(Config.SUPABASE_BUCKET).remove([file_path])
    
    print(f"Supabase delete response: {delete_response}")  # Debugging
    
    if not delete_response:  # If deletion fails
        return "supa delete error"
    
    return True


def update_file(file,file_path_global):
    if not file or not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)  # Secure filename
    file_path_local = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    
    with open(file_path_local,"rb") as f:
        update_response = supabase.storage.from_(Config.SUPABASE_BUCKET).update(f,file_path_global,file_options={"cache-control": "3600", "upsert": "true"})
        
    if not update_response:
        return None
    
    return update_response