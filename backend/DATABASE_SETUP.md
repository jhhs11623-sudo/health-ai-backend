# Database Setup Guide

## Overview
This guide explains how to set up and use the database system for storing user login information and medical history.

## Database Architecture

### Database Models

#### 1. **User Model** (`users` table)
Stores user account information:
- `id` - Primary key
- `username` - Unique username for login
- `email` - Unique email address
- `password_hash` - Hashed password (never stores plain text)
- `first_name`, `last_name` - User's name
- `age`, `gender` - Demographic information
- `created_at`, `updated_at` - Timestamp fields
- `is_active` - Account status

#### 2. **MedicalHistory Model** (`medical_histories` table)
Stores patient medical records:
- `id` - Primary key
- `user_id` - Foreign key to users table
- `symptoms` - List of reported symptoms (JSON)
- `symptom_predictions` - AI predictions from symptoms (JSON)
- `image_type` - Type of medical image ('skin' or 'xray')
- `image_predictions` - AI predictions from images (JSON)
- `risk_assessment` - Health risk assessment (JSON)
- `blood_type` - Patient's blood type
- `allergies` - Known allergies
- `medications` - Current medications
- `medical_conditions` - Chronic conditions/history (JSON)
- `blood_pressure`, `heart_rate`, `temperature` - Vital signs
- `weight`, `height` - Biometric data
- `consultation_notes` - Doctor notes
- `doctor_name` - Consulting physician
- `record_type` - Type of record ('symptom_check', 'image_analysis', 'risk_assessment', 'general')
- `created_at`, `updated_at` - Timestamp fields

#### 3. **Session Model** (`sessions` table)
Tracks active user sessions:
- `id` - Primary key
- `user_id` - Foreign key to users table
- `token` - Session/JWT token
- `created_at`, `expires_at` - Token validity period
- `is_active` - Session status
- `ip_address` - User's IP address
- `user_agent` - Browser/client information

## Setup Instructions

### 1. Install Required Packages

```bash
cd backend
pip install -r requirements.txt
```

**Key packages:**
- `Flask-SQLAlchemy` - ORM for database management
- `PyJWT` - JWT token generation and validation
- `Werkzeug` - Password hashing utilities

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory (use `.env.example` as template):

```bash
# Database Configuration
DATABASE_URL=sqlite:///health_ai.db

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

**Database URL Examples:**
- **SQLite (Local):** `sqlite:///health_ai.db` (easiest for development)
- **PostgreSQL:** `postgresql://user:password@localhost:5432/health_ai`
- **MySQL:** `mysql+pymysql://user:password@localhost:3306/health_ai`

### 3. Initialize the Database

**Option A: Using the initialization script (recommended)**
```bash
python init_db.py
```

This will:
- Create all database tables
- Create a test user (username: `testuser`, password: `password123`)
- Add sample medical history
- Display database information

**Option B: Automatic initialization**
The database is automatically initialized when the Flask app starts (first run).

**Option C: POST request to the API**
```bash
curl -X POST http://localhost:5000/api/db/init
```

## API Endpoints

### Authentication Endpoints

#### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "gender": "M"
}

Response: 
{
  "message": "User registered successfully",
  "token": "jwt_token_here",
  "user": {user object}
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}

Response:
{
  "message": "Login successful",
  "token": "jwt_token_here",
  "user": {user object}
}
```

#### Get User Profile
```
GET /api/auth/profile
Authorization: Bearer {token}

Response: {user object}
```

#### Update User Profile
```
PUT /api/auth/profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "first_name": "John",
  "age": 31
}
```

#### Change Password
```
POST /api/auth/change-password
Authorization: Bearer {token}
Content-Type: application/json

{
  "old_password": "old_pass",
  "new_password": "new_pass"
}
```

#### Delete Account
```
DELETE /api/auth/delete-account
Authorization: Bearer {token}
Content-Type: application/json

{
  "password": "user_password"
}
```

### Medical History Endpoints

#### Get All Medical Records
```
GET /api/auth/medical-history
Authorization: Bearer {token}

Response:
{
  "records": [
    {record object},
    ...
  ],
  "total": 5
}
```

#### Add Medical History Record
```
POST /api/auth/medical-history
Authorization: Bearer {token}
Content-Type: application/json

{
  "record_type": "general",
  "blood_type": "O+",
  "allergies": "Penicillin",
  "medications": "Aspirin",
  "blood_pressure": "120/80",
  "heart_rate": 72,
  "temperature": 98.6,
  "weight": 70.5,
  "height": 175.0,
  "symptoms": ["cough", "fever"],
  "symptom_predictions": {"disease": "Common Cold"},
  "consultation_notes": "Patient reports mild symptoms"
}

Response:
{
  "message": "Medical history record added successfully",
  "record": {record object}
}
```

#### Get Specific Medical Record
```
GET /api/auth/medical-history/{record_id}
Authorization: Bearer {token}

Response: {record object}
```

#### Update Medical Record
```
PUT /api/auth/medical-history/{record_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "consultation_notes": "Updated notes",
  "blood_pressure": "118/78"
}
```

#### Delete Medical Record
```
DELETE /api/auth/medical-history/{record_id}
Authorization: Bearer {token}
```

## Testing the Setup

### 1. Start the Backend Server
```bash
cd backend
python app.py
```

You should see:
```
✓ Database tables initialized successfully
🚀 Starting Health AI Backend Server...
 * Running on http://0.0.0.0:5000
```

### 2. Test Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "first_name": "New",
    "last_name": "User"
  }'
```

### 3. Test Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "password123"
  }'
```

### 4. Use Token for Protected Routes
```bash
TOKEN="<token_from_login_response>"

curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer $TOKEN"
```

## Database Files

### SQLite
When using SQLite (default), the database file will be created at:
```
backend/health_ai.db
```

**Important:** Add to `.gitignore` to prevent committing the database file:
```
*.db
*.sqlite
*.sqlite3
```

## Troubleshooting

### "database.db is locked" Error
- Close any other connections to the database
- Delete the `.db-journal` file if it exists
- Restart the Flask server

### "Column 'xyz' already exists" Error
- The database schema may have changed
- Backup your database and delete the `.db` file
- Run `init_db.py` again to recreate tables

### Password Not Hashing Correctly
- Ensure `Werkzeug` is installed (`pip install Werkzeug==2.3.7`)
- The password is automatically hashed in the `set_password()` method

### JWT Token Errors
- Ensure `PyJWT` is installed (`pip install PyJWT==2.8.0`)
- Check that `SECRET_KEY` is set in `.env` file
- Token expiration is 24 hours by default (configurable in `auth.py`)

## Production Considerations

1. **Change SECRET_KEY** - Set a strong random key in production
2. **Use PostgreSQL/MySQL** - SQLite is fine for dev, but use robust databases for production
3. **Enable HTTPS** - Always use HTTPS in production
4. **Hash Passwords** - Already implemented, passwords are automatically hashed
5. **Rate Limiting** - Add rate limiting to prevent brute force attacks
6. **CORS Policy** - Update CORS settings for specific domains in production
7. **Environment Variables** - Store sensitive data in environment variables, never hardcode

## Next Steps

1. ✅ Database is set up and running
2. 🔌 Integrate with frontend authentication forms
3. 🔐 Implement role-based access control (if needed)
4. 📊 Add API for medical record analytics
5. 🔍 Implement search/filtering for medical records
6. 📧 Add email verification for new accounts
7. 🔄 Implement password reset functionality

