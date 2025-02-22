from flask import Flask
from database import db
from flask_migrate import Migrate
from routes import register_routes
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)

register_routes(app)  # Register routes from routes/

if __name__ == "__main__":
    app.run(debug=True)
