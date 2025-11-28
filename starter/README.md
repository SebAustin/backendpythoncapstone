# Casting Agency API

## Project Overview

The Casting Agency API is a full-stack application that models a company responsible for creating movies and managing and assigning actors to those movies. This is the capstone project for the Udacity Full Stack Web Developer Nanodegree.

### Motivation

This project demonstrates skills in:
- Data modeling with SQLAlchemy
- Building RESTful APIs with Flask
- Implementing Role-Based Access Control (RBAC) with Auth0
- Writing comprehensive unit tests
- Deploying applications to cloud platforms

### Live Application

**Deployed URL**: `https://your-app-name.onrender.com` (To be updated after deployment)

## Tech Stack

- **Python 3.9+** - Programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Auth0** - Authentication and authorization
- **Render** - Cloud deployment platform

## Getting Started

### Prerequisites

- Python 3.9 or higher
- PostgreSQL database
- Auth0 account for authentication
- pip (Python package manager)

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/udacity/FSND.git
cd FSND/projects/capstone/starter
```

#### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up the Database

Create two PostgreSQL databases (one for development, one for testing):

```bash
# Create development database
createdb casting

# Create test database
createdb casting_test
```

#### 5. Configure Environment Variables

Update the `setup.sh` file with your configuration:

```bash
# Edit setup.sh with your actual values
export DATABASE_URL="postgresql://postgres@localhost:5432/casting"
export AUTH0_DOMAIN="your-domain.auth0.com"
export API_AUDIENCE="casting-agency"
export CASTING_ASSISTANT_TOKEN="your-token-here"
export CASTING_DIRECTOR_TOKEN="your-token-here"
export EXECUTIVE_PRODUCER_TOKEN="your-token-here"
```

Then source the file:

```bash
chmod +x setup.sh
source setup.sh
```

#### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:8080`

## Auth0 Setup

### 1. Create an Auth0 Account

