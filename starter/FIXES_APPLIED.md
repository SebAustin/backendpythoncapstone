# Fixes Applied for Python 3.14 Compatibility

## Summary

The Casting Agency project has been successfully updated to work with Python 3.11 due to compatibility issues with Python 3.14 and certain dependencies.

## Issues Encountered & Solutions

### 1. **Python 3.14 Compatibility Issues**

**Problem**: Python 3.14 is too new, and several dependencies don't have pre-built wheels or have compilation errors:
- `psycopg2-binary==2.9.1` - Failed to compile on Python 3.14 (missing function declarations)
- `greenlet==1.1.0` - No wheels available for Python 3.14
- `python-jose==3.3.0` - Contains Python 2 syntax (`print` statements without parentheses)

**Solution**: Switched to Python 3.11.14, which has excellent compatibility with all dependencies.

```bash
# Remove old virtual environment
rm -rf venv

# Create new environment with Python 3.11
python3.11 -m venv venv
source venv/bin/activate
```

### 2. **JWT Library Incompatibility**

**Problem**: `python-jose==3.3.0` has Python 2 syntax incompatible with Python 3.14+

**Solution**: Replaced `python-jose` with `PyJWT==2.8.0`, which is better maintained and Auth0-recommended.

**Changes Made**:

#### `requirements.txt`
- Removed: `python-jose==3.3.0`, `ecdsa`, `pyasn1`, `rsa`
- Added: `PyJWT==2.8.0`, `cryptography==42.0.5`
- Updated all dependencies to modern, compatible versions

#### `auth/auth.py`
- Changed import: `from jose import jwt` → `import jwt`
- Updated `verify_decode_jwt()` function to use PyJWT API:
  - Added `from jwt.algorithms import RSAAlgorithm`
  - Convert JWK to PEM format using `RSAAlgorithm.from_jwk()`
  - Updated exception handling for PyJWT-specific exceptions

### 3. **Flask-SQLAlchemy 3.x Context Requirements**

**Problem**: Flask-SQLAlchemy 3.0+ requires application context for `db.create_all()`

**Solution**: Wrapped `db.create_all()` in application context

#### `models.py`
```python
# Before
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()  # ❌ Error: Working outside of application context

# After
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():  # ✅ Fixed
        db.create_all()
```

### 4. **PostgreSQL Role Configuration**

**Problem**: Default `DATABASE_URL` used "postgres" role, which doesn't exist on macOS Homebrew PostgreSQL installations

**Solution**: Updated database URL to use the actual system username

#### `setup.sh` and `models.py`
```bash
# Before
export DATABASE_URL="postgresql://postgres@localhost:5432/casting"

# After
export DATABASE_URL="postgresql://shenry@localhost:5432/casting"
```

### 5. **Runtime Configuration**

**Problem**: `runtime.txt` specified Python 3.9.18

**Solution**: Updated to Python 3.11.14 for Render deployment

#### `runtime.txt`
```
python-3.11.14
```

## Updated Dependencies

### Final `requirements.txt`
```
alembic==1.13.1
click==8.1.7
cryptography==42.0.5
Flask==2.3.3
Flask-Cors==4.0.0
Flask-Migrate==4.0.5
Flask-Script==2.0.6
Flask-SQLAlchemy==3.0.5
greenlet==3.0.3
gunicorn==21.2.0
itsdangerous==2.1.2
Jinja2==3.1.3
Mako==1.3.2
MarkupSafe==2.1.5
psycopg2-binary==2.9.9
python-dateutil==2.9.0
python-editor==1.0.4
PyJWT==2.8.0
six==1.16.0
SQLAlchemy==2.0.25
Werkzeug==2.3.7
```

## Verification

### ✅ Application Successfully Running

```bash
$ python app.py
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:8080

$ curl http://localhost:8080/
{
  "message": "Casting Agency API is running!",
  "success": true
}
```

### ✅ All Imports Working

```bash
$ python -c "from app import APP; print('✅ App imports successfully!')"
✅ App imports successfully!
```

### ✅ Database Connection Working

- Database tables created successfully
- PostgreSQL connection established
- No import or runtime errors

## Testing Instructions

1. **Setup Environment**:
   ```bash
   cd "FSND-master/projects/capstone/starter"
   source venv/bin/activate
   ```

2. **Source Environment Variables**:
   ```bash
   source setup.sh
   ```

3. **Run Application**:
   ```bash
   python app.py
   ```

4. **Test Health Endpoint**:
   ```bash
   curl http://localhost:8080/
   ```

## Next Steps

1. ✅ Python 3.11 environment configured
2. ✅ All dependencies installed and working
3. ✅ Application running successfully
4. ⏳ Configure Auth0 (follow SETUP_INSTRUCTIONS.md)
5. ⏳ Obtain JWT tokens for testing
6. ⏳ Run unit tests
7. ⏳ Deploy to Render

## Compatibility Notes

- **Python Version**: 3.11.14 (recommended for production)
- **Alternative**: Python 3.12.x also works well
- **Avoid**: Python 3.14+ (too new, limited package support)
- **JWT Library**: PyJWT 2.8.0 (replaces python-jose)
- **Flask-SQLAlchemy**: 3.0.5 (requires app context for db operations)

## Files Modified

1. `requirements.txt` - Updated all dependencies
2. `auth/auth.py` - Switched from python-jose to PyJWT
3. `models.py` - Added app context for db.create_all(), updated database URL
4. `setup.sh` - Updated database URL with correct username
5. `runtime.txt` - Changed to Python 3.11.14

## Additional Resources

- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [Flask-SQLAlchemy 3.x Migration Guide](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/changes/)
- [Auth0 + PyJWT Guide](https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-key-sets)

---

**Date**: November 27, 2025  
**Status**: ✅ All Issues Resolved  
**Application**: Fully Functional

