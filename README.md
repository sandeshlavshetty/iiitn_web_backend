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

note:- 
from flask_cors import CORS

CORS(auth_bp, resources={r"/*": {"origins": "*"}})
CORS(media_bp, resources={r"/*": {"origins": "http://localhost:3000"}})

# API Endpoints


```markdown
# API Documentation

This document describes the API endpoints for the application.  It provides details on request methods, input parameters, expected outputs, and example `curl` commands.

## Authentication (auth_bp)

### Login (`/login`)

* **Method:** POST
* **Description:** Authenticates a user and returns a JWT token.
* **Input (JSON):**
```json
{
  "email": "[email address removed]",
  "password": "password123"
}
```
* **Expected Output (JSON):**
```json
{
  "access_token": "eyJ..." // JWT token
}
```
* **Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "[email address removed]", "password": "password123"}' http://your-api-domain/login
```
* **Error Response (401):**
```json
{
  "message": "Invalid credentials"
}
```

### Protected Resource (`/protected`)

* **Method:** GET
* **Description:**  A protected endpoint that requires a valid JWT token.
* **Headers:**
  * `Authorization: Bearer <access_token>`
* **Expected Output (JSON):**
```json
{
  "message": "Welcome, [email address removed]!"
}
```
* **Curl Example:**
```bash
curl -X GET -H "Authorization: Bearer eyJ..." http://your-api-domain/protected
```

## Card (card_bp)

### Get All Cards (`/cards`)

* **Method:** GET
* **Description:** Retrieves all cards.
* **Expected Output (JSON):**
```json
[
  {
    "c_id": 1,
    "c_category": "Category A",
    "c_sub_category": "Subcategory 1",
    "title": "Card Title",
    "caption": "Card Caption",
    "content": "Card Content",
    "date": "2024-10-27",
    "location": "Location 1",
    "media_img_id": 1,
    "media_vid_id": null,
    "media_doc_id": null,
    "updated_by": 1,
    "updated_time": "2024-10-27 10:00:00",
    "added_by": 1,
    "added_time": "2024-10-27 09:00:00"
  },
  // ... more cards
]
```
* **Curl Example:**
```bash
curl http://your-api-domain/cards
```

### Create Card (`/cards`)

* **Method:** POST
* **Description:** Creates a new card.
* **Input (JSON):**
```json
{
  "c_category": "Category B",
  "c_sub_category": "Subcategory 2",
  "title": "New Card",
  // ... other card data
}
```
* **Expected Output (JSON):**
```json
{
  "message": "Card created",
  "card": 2  // New card ID
}
```
* **Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{ "c_category": "Category B", ... }' http://your-api-domain/cards
```

### Get Card by ID (`/cards/<int:c_id>`)

* **Method:** GET
* **Description:** Retrieves a specific card by ID.
* **Expected Output (JSON):** (Same structure as Get All Cards, but for a single card)
* **Curl Example:**
```bash
curl http://your-api-domain/cards/1
```

### Update Card (`/cards/<int:c_id>`)

* **Method:** PUT
* **Description:** Updates a specific card.
* **Input (JSON):** (Card data to update)
* **Expected Output (JSON):**
```json
{
  "message": "Card updated"
}
```
* **Curl Example:**
```bash
curl -X PUT -H "Content-Type: application/json" -d '{ "title": "Updated Title", ... }' http://your-api-domain/cards/1
```

### Delete Card (`/cards/<int:c_id>`)

* **Method:** DELETE
* **Description:** Deletes a specific card.
* **Expected Output (JSON):**
```json
{
  "message": "Card deleted"
}
```
* **Curl Example:**
```bash
curl -X DELETE http://your-api-domain/cards/1
```

## Department (department_bp)

*(Similar structure to Card routes.  Replace `card` with `department` and `c_id` with `d_id` in URLs and JSON payloads.)*

## Faculty/Staff (faculty_bp)

*(Similar structure to Card routes.  Replace `card` with `faculty_staff` and `c_id` with `f_id` in URLs and JSON payloads.)*

## Media (media_bp)

### Upload File (`/upload`)

* **Method:** POST
* **Description:** Uploads a file.
* **Input (FormData):**
  * `file`: The file to upload.
  * `media_type`: The type of media ("image", "video", "document").
* **Expected Output (JSON):**
```json
{
  "message": "File uploaded successfully",
  "media_id": 1, // ID of the created media entry
  "file_path": "/path/to/uploaded/file"
}
```
* **Curl Example:**
```bash
curl -X POST -F "file=@/path/to/file.jpg" -F "media_type=image" http://your-api-domain/upload
```

### Get Media Details (`/<media_type>/<int:media_id>`)

* **Method:** GET
* **Description:** Retrieves details of a specific media item.
* **Expected Output (JSON):**
```json
{
    "media_id": 1,
    "file_name": "image.jpg",
    "file_path": "/path/to/uploaded/file/image.jpg"
}
```
* **Curl Example:**
```bash
curl http://your-api-domain/image/1
```

### Delete Media File (`/<media_type>/<int:media_id>`)

* **Method:** DELETE
* **Description:** Deletes a specific media file.
* **Expected Output (JSON):**
```json
{
  "message": "Media deleted successfully"
}
```
* **Curl Example:**
```bash
curl -X DELETE http://your-api-domain/image/1
```

### Add Media (`/media`)

* **Method:** POST
* **Input (JSON):**
```json
{
  "m_category": "Category",
  "m_sub_category": "Subcategory",
  "title": "Media Title",
  // ... other media data
}
```
* **Expected Output (JSON):**
```json
{
  "message": "Media added successfully",
  "m_id": 1  // New media ID
}
```
* **Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{ "m_category": "Category", ... }' http://your-api-domain/media
```

