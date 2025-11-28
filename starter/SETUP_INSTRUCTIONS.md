# Setup Instructions for Casting Agency API

This document provides step-by-step instructions to set up and run the Casting Agency API project.

## Quick Start Checklist

- [ ] Python 3.9+ installed
- [ ] PostgreSQL installed and running
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Auth0 account created
- [ ] Auth0 API and roles configured
- [ ] JWT tokens obtained
- [ ] Environment variables configured
- [ ] Databases created
- [ ] Application running

## Detailed Setup Steps

### 1. Install Prerequisites

#### Python 3.9+
```bash
python3 --version  # Should show 3.9 or higher
```

If you need to install Python:
- **macOS**: `brew install python@3.9`
- **Ubuntu**: `sudo apt-get install python3.9`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

#### PostgreSQL
```bash
postgres --version  # Should show PostgreSQL version
```

If you need to install PostgreSQL:
- **macOS**: `brew install postgresql`
- **Ubuntu**: `sudo apt-get install postgresql`
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/)

Start PostgreSQL:
```bash
# macOS
brew services start postgresql
# or
pg_ctl -D /usr/local/var/postgres start

# Ubuntu
sudo service postgresql start

# Windows
# Use Services app or pgAdmin
```

### 2. Clone and Setup Project

```bash
# Navigate to the project directory
cd "FSND-master/projects/capstone/starter"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Create Databases

```bash
# Create development database
createdb casting

# Create test database
createdb casting_test

# Verify databases exist
psql -l | grep casting
```

### 4. Configure Auth0

#### Step 4.1: Create Auth0 Account
1. Go to https://auth0.com
2. Sign up for a free account
3. Create a new tenant or use default

#### Step 4.2: Create API
1. Navigate to **Applications** → **APIs**
2. Click **Create API**
3. Configure:
   - Name: `Casting Agency`
   - Identifier: `casting-agency`
   - Signing Algorithm: `RS256`
4. Click **Create**

#### Step 4.3: Enable RBAC
1. In API Settings:
   - Enable **RBAC**
   - Enable **Add Permissions in the Access Token**
2. Click **Save**

#### Step 4.4: Create Permissions
In the **Permissions** tab of your API, add:
- `get:actors` - View actors
- `get:movies` - View movies
- `post:actors` - Create actors
- `post:movies` - Create movies
- `patch:actors` - Update actors
- `patch:movies` - Update movies
- `delete:actors` - Delete actors
- `delete:movies` - Delete movies

#### Step 4.5: Create Roles
Navigate to **User Management** → **Roles** and create:

**1. Casting Assistant**
- Permissions: `get:actors`, `get:movies`

**2. Casting Director**
- Permissions: `get:actors`, `get:movies`, `post:actors`, `delete:actors`, `patch:actors`, `patch:movies`

**3. Executive Producer**
- Permissions: All permissions (all 8 permissions)

#### Step 4.6: Create Test Users
1. Navigate to **User Management** → **Users**
2. Create 3 users:
   - `assistant@test.com` → Assign to Casting Assistant role
   - `director@test.com` → Assign to Casting Director role
   - `producer@test.com` → Assign to Executive Producer role

#### Step 4.7: Create Application for Testing
1. Go to **Applications** → **Applications**
2. Click **Create Application**
3. Name: `Casting Agency Testing`
4. Type: **Single Page Application**
5. Click **Create**
6. In Settings tab, configure:
   - Allowed Callback URLs: `http://localhost:8080/login-results`
   - Allowed Logout URLs: `http://localhost:8080`
   - Allowed Web Origins: `http://localhost:8080`
7. Save Changes
8. Note your **Domain** and **Client ID**

#### Step 4.8: Get JWT Tokens

For each test user, visit this URL (replace YOUR_DOMAIN and YOUR_CLIENT_ID):

```
https://YOUR_DOMAIN.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080/login-results
```

Example:
```
https://dev-abc123.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=abc123xyz&redirect_uri=http://localhost:8080/login-results
```

