import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

def save_file(file):
    """Saves file to local storage and returns file path."""
    if not file or not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)  # Secure filename
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    
    return file_path