### Get All Media (`/media`)

* **Method:** GET
* **Description:** Retrieves all media entries.
* **Expected Output (JSON):** (Array of media objects)
* **Curl Example:**
```bash
curl http://your-api-domain/media
```

### Get Media by ID (`/media/<int:m_id>`)

* **Method:** GET
* **Description:** Retrieves a specific media entry by ID.
* **Expected Output (JSON):** (Single media object)
* **Curl Example:**
```bash
curl http://your-api-domain/media/1
```

### Update Media (`/media/<int:m_id>`)

* **Method:** PUT
* **Description:** Updates a specific media entry.
* **Input (JSON):** (Media data to update)
* **Expected Output (JSON):**
```json
{
  "message": "Media updated successfully"
}
```
* **Curl Example:**
```bash
curl -X PUT -H "Content-Type: application/json" -d '{ "title": "Updated Title", ... }' http://your-api-domain/media/1
```

### Delete Media (`/media/<int:m_id>`)

* **Method:** DELETE
* **Description:** Deletes a specific media entry.
* **Expected Output (JSON):

```markdown
{
  "message": "Media deleted successfully"
}
```
* **Curl Example:**
```bash
curl -X DELETE http://your-api-domain/media/1
```

## Social Media (social_media_bp)

### Get Social Media Links (`/`)

* **Method:** GET
* **Description:** Retrieves social media links.
* **Expected Output (JSON):**
```json
{
  "sm_id": 1,
  "insta": "instagram_link",
  "twitter": "twitter_link",
  "linkedin": "linkedin_link",
  "youtube": "youtube_link"
}
```
* **Curl Example:**
```bash
curl http://your-api-domain/
```

### Update Social Media Links (`/`)

* **Method:** POST
* **Description:** Updates social media links.  (This route uses POST, which might be better suited as a PUT since it's an update. Consider changing it.)
* **Input (JSON):**
```json
{
  "insta": "new_instagram_link",
  "twitter": "new_twitter_link",
  "linkedin": "new_linkedin_link",
  "youtube": "new_youtube_link"
}
```
* **Expected Output (JSON):**
```json
{
  "message": "Social media links updated",
  "sm_id": 1
}
```
* **Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{ "insta": "new_instagram_link", ... }' http://your-api-domain/
```

### Delete Social Media Links (`/`)

* **Method:** DELETE
* **Description:** Deletes social media links.
* **Expected Output (JSON):**
```json
{
  "message": "Social media links deleted"
}
```
* **Curl Example:**
```bash
curl -X DELETE http://your-api-domain/
```

## Student (student_bp)

*(Similar structure to Card routes. Replace `card` with `student` and `c_id` with `s_id` in URLs and JSON payloads.  Note that `s_id` is a string.)*

## User (user_bp)

### Get All Persons (`/`)

* **Method:** GET
* **Description:** Retrieves all persons.
* **Expected Output (JSON):** (Array of person objects)
* **Curl Example:**
```bash
curl http://your-api-domain/
```

### Get Person by ID (`/<int:p_id>`)

* **Method:** GET
* **Description:** Retrieves a specific person by ID.
* **Expected Output (JSON):** (Single person object)
* **Curl Example:**
```bash
curl http://your-api-domain/1
```

### Create Person (`/`)

* **Method:** POST
* **Description:** Creates a new person.
* **Input (JSON):**
```json
{
  "email_pri": "[email address removed]",
  "name": "John Doe",
  "phone_no": "123-456-7890",
  "password": "password123",  // Should be hashed on the server
  "role": "student",
  // ... other person data
}
```
* **Expected Output (JSON):**
```json
{
  "message": "Person added",
  "p_id": 1
}
```
* **Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{ "email_pri": "[email address removed]", ... }' http://your-api-domain/
```

### Update Person (`/<int:p_id>`)

* **Method:** PUT
* **Description:** Updates a specific person.
* **Input (JSON):** (Person data to update)
* **Expected Output (JSON):**
```json
{
  "message": "Person updated",
  "p_id": 1
}
```
* **Curl Example:**
```bash
curl -X PUT -H "Content-Type: application/json" -d '{ "name": "Jane Doe", ... }' http://your-api-domain/1
```

### Delete Person (`/<int:p_id>`)

* **Method:** DELETE
* **Description:** Deletes a specific person.
* **Expected Output (JSON):**
```json
{
  "message": "Person deleted"
}
```
* **Curl Example:**
```bash
curl -X DELETE http://your-api-domain/1
```

**Important Notes:**

* Replace `http://your-api-domain` with the actual domain or IP address of your API.
* The `password` in the input JSON for the `/` (POST) user route should be hashed on the server-side before being stored in the database.  **Never** store passwords in plain text.
* Consider using a tool like Swagger or Postman to generate and interact with API documentation more effectively.  This Markdown is a good start, but interactive tools are much better for development.
*  Review the use of POST vs PUT for updates.  Generally, PUT is preferred for updates to existing resources.
*  Ensure proper error handling and status codes are returned by your API for various scenarios (e.g., resource not found, invalid input, server errors).


# api 