1. Go to [auth0.com](https://auth0.com) and create an account
2. Create a new tenant or use an existing one

### 2. Create an API

1. Navigate to **Applications** → **APIs** in the Auth0 dashboard
2. Click **Create API**
3. Set the following:
   - **Name**: Casting Agency
   - **Identifier**: `casting-agency` (this is your `API_AUDIENCE`)
   - **Signing Algorithm**: RS256
4. Click **Create**

### 3. Enable RBAC

In your API settings:
1. Go to **Settings** tab
2. Enable **RBAC**
3. Enable **Add Permissions in the Access Token**
4. Click **Save**

### 4. Create Permissions

In your API, go to **Permissions** tab and add the following:

| Permission | Description |
|------------|-------------|
| `get:actors` | View actors |
| `get:movies` | View movies |
| `post:actors` | Create actors |
| `post:movies` | Create movies |
| `patch:actors` | Update actors |
| `patch:movies` | Update movies |
| `delete:actors` | Delete actors |
| `delete:movies` | Delete movies |

### 5. Create Roles

Navigate to **User Management** → **Roles** and create three roles:

#### Casting Assistant
- Permissions: `get:actors`, `get:movies`

#### Casting Director
- Permissions: All Casting Assistant permissions plus:
  - `post:actors`
  - `delete:actors`
  - `patch:actors`
  - `patch:movies`

#### Executive Producer
- Permissions: All Casting Director permissions plus:
  - `post:movies`
  - `delete:movies`

### 6. Create Test Users

1. Navigate to **User Management** → **Users**
2. Create three test users (one for each role)
3. Assign each user to their respective role

### 7. Get JWT Tokens

To get JWT tokens for testing:

1. Create an application in Auth0:
   - Go to **Applications** → **Applications** → **Create Application**
   - Choose **Single Page Application**
   - Note the **Domain** and **Client ID**

2. Use the Auth0 authorization URL to login:
```
https://YOUR_DOMAIN.auth0.com/authorize?
  audience=casting-agency&
  response_type=token&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=http://localhost:8080/login-results
```

3. Copy the access token from the URL after login
4. Add the tokens to your `setup.sh` file

## API Documentation

### Base URL

**Local**: `http://localhost:8080`

**Production**: `https://your-app-name.onrender.com`

### Authentication

All endpoints require authentication via JWT tokens passed in the Authorization header:

```
Authorization: Bearer <token>
```

### Endpoints

#### GET /

Health check endpoint

**Response:**
```json
{
  "success": true,
  "message": "Casting Agency API is running!"
}
```

#### GET /actors

Get all actors

**Required Permission:** `get:actors`

**Response:**
```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Tom Hanks",
      "age": 65,
      "gender": "Male"
    }
  ]
}
```

#### POST /actors

Create a new actor

**Required Permission:** `post:actors`

**Request Body:**
```json
{
  "name": "Tom Hanks",
  "age": 65,
  "gender": "Male"
}
```

**Response:**
```json
{
  "success": true,
  "actor": {
    "id": 1,
    "name": "Tom Hanks",
    "age": 65,
    "gender": "Male"
  }
}
```

#### PATCH /actors/<actor_id>

Update an existing actor

**Required Permission:** `patch:actors`

**Request Body:**
```json
{
  "name": "Tom Hanks Updated",
  "age": 66
}
```

**Response:**
```json
{
  "success": true,
  "actor": {
    "id": 1,
    "name": "Tom Hanks Updated",
    "age": 66,
    "gender": "Male"
  }
}
```

#### DELETE /actors/<actor_id>

Delete an actor

**Required Permission:** `delete:actors`

**Response:**
```json
{
  "success": true,
  "delete": 1
}
```

#### GET /movies

Get all movies

**Required Permission:** `get:movies`

**Response:**
```json
{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "Forrest Gump",
      "release_date": "1994-07-06"
    }
  ]
}
```

#### POST /movies

Create a new movie

**Required Permission:** `post:movies`

**Request Body:**
```json
{
  "title": "Forrest Gump",
  "release_date": "1994-07-06"
}
```

**Response:**
```json
{
  "success": true,
  "movie": {
    "id": 1,
    "title": "Forrest Gump",
    "release_date": "1994-07-06"
  }
}
```

#### PATCH /movies/<movie_id>

Update an existing movie

**Required Permission:** `patch:movies`

**Request Body:**
```json
{
  "title": "Forrest Gump Updated",
  "release_date": "1994-07-07"
}
```

**Response:**
```json
{
  "success": true,
  "movie": {
    "id": 1,
    "title": "Forrest Gump Updated",
    "release_date": "1994-07-07"
  }
}
```

#### DELETE /movies/<movie_id>

Delete a movie

**Required Permission:** `delete:movies`

**Response:**
```json
{
  "success": true,
  "delete": 1
}
```

### Error Responses

All error responses follow this format:

```json
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

#### Error Codes

- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Resource Not Found
- **422**: Unprocessable Entity
- **500**: Internal Server Error

## Roles and Permissions

### Permissions Matrix

| Endpoint | Casting Assistant | Casting Director | Executive Producer |
|----------|-------------------|------------------|-------------------|
| GET /actors | ✅ | ✅ | ✅ |
| GET /movies | ✅ | ✅ | ✅ |
| POST /actors | ❌ | ✅ | ✅ |
| POST /movies | ❌ | ❌ | ✅ |
| PATCH /actors | ❌ | ✅ | ✅ |
| PATCH /movies | ❌ | ✅ | ✅ |
| DELETE /actors | ❌ | ✅ | ✅ |
| DELETE /movies | ❌ | ❌ | ✅ |

### Role Descriptions

#### Casting Assistant
- **Description**: Can view actors and movies
- **Permissions**: `get:actors`, `get:movies`
- **Use Case**: View-only access to the casting database

#### Casting Director
- **Description**: Can manage actors and modify movies
- **Permissions**: All Casting Assistant permissions plus `post:actors`, `delete:actors`, `patch:actors`, `patch:movies`
- **Use Case**: Manage day-to-day casting operations

#### Executive Producer
- **Description**: Full access to all resources
- **Permissions**: All Casting Director permissions plus `post:movies`, `delete:movies`
- **Use Case**: Complete control over the entire system

## Testing

### Running Tests

1. Ensure the test database is created:
```bash
createdb casting_test
```

2. Set environment variables (tokens must be valid):
```bash
source setup.sh
```

3. Run the test suite:
```bash
python test_app.py
```

### Test Coverage

The test suite includes:
- **Success tests**: 8 tests for successful endpoint operations
- **Error tests**: 8 tests for error handling
- **RBAC tests**: 10+ tests for role-based access control

Total: 26+ comprehensive tests

### Test Structure

```
test_app.py
├── Actor Endpoint Tests
│   ├── Success: GET, POST, PATCH, DELETE
│   └── Error: Missing auth, invalid data, not found
├── Movie Endpoint Tests
│   ├── Success: GET, POST, PATCH, DELETE
│   └── Error: Missing auth, invalid data, not found
└── RBAC Tests
    ├── Casting Assistant (view only)
    ├── Casting Director (manage actors, modify movies)
    └── Executive Producer (full access)
```

## Deployment to Render

### Prerequisites

1. Create a [Render account](https://render.com)
2. Have your code in a GitHub repository
3. Set up Auth0 as described above

### Step 1: Create PostgreSQL Database

1. Log into Render Dashboard
2. Click **New** → **PostgreSQL**
3. Configure:
   - **Name**: `casting-db`
   - **Database**: Auto-generated
   - **User**: Auto-generated
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click **Create Database**
5. Copy the **Internal Database URL**

### Step 2: Create Web Service

1. In Render Dashboard, click **New** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `casting-agency-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:APP`
   - **Plan**: Free

### Step 3: Add Environment Variables

In the Web Service settings, add these environment variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (Paste the Internal Database URL from PostgreSQL service) |
| `AUTH0_DOMAIN` | your-domain.auth0.com |
| `API_AUDIENCE` | casting-agency |
| `PYTHON_VERSION` | 3.9.18 |

### Step 4: Deploy

1. Click **Create Web Service**
2. Render will automatically build and deploy your application
3. Once deployed, your app will be available at the provided URL

### Step 5: Update Auth0 Settings

1. Go to your Auth0 Application settings
2. Add your Render URL to:
   - Allowed Callback URLs
   - Allowed Logout URLs
   - Allowed Web Origins

### Step 6: Test the Deployment

Use the provided Render URL to test your endpoints:

```bash
curl https://your-app-name.onrender.com
```

## Project Structure

```
casting-agency/
├── app.py                 # Main application file
├── models.py              # Database models
├── test_app.py            # Test suite
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for deployment
├── setup.sh              # Environment setup script
├── .gitignore            # Git ignore patterns
├── README.md             # This file
└── auth/
    ├── __init__.py       # Auth module initialization
    └── auth.py           # Authentication and authorization
```

## API Testing with Postman/cURL

### Example cURL Requests

**Get all actors:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8080/actors
```

**Create an actor:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Tom Hanks","age":65,"gender":"Male"}' \
  http://localhost:8080/actors
```

**Update an actor:**
```bash
curl -X PATCH \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"age":66}' \
  http://localhost:8080/actors/1
```

**Delete an actor:**
```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8080/actors/1
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. Verify PostgreSQL is running:
```bash
pg_ctl -D /usr/local/var/postgres status
```

2. Check your DATABASE_URL format:
```bash
echo $DATABASE_URL
# Should be: postgresql://user@localhost:5432/dbname
```

3. Test database connection:
```bash
psql $DATABASE_URL
```

### Authentication Issues

If you get 401/403 errors:

1. Verify your token is not expired (Auth0 tokens expire after 24 hours)
2. Check that permissions are correctly assigned to roles in Auth0
3. Ensure RBAC is enabled in your Auth0 API settings
4. Verify the token includes permissions in the payload

### Import Errors

If you get module import errors:

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify Python version
python --version  # Should be 3.9+
```

## Contributing

This is a capstone project for educational purposes. Contributions are not expected, but feedback is welcome!

## License

This project is part of the Udacity Full Stack Web Developer Nanodegree.

## Acknowledgments

- Udacity for the project specifications
- Auth0 for authentication services
- Render for hosting platform

## Author

Your Name - Udacity Full Stack Web Developer Nanodegree Student

## Contact

For questions or issues, please contact through the Udacity platform.

