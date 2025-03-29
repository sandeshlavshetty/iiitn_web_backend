import os
from werkzeug.utils import secure_filename
from flask import current_app
from supabase import create_client
from config import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

def save_file(file):
    """Saves file to local storage and returns the file path."""
    if not file or not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)  
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)

    # Ensure directory exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    file.save(file_path)
    return filename

def delete_file(file_path):
    """Deletes a file from the local storage."""
    if not file_path or not os.path.exists(file_path):
        return False  # File doesn't exist

    try:
        os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def update_file(file, old_file_path):
    """Replaces an existing file with a new one."""
    if not file or not allowed_file(file.filename):
        return None

    # Delete old file
    delete_file(old_file_path)

    # Save new file
    return save_file(file)
