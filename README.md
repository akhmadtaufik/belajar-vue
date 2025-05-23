# RESTful API Documentation

## 1. Project Overview

### Brief Introduction

This document provides detailed information about the RESTful API for this project. The API allows users to register, log in, post tweets (text and images), and view tweets and user information.

### Purpose of the API

The primary purpose of this API is to serve as the backend for a microblogging-style application, handling user authentication, content management (tweets), and data retrieval.

### Technologies Used

- **Backend:**
  - Python
  - Flask (Web Framework)
  - Flask-SQLAlchemy (ORM)
  - Flask-Migrate (Database Migrations)
  - Flask-JWT-Extended (JWT Authentication)
  - Flask-Login (Session Management - used alongside JWT)
  - Flask-Cors (Cross-Origin Resource Sharing)
  - Flask-Admin (Admin Interface)
  - Gunicorn (WSGI HTTP Server for production)
  - Minio (S3-compatible Object Storage for images)
- **Database:**
  - SQLAlchemy supports multiple database backends. The `config.py` currently points to SQLite (`sqlite:///app.db`).
  - `psycopg2-binary` is listed in `requirements.txt`, suggesting PostgreSQL can also be used.
- **Frontend (separate project in `vue-frontend/`):**
  - Vue.js

## 2. Installation Guide

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Node.js and npm (for the Vue.js frontend, if running locally)
- Access to a Minio instance (or S3-compatible storage) configured to `127.0.0.1:9000` with credentials `access_key="your_access_key"`, `secret_key="your_secret_key"`, or update `app/tweet/routes.py`.

### Environment Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### How to Install Dependencies

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize/Upgrade the database:**

   ```bash
   flask db upgrade
   ```

3. **Install frontend dependencies (if running the Vue frontend):**

   ```bash
   cd vue-frontend
   npm install
   cd ..
   ```

### How to Run the Development Server

The `devserver.sh` script can be used to run both backend and frontend development servers:

```bash
./devserver.sh
```

This script performs the following:

1. Activates the Python virtual environment.
2. Starts the Flask backend server: `python -m flask run --debug` (typically on `http://127.0.0.1:5000`)
3. Navigates to the `vue-frontend` directory and starts the Vue development server: `npm run dev` (typically on a different port like `http://localhost:5173`)

**Manual Startup:**

- **Backend:**

  ```bash
  source .venv/bin/activate
  flask db upgrade # Ensure database is up-to-date
  python -m flask run --debug
  ```

- **Frontend:**

  ```bash
  cd vue-frontend
  npm run dev
  ```

## 3. Authentication & Authorization

### Authentication Method Used

The API uses JSON Web Tokens (JWT) for authentication, managed by `Flask-JWT-Extended`.

- Access tokens are short-lived (1 hour by default, configurable via `JWT_ACCESS_TOKEN_EXPIRES` in `config.py`).
- Refresh tokens are provided to obtain new access tokens without re-authentication.
- A token blacklist mechanism is implemented using the `BlacklistToken` model to handle logout by revoking tokens (denylist approach).

### How to Get an Access Token

1. **Register a new user:** Send a `POST` request to `/auth/register`.
2. **Log in:** Send a `POST` request to `/auth/login` with valid user credentials. The response will contain an `access_token` and a `refresh_token`.

   ```json
   {
     "message": "Berhasil Login",
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   }
   ```

   Include the `access_token` in the `Authorization` header for protected endpoints:
   `Authorization: Bearer <access_token>`

### Authorization Rules

User roles are defined in the `Users` model with a `role` attribute (defaulting to "user").

- **General Users (`role="user"`):**
  - Can register, login, logout, refresh tokens.
  - Can create tweets (text and image).
  - Can view all tweets and user profiles.
  - Can download/view images associated with tweets.
- **Admin Users (e.g., `role="admin"`):**
  - The Flask-Admin interface is available at `/admin` (configuration in `app/admin/`).
  - The `Users` model has a `has_role(self, role_name)` method, allowing for programmatic role checks within custom Flask-Admin views or other protected routes if implemented.
  - API endpoints are primarily protected by `@jwt_required`, meaning a valid JWT is needed. Fine-grained role-based restrictions for specific API actions would need to be explicitly added to the route handlers.

## 4. API Endpoints

Endpoints are prefixed by their respective blueprints (e.g., `/auth`, `/tweet`, `/user`).

### Authentication (`/auth`)

---

#### **Register User**

