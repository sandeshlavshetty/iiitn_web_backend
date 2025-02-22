# iiitn_web_backend
## file structure
college_backend/
│── app.py                # Main Flask app
│── config.py             # Configuration settings (DB, JWT, etc.)
│── requirements.txt      # List of dependencies
│── .env                  # Environment variables (DB credentials, secret keys)
│
├── database/
│   ├── __init__.py       # Initializes SQLAlchemy instance
│   ├── models.py         # Defines database tables (ORM models)
│   ├── db_operations.py  # CRUD operations
│
├── routes/
│   ├── __init__.py       # Initializes Blueprint
│   ├── auth_routes.py    # Authentication endpoints (login, register)
│   ├── user_routes.py    # User-related endpoints
│   ├── media_routes.py   # Media upload & retrieval
│   ├── card_routes.py    # Card CRUD APIs
│   ├── faculty_routes.py # Faculty & staff APIs
│   ├── student_routes.py # Student-related APIs
│
├── utils/
│   ├── __init__.py       # Helper functions
│   ├── jwt_helper.py     # JWT token functions
│   ├── hash_helper.py    # Password hashing functions
│   ├── file_helper.py    # File storage functions
│
└── migrations/           # Auto-generated database migrations

📌 Explanation:
✅ app.py → Entry point for Flask
✅ config.py → Stores DB connection, JWT secret key, etc.
✅ database/models.py → Defines PostgreSQL schema using SQLAlchemy
✅ routes/ → API endpoints grouped by functionality
✅ utils/ → Helper functions (hashing, JWT, file handling)
✅ migrations/ → Stores database migration history


