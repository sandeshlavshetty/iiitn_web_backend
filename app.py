from flask import Flask, make_response
from database import db
from flask_migrate import Migrate
from routes import register_routes
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from config import Config
from routes.student_routes import student_bp
from flask_cors import CORS  # Import CORS
from database import init_db
  
load_dotenv()  # Load environment variables

app = Flask(__name__)
@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config.from_object(Config)

# Enable CORS globally
CORS(app, resources={r"/*": {"origins": "*"}})

# db.init_app(app)
init_db(app)
from database.models import SocialMedia  # ✅ Ensure models are imported
migrate = Migrate(app, db)
jwt = JWTManager(app)  # Initialize JWT



register_routes(app)  # Register routes from routes/

if __name__ == "__main__":
    app.run(debug=True)