- **Endpoint:** `POST /auth/register`
- **Description:** Registers a new user.
- **Required Headers:** None
- **Path/Query Parameters:** None
- **Request Body Schema:** `application/json`

  ```json
  {
    "username": "string (required)",
    "password": "string (required)",
    "email": "string (optional)",
    "role": "string (optional, defaults to 'user')"
  }
  ```

- **Example Request:**

  ```json
  {
    "username": "newuser",
    "password": "password123",
    "email": "newuser@example.com",
    "role": "user"
  }
  ```

- **Response Schema:** `application/json`
- **Example Response (Success 200):**

  ```json
  {
    "message": "Berhasil Login" // Note: Message seems to be "Berhasil Login" even for registration
  }
  ```

- **Example Response (Error):**

  ```json
  {
    "error": "Username is required." // Or other validation errors
  }
  ```

- **Possible Status Codes:**
  - `200 OK`: User registered successfully.
  - `4xx Bad Request/Unprocessable Entity`: Missing required fields or invalid input. (The code returns `jsonify({"error": error})` without a specific status code for some errors, which defaults to 200 OK if not specified. This should ideally be a 4xx code.)

---

#### **Login User**

- **Endpoint:** `POST /auth/login`
- **Description:** Authenticates a user and returns access and refresh tokens.
- **Required Headers:** None
- **Path/Query Parameters:** None
- **Request Body Schema:** `application/json`

  ```json
  {
    "username": "string (required)",
    "password": "string (required)"
  }
  ```

- **Example Request:**

  ```json
  {
    "username": "testuser",
    "password": "password123"
  }
  ```

