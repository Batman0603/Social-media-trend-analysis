# Social Media Trend Analysis Backend

## Project Overview
This project is a FastAPI-based backend for social media trend and engagement analysis. It supports hashtag tracking, comment sentiment analysis, user engagement reports, and more.

---

## How to Run the App

1. **Clone the repository and navigate to the project folder.**
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Set up your database connection in `.env` if needed.**
5. **Seed the database (optional):**
   ```powershell
   python scripts/seed_db.py
   ```
6. **Run the FastAPI app:**
   ```powershell
   uvicorn app.main:app --reload
   ```
7. **Open your browser at:**
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)

---

## API Endpoints & How to Test

### User Endpoints
- **POST /users**
  - Create a new user.
  - Body:
    ```json
    { "username": "your_username" }
    ```
- **GET /users**
  - List all users.
- **POST /users/with-post**
  - Atomically create a user and their first post.
  - Body:
    ```json
    { "username": "newuser123", "post_content": "This is my first post!" }
    ```

### Comment Endpoints
- **POST /comments**
  - Add a new comment (optionally as a reply with `?parent_id=...`).
  - Body:
    ```json
    { "text": "Nice post!", "user_id": 1, "post_id": 1 }
    ```
- **GET /comments**
  - Get all top-level comments with nested replies.
- **GET /comments/{comment_id}**
  - Get a single comment thread (with all nested replies).

### Hashtag Endpoints
- **GET /hashtags/trending**
  - Get trending hashtags (by frequency).
  - Optional: `/hashtags/trending?limit=5`
- **GET /hashtags/recommend/{hashtag_id}**
  - Get top 3 recommended hashtags (with >30% co-occurrence) for a given hashtag.

### Reports & Analytics
- **GET /reports/engagement**
  - Get user engagement report (posts, comments, hashtags per user).
- **GET /reports/most-engaged**
  - Get most engaged users (by post + comment count).
  - Optional: `/reports/most-engaged?limit=3`

### Root Endpoint
- **GET /**
  - Returns a status message.

---

## How to Test the API

1. **Use Swagger UI:**
   - Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API testing.
2. **Use Bruno/Postman:**
   - Set the method (GET or POST) and URL (e.g., http://localhost:8000/users).
   - For POST requests, set the body to JSON and provide the required fields.
   - Send the request and view the response.

---

## Notes
- Ensure your database is running and accessible.
- All endpoints return JSON responses.
- For nested comments, use the `parent_id` query parameter in POST /comments.

---

For any issues, check the FastAPI logs or contact the project maintainer.
