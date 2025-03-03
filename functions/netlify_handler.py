from app import app  # Your Flask app
from netlify_handler import handler

def handler(event, context):
    return handler(app, event, context)