- **Response Schema:** `application/json`
- **Example Response (Success 200):**

  ```json
  {
    "message": "Berhasil Login",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

- **Example Response (Error 422):**

  ```json
  {
    "error": "username not found"
  }
  ```

  ```json
  {
    "error": "Incorrect password"
  }
  ```

- **Possible Status Codes:**
  - `200 OK`: Login successful.
  - `422 Unprocessable Entity`: Invalid credentials or missing fields.

---

#### **Refresh Access Token**

- **Endpoint:** `POST /auth/refresh`
- **Description:** Generates a new access token using a valid JWT identity (typically from a refresh token, though the code uses `@jwt_required` which usually implies an access token was used to identify the user for refreshing).
  _Flask-JWT-Extended handles refresh tokens typically via `@jwt_required(refresh=True)`. The current implementation `@jwt_required(locations=["headers"])` might expect an access token to get the identity for creating a new access token. This section might need clarification based on exact client-side implementation of refresh._
- **Required Headers:**
  - `Authorization: Bearer <token>` (The type of token expected - access or refresh - depends on Flask-JWT-Extended setup for this route)
- **Path/Query Parameters:** None
- **Request Body Schema:** None
- **Example Request:** (No body, just header)
- **Response Schema:** `application/json`
- **Example Response (Success 200):**

  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

- **Possible Status Codes:**
  - `200 OK`: Token refreshed successfully.
  - `401 Unauthorized`: Invalid or expired token.

---

#### **Logout User**

- **Endpoint:** `POST /auth/logout`
- **Description:** Invalidates the current user's JWT by adding its JTI (JWT ID) to a blacklist.
- **Required Headers:**
  - `Authorization: Bearer <access_token>`
- **Path/Query Parameters:** None
- **Request Body Schema:** None
- **Example Request:** (No body, just header)
- **Response Schema:** `application/json`
- **Example Response (Success 200):**

  ```json
  {
    "message": "Berhasil Logout"
  }
  ```

- **Possible Status Codes:**
  - `200 OK`: Logout successful.
  - `401 Unauthorized`: Invalid or expired token.

---

### Tweets (`/tweet`)

---

#### **Get Tweets**

- **Endpoint:** `GET /tweet`
- **Description:** Retrieves a list of tweets.
- **Required Headers:**
  - `Authorization: Bearer <access_token>` (Optional: If provided, `user_id` is included in response; otherwise, `user_id` is "None")
- **Path/Query Parameters:**
  - `limit` (integer, optional, default: 20): Maximum number of tweets to return.
- **Request Body Schema:** None
- **Example Request:** `GET /tweet?limit=10`
- **Response Schema:** `application/json`
- **Example Response (Success 200):**

  ```json
  {
    "user_id": 1, // or "None"
    "data": [
      {
        "id": 1,
        "content": "This is a tweet!",
        "user_id": 1,
        "image_name": "image.jpg",
        "image_path": "http://127.0.0.1:9000/imagebucket/image.jpg?presigned-url-params..."
      }
      // ... more tweets
    ]
  }
  ```

- **Possible Status Codes:**
  - `200 OK`: Tweets retrieved successfully.
  - `400 Bad Request`: Invalid `limit` parameter.

---

#### **Create Tweet**

- **Endpoint:** `POST /tweet`
- **Description:** Creates a new tweet. Can be text-only or include an image.
- **Required Headers:**
  - `Authorization: Bearer <access_token>`
- **Request Body Schema:**

  - **Option 1: `multipart/form-data` (for tweets with images)**
    - `content`: string (required) - The text content of the tweet.
    - `file`: file (required) - The image file (jpg, jpeg, png).
  - **Option 2: `application/json` (for text-only tweets)**

```json
{
  "content": "string (required)"
}
```

- **Example Request (multipart/form-data):**

  ```plaintext
  POST /tweet
  Authorization: Bearer <access_token>
  Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="content"

  My tweet with an image!
  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="file"; filename="photo.jpg"
  Content-Type: image/jpeg

  (binary image data)
  ------WebKitFormBoundary7MA4YWxkTrZu0gW--
  ```

- **Example Request (application/json):**

  ```json
  {
    "content": "Just a text tweet."
  }
  ```

- **Response Schema:** `application/json`
- **Example Response (Success 200):**

  ```json
  {
    "data": {
      "id": 2,
      "content": "My tweet with an image!",
      "user_id": 1,
      "image_name": "photo.jpg",
      "image_path": "http://127.0.0.1:9000/imagebucket/photo.jpg?presigned-url-params..."
    }
  }
  ```

- **Possible Status Codes:**
  - `200 OK`: Tweet created successfully.
  - `400 Bad Request`: Missing content, no file part, no selected file, or empty content.
  - `401 Unauthorized`: Invalid or missing JWT.
  - `415 Unsupported Media Type`: If content type is neither `multipart/form-data` nor `application/json`.
  - `500 Internal Server Error`: Failed to save tweet or Minio error.

---

#### **Get Tweet Image (Serve)**

- **Endpoint:** `GET /tweet/image/<string:name>`
- **Description:** Serves an image file directly. _Note: This route seems to attempt to serve from a local `./static/uploaded/` directory, which might conflict with Minio usage for `image_path` in the `Tweets` model. The `image_path` from Minio is a pre-signed URL and should be used directly by the client._ This endpoint might be legacy or for a different purpose.
- **Required Headers:**
  - `Authorization: Bearer <access_token>` (Optional)
- **Path/Query Parameters:**
  - `name` (string, required): The filename of the image.
- **Request Body Schema:** None
- **Example Request:** `GET /tweet/image/photo.jpg`
- **Response:** Image file
- **Possible Status Codes:**
  - `200 OK`: Image served.
  - `404 Not Found`: Image not found at the specified local path.

---

#### **Download Tweet Image**

- **Endpoint:** `GET /tweet/download/<string:name>`
- **Description:** Allows downloading an image file. _Similar to `/image/<name>`, this serves from a local directory (`./static/uploaded/`) and might be inconsistent with Minio usage._
- **Required Headers:**
  - `Authorization: Bearer <access_token>` (Optional)
- **Path/Query Parameters:**
  - `name` (string, required): The filename of the image.
- **Request Body Schema:** None
- **Example Request:** `GET /tweet/download/photo.jpg`
- **Response:** Image file with `Content-Disposition: attachment`.
- **Possible Status Codes:**
  - `200 OK`: Image download initiated.
  - `404 Not Found`: Image not found at the specified local path.

---

### Users (`/user`)

---

#### **Get Users**

- **Endpoint:** `GET /user`
- **Description:** Retrieves a list of users.
- **Required Headers:** None (Open endpoint)
- **Path/Query Parameters:**
  - `limit` (integer, optional, default: 10): Maximum number of users to return.
- **Request Body Schema:** None
- **Example Request:** `GET /user?limit=5`
- **Response Schema:** `application/json`
- **Example Response (Success 200):**

  ```json
  {
    "data": [
      {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "[hashed_password]"
      }
      // ... more users
    ]
  }
  ```

- **Possible Status Codes:**
  - `200 OK`: Users retrieved successfully.
  - `400 Bad Request`: Invalid `limit` parameter.

---

## 5. Data Models

### User (`Users`)

| Field      | Type        | Constraints                      | Description                          |
| ---------- | ----------- | -------------------------------- | ------------------------------------ |
| `user_id`  | Integer     | Primary Key                      | Unique identifier for the user.      |
| `username` | String      | Unique                           | User's chosen username.              |
| `email`    | String(128) |                                  | User's email address.                |
| `password` | String(128) |                                  | Hashed password for the user.        |
| `role`     | String(80)  | Not Null, Server Default: "user" | User's role (e.g., "user", "admin"). |

**Relationships:**

- Has many `Tweets` (via `Tweets.user_id`).

**Serialization (`user.serialize()`):**

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### Tweet (`Tweets`)

| Field        | Type         | Constraints                   | Description                                         |
| ------------ | ------------ | ----------------------------- | --------------------------------------------------- |
| `id`         | Integer      | Primary Key                   | Unique identifier for the tweet.                    |
| `content`    | String(128)  |                               | Text content of the tweet.                          |
| `user_id`    | Integer      | Foreign Key (`users.user_id`) | ID of the user who posted the tweet.                |
| `image_name` | String(128)  | Nullable                      | Original filename of the uploaded image.            |
| `image_path` | String(1000) | Nullable                      | URL (potentially pre-signed) to the image in Minio. |

**Relationships:**

- Belongs to `Users` (via `user` relationship).

**Serialization (`tweet.serialize()`):**

```json
{
  "id": "integer",
  "content": "string",
  "user_id": "integer",
  "image_name": "string",
  "image_path": "string"
}
```

### Blacklist Token (`BlacklistToken`)

| Field | Type       | Constraints      | Description                                |
| ----- | ---------- | ---------------- | ------------------------------------------ |
| `id`  | Integer    | Primary Key      | Unique identifier for the blacklist entry. |
| `jti` | String(36) | Not Null, Unique | The JWT ID (JTI) of the revoked token.     |

**Serialization (`blacklist_token.serialize()`):**

```json
{
  "id": "integer",
  "jti": "string"
}
```

### Tweet Count (`TweetCount`)

| Field         | Type        | Constraints      | Description                            |
| ------------- | ----------- | ---------------- | -------------------------------------- |
| `id`          | Integer     | Primary Key      | Unique identifier for the count entry. |
| `username`    | String(100) | Not Null, Unique | Username of the user.                  |
| `total_tweet` | Integer     | Default: 0       | Total number of tweets by the user.    |

**Serialization (`tweet_count.serialize()`):**

```json
{
  "id": "integer",
  "usernam": "string",
  "total_tweet": "integer"
}
```

_Note: The `TweetCount` model and its updates (e.g., via `app/scheduler/count_tweet.py`) are not directly exposed via API endpoints in the provided route files, but the model exists._

## 6. Error Handling

### Standard Error Response Format

Errors are generally returned in JSON format:

```json
{
  "error": "Descriptive error message"
}
```

Or sometimes:

```json
{
  "message": "Descriptive error message"
}
```

Status codes vary (e.g., 400, 401, 422, 500). Some error responses might default to a 200 OK status if not explicitly set in the route handler, which is not ideal.

### Common Error Messages

- **Authentication (`/auth`):**
  - `"Username is required."`
  - `"Password is required."`
  - `"username not found"` (422)
  - `"Incorrect password"` (422)
  - Flask-JWT-Extended will return its own standard error messages for invalid/expired tokens (e.g., `{"msg": "Token has expired"}` with a 401 status).
- **Tweets (`/tweet`):**
  - `"invalid parameter"` (400, for `limit`)
  - `"Invalid or missing JWT token"` (401)
  - `"No file part"` (400)
  - `"No selected file"` (400)
  - `"Tweet content cannot be empty"` (400)
  - `"Unsupported media type: <content_type>"` (415)
  - `"Failed to save tweet: <reason>"` (500)
- **Users (`/user`):**
  - `"invalid parameter"` (400, for `limit`)

## 7. Environment Variables

While the current `config.py` and `app/tweet/routes.py` use hardcoded values for secrets and configurations, the following environment variables _should_ be used for a production-ready setup:

| Variable Name              | Description                                      | Example Value                           | Used In (Recommended) |
| -------------------------- | ------------------------------------------------ | --------------------------------------- | --------------------- |
| `SECRET_KEY`               | Flask secret key for session management, etc.    | `a_very_strong_random_string`           | `config.py`           |
| `SQLALCHEMY_DATABASE_URI`  | Database connection string.                      | `postgresql://user:pass@host/db`        | `config.py`           |
| `JWT_SECRET_KEY`           | Secret key for signing JWTs.                     | `another_strong_random_secret`          | `config.py`           |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token expiration time (e.g., in seconds). | `3600` (for 1 hour)                     | `config.py`           |
| `MINIO_ENDPOINT`           | Minio server endpoint.                           | `minio.example.com` or `127.0.0.1:9000` | `app/tweet/routes.py` |
| `MINIO_ACCESS_KEY`         | Access key for Minio.                            | `your_minio_access_key`                 | `app/tweet/routes.py` |
| `MINIO_SECRET_KEY`         | Secret key for Minio.                            | `your_minio_secret_key`                 | `app/tweet/routes.py` |
| `MINIO_BUCKET_NAME`        | Name of the Minio bucket for images.             | `your_bucket_name`                      | `app/tweet/routes.py` |
| `MINIO_SECURE`             | Whether to use HTTPS for Minio (True/False).     | `False` (for local http)                | `app/tweet/routes.py` |
| `FLASK_ENV`                | Flask environment (development, production).     | `production`                            | Deployment scripts    |
| `FLASK_DEBUG`              | Flask debug mode (0 or 1).                       | `0` (for production)                    | Deployment scripts    |