1. Open URL in browser
2. Log in with test user credentials
3. After redirect, copy the `access_token` from the URL
4. Repeat for all three users

### 5. Configure Environment Variables

Edit `setup.sh` with your actual values:

```bash
#!/bin/bash

# Database URL for local development
export DATABASE_URL="postgresql://postgres@localhost:5432/casting"

# Auth0 Configuration (replace with your values)
export AUTH0_DOMAIN="your-domain.auth0.com"
export API_AUDIENCE="casting-agency"

# JWT Tokens for Testing (paste actual tokens)
export CASTING_ASSISTANT_TOKEN="eyJhbGc..."
export CASTING_DIRECTOR_TOKEN="eyJhbGc..."
export EXECUTIVE_PRODUCER_TOKEN="eyJhbGc..."

echo "Environment variables set successfully!"
echo "DATABASE_URL: $DATABASE_URL"
echo "AUTH0_DOMAIN: $AUTH0_DOMAIN"
echo "API_AUDIENCE: $API_AUDIENCE"
```

Then source the file:
```bash
chmod +x setup.sh
source setup.sh
```

### 6. Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

Test the health endpoint:
```bash
curl http://localhost:8080/
```

Expected response:
```json
{
  "success": true,
  "message": "Casting Agency API is running!"
}
```

### 7. Run Tests

```bash
# Make sure environment variables are set
source setup.sh

# Run tests
python test_app.py
```

Expected output:
```
..........................
----------------------------------------------------------------------
Ran 26 tests in X.XXXs

OK
```

### 8. Test with Postman

1. Import the Postman collection: `casting-agency.postman_collection.json`
2. Set environment variables in Postman:
   - `host`: `http://localhost:8080`
   - `access_token`: Your JWT token
3. Test the endpoints

## Common Issues and Solutions

### Issue: "Role postgres does not exist"
**Solution** (macOS with Homebrew):
```bash
/usr/local/Cellar/postgresql/14.x/bin/createuser -s postgres
```

### Issue: "Connection refused" to PostgreSQL
**Solution**:
```bash
# Check if PostgreSQL is running
pg_ctl -D /usr/local/var/postgres status

# Start PostgreSQL
pg_ctl -D /usr/local/var/postgres start
```

### Issue: "ModuleNotFoundError"
**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Token expired" (401 error)
**Solution**:
- Auth0 tokens expire after 24 hours
- Generate new tokens following Step 4.8
- Update the tokens in `setup.sh`
- Re-source the file: `source setup.sh`

### Issue: "Permission not found" (403 error)
**Solution**:
- Verify RBAC is enabled in Auth0 API settings
- Verify "Add Permissions in the Access Token" is enabled
- Check that roles have correct permissions assigned
- Generate fresh JWT tokens

## Next Steps

1. ✅ Local development setup complete
2. ⬜ Customize the application (optional)
3. ⬜ Deploy to Render (see README.md for deployment instructions)
4. ⬜ Update README.md with deployed URL
5. ⬜ Submit project to Udacity

## Deployment to Render

See the main README.md file for detailed deployment instructions. Quick summary:

1. Create Render account
2. Create PostgreSQL database on Render
3. Create Web Service on Render
4. Connect GitHub repository
5. Set environment variables
6. Deploy!

## Verification Checklist

Before deployment, verify:

- [ ] All tests pass locally
- [ ] Health endpoint returns success
- [ ] Can create, read, update, delete actors
- [ ] Can create, read, update, delete movies
- [ ] RBAC works correctly for all three roles
- [ ] Auth0 is properly configured
- [ ] Environment variables are set correctly
- [ ] Database is properly configured

## Resources

- [Auth0 Documentation](https://auth0.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Render Documentation](https://render.com/docs)

## Support

If you encounter issues:
1. Check this document for common issues
2. Review the main README.md
3. Check Auth0 logs in the Auth0 dashboard
4. Review application logs
5. Ask for help on Udacity Knowledge platform

Good luck with your Capstone project! 🚀