These would typically be loaded using `os.environ.get()` or a library like `python-dotenv`.

## 8. Deployment

### Guide for Deploying to Production

1. **Containerization (Recommended):**
   The project includes a `Dockerfile` (though it appears incomplete in the provided listing - `COPY . /src/` then `COPY` with no args). A complete Dockerfile would look something like this:

   ```dockerfile
   FROM python:3.8.0-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip3 install --no-cache-dir --upgrade pip
   RUN pip3 install --no-cache-dir -r requirements.txt

   COPY . .

   # Ensure database migrations are run if not handled externally
   # RUN flask db upgrade

   # Expose the port Gunicorn will run on
   EXPOSE 5000

   # Command to run the application using Gunicorn
   CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]
   # Assuming your Flask app instance is created by a function create_app() in app/__init__.py
   # If app instance is named 'app' directly in app/__init__.py, use "app:app"
   ```

   Build and run the Docker container:

   ```bash
   docker build -t my-flask-app .
   docker run -p 5000:5000 \
       -e SECRET_KEY='...' \
       -e SQLALCHEMY_DATABASE_URI='...' \
       # ... other environment variables
       my-flask-app
   ```

2. **Traditional Deployment (e.g., on a VM):**

   - Ensure all prerequisites (Python, pip, database, Minio) are installed and configured on the server.
   - Set up a dedicated user for running the application.
   - Clone the repository.
   - Create and activate a virtual environment.
   - Install dependencies (`pip install -r requirements.txt`).
   - Set up environment variables (e.g., in a `.env` file loaded by `python-dotenv`, or system environment variables).
   - Run database migrations: `flask db upgrade`.
   - Use Gunicorn as the WSGI server:

     ```bash
     gunicorn --workers 4 --bind 0.0.0.0:5000 "app:create_app()"
     # Adjust workers and binding as needed.
     # Assumes app factory pattern in app/__init__.py. If app is directly instantiated:
     # gunicorn --workers 4 --bind 0.0.0.0:5000 "app:app"
     ```

   - Set up a reverse proxy (e.g., Nginx or Apache) to handle incoming HTTP(S) requests, manage SSL, and forward requests to Gunicorn.
   - Configure process management (e.g., systemd, Supervisor) to ensure the Gunicorn process runs continuously and restarts on failure.

### Environment Configuration Tips

- **Database:** Use a robust database like PostgreSQL for production instead of SQLite. Update `SQLALCHEMY_DATABASE_URI`.
- **Secrets:** NEVER hardcode secrets (API keys, database passwords, `SECRET_KEY`, `JWT_SECRET_KEY`) in code. Use environment variables.
- **Minio:** Ensure Minio is properly secured and configured for production use (e.g., HTTPS, appropriate bucket policies).
- **Flask Debug Mode:** Ensure `FLASK_DEBUG` is set to `0` or `False` in production.
- **Logging:** Configure proper logging for the application to capture errors and important events in production. Flask's default logging might not be sufficient.
- **CORS:** Configure `Flask-Cors` appropriately for your production domain(s).
- **Frontend:** The Vue.js frontend (`vue-frontend/`) needs to be built for production (`npm run build`) and its static assets served by a web server (often the same reverse proxy like Nginx). The API base URL in the frontend configuration must point to the production API deployment.

This documentation provides a comprehensive overview. Specific details for certain advanced configurations or third-party integrations might require further examination of the codebase.
