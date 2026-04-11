# SRMAP Event Management System

A comprehensive college event management web application built with Flask and MySQL. This system enables students to discover, register for events, and allows administrators to manage events efficiently.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Database Design & DBMS Concepts](#database-design--dbms-concepts)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [How to Run](#how-to-run)
7. [Features](#features)
8. [Database Schema](#database-schema)
9. [API Endpoints](#api-endpoints)
10. [User Roles](#user-roles)
11. [Security Features](#security-features)
12. [File Descriptions](#file-descriptions)

---

## Project Overview

The **SRMAP Event Management System** is a web-based platform for managing college events. Students can:
- Register for events
- View upcoming events
- Track their registrations
- Receive notifications about events

Administrators can:
- Create and manage events
- Monitor event registrations
- Manage notifications
- View user activity logs

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask 3.0.0 (Python Web Framework) |
| **Database** | MySQL (Relational Database) |
| **Database Driver** | PyMySQL 1.1.0 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Security** | Werkzeug (Password Hashing & HTTPS utilities) |
| **Encryption** | Cryptography library |

---

## Database Design & DBMS Concepts

### Core DBMS Principles Used

#### 1. **Normalization**
The database follows **3rd Normal Form (3NF)** principles:
- **Atomic Values**: Each column contains only atomic (indivisible) values
- **No Partial Dependencies**: Non-key attributes depend on the entire primary key
- **No Transitive Dependencies**: Non-key attributes depend only on the primary key

#### 2. **Entity-Relationship Model (ER)**
The system is designed using the ER model with clear relationships:
- **Students** 1:M **Registrations** M:1 **Events**
- **Admins** create and manage **Events**
- **Notifications** inform users about **Events**

#### 3. **Primary Keys (PK)**
- Uniquely identifies each record in a table
- Auto-increment integers used for efficient indexing
- Examples: `student_id`, `event_id`, `admin_id`

#### 4. **Foreign Keys (FK)**
- Maintain **referential integrity** between related tables
- Prevent orphaned records
- ON DELETE CASCADE ensures data consistency
- Example: `registrations.student_id` → `students.student_id`

#### 5. **Unique Constraints**
- Prevent duplicate entries for critical fields
- Examples:
  - `students.roll_no` - Each student has unique roll number
  - `students.email` - Each email is unique
  - `admins.username` - Admin usernames must be unique
  - `registrations(student_id, event_id)` - Each student can register once per event

#### 6. **TIMESTAMPS**
- **Automatic timestamps** track when records are created or updated
- Examples: `registrations.reg_date`, `notifications.posted_date`, `login_activity.login_time`
- Useful for audit trails and event ordering

#### 7. **Data Integrity**
- **Type Checking**: VARCHAR for text, INT for numbers, DATE/TIME for temporal data
- **NOT NULL Constraints**: Essential fields cannot be empty
- **Default Values**: AUTO_INCREMENT for IDs, CURRENT_TIMESTAMP for dates
- **ON DELETE CASCADE**: When a student is deleted, all their registrations are automatically deleted

#### 8. **ACID Properties**
- **Atomicity**: Transactions (e.g., login recording) are all-or-nothing
- **Consistency**: Data always maintains valid state
- **Isolation**: Multiple transactions don't interfere
- **Durability**: Committed data persists after COMMIT

---

## Project Structure

```
srmap-events/
│
├── app.py                      # Main Flask application with routes
├── database.sql                # Database schema and table definitions
├── setup_db.py                 # Initial database setup script
├── patch_db.py                 # Database maintenance/patching script
├── add_admin.py                # Script to add new admin users
├── requirements.txt            # Python dependencies
│
├── templates/                  # HTML templates (Flask Jinja2)
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Student registration page
│   ├── dashboard.html         # Student dashboard
│   ├── events.html            # Events listing page
│   └── admin.html             # Admin dashboard
│
├── static/                    # Static files
│   ├── css/
│   │   └── style.css          # Custom CSS styling
│   ├── images/                # Image assets
│   └── js/
│       └── main.js            # JavaScript functionality
│
└── report/                    # Project reports and documentation
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server 5.7+
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd srmap-events
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Database Credentials
Edit `app.py`, `setup_db.py`, `patch_db.py`, and `add_admin.py`:
```python
DB_HOST = 'localhost'      # Your MySQL server address
DB_USER = 'root'          # Your MySQL username
DB_PASSWORD = 'your_password'  # Your MySQL password
```

### Step 4: Initialize the Database
Run the setup script to create tables and insert sample data:
```bash
python setup_db.py
```

Output should show:
```
Setting up SRMAP Event Management System Database...
Database setup complete! Fake user and admin injected.
Admin credentials: admin / 1133456@Sumit
Student credentials: student@srmap.edu.in / 1133456@Sumit
```

---

## How to Run

### Start the Flask Application
```bash
python app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
```

### Access the Application
Open your browser and go to: **http://localhost:5000**

### Test Credentials (after setup_db.py)
**Admin Login:**
- Username: `admin`
- Password: `1133456@Sumit`

**Student Login:**
- Email: `student@srmap.edu.in`
- Password: `1133456@Sumit`

---

## Features

### For Students
✅ User Registration with secure password hashing
✅ Event Discovery - Browse upcoming events
✅ Event Registration - Register for events
✅ Dashboard - View registered events
✅ Notifications - Receive event updates
✅ Secure Authentication with session management

### For Administrators
✅ Admin Login with role-based access
✅ Event Management - Create, update, delete events
✅ Event Details - Set venue, date, time, capacity
✅ Registration Management - Monitor student registrations
✅ Notifications - Send announcements to students
✅ User Activity Tracking - View login history
✅ Admin Management - Add new admin users

---

## Database Schema

### Table: `students`
```sql
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(50)
);
```
**Purpose**: Stores student profile information
**Unique Fields**: `roll_no`, `email` (prevent duplicates)

---

### Table: `admins`
```sql
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```
**Purpose**: Stores admin credentials
**Unique Fields**: `username`
**Security**: Passwords are hashed using Werkzeug

---

### Table: `events`
```sql
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(150) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue VARCHAR(100),
    organizer VARCHAR(100),
    capacity INT DEFAULT 100
);
```
**Purpose**: Stores event information
**Key Fields**:
- `event_date` - When the event occurs
- `capacity` - Maximum number of registrations
- `organizer` - Person/club organizing the event

---

### Table: `registrations`
```sql
CREATE TABLE registrations (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    UNIQUE(student_id, event_id)
);
```
**Purpose**: Links students to events (Junction/Bridge Table)
**Important Features**:
- **UNIQUE Constraint**: `(student_id, event_id)` - Each student can register only once per event
- **Foreign Keys**: Maintain referential integrity
- **ON DELETE CASCADE**: Auto-delete registrations if student/event is deleted
- **Automatic Timestamp**: Records registration date/time

---

### Table: `notifications`
```sql
CREATE TABLE notifications (
    notice_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Purpose**: Stores announcements and notifications for users
**Key Fields**:
- `title` - Notification headline
- `message` - Full notification text
- `posted_date` - When notification was posted

---

### Table: `login_activity`
```sql
CREATE TABLE login_activity (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role VARCHAR(20),
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Purpose**: Audit trail for user logins
**Useful For**:
- Security monitoring
- User behavior analysis
- Tracking active admins vs students
- Identifying suspicious activity

---

## Relationship Diagram

```
┌──────────────┐
│   students   │
├──────────────┤
│ student_id◄──┼────┐
│ name         │    │
│ roll_no      │    │  Foreign Key
│ email        │    │
│ password     │    │
│ department   │    │
└──────────────┘    │
                    │
              ┌─────▼──────────┐
              │ registrations  │
              ├────────────────┤
              │ reg_id         │
              │ student_id ────┼──────► students
              │ event_id ──────┼──────► events
              │ reg_date       │
              └────────────────┘

┌──────────────┐
│    events    │
├──────────────┤
│ event_id  ◄──┼────────────────────┐
│ event_name   │                    │
│ description  │              Foreign Key
│ event_date   │                    │
│ event_time   │    ┌───────────────┘
│ venue        │    │
│ organizer    │    │
│ capacity     │    │
└──────────────┘    │

┌──────────────┐
│    admins    │
├──────────────┤
│ admin_id     │
│ username     │◄── Creates and manages events
│ password     │
└──────────────┘

┌────────────────────┐
│  notifications     │
├────────────────────┤
│ notice_id          │
│ title              │
│ message            │
│ posted_date        │
└────────────────────┘

┌────────────────────┐
│ login_activity     │
├────────────────────┤
│ login_id           │
│ user_id            │◄── References both students and admins
│ role               │
│ login_time         │
└────────────────────┘
```

---

## API Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/` | Home page with 3 upcoming events | No |
| GET/POST | `/login` | User login (student/admin) | No |
| GET/POST | `/register` | Student registration | No |
| GET | `/dashboard` | Student dashboard with registered events | ✅ Student |
| GET/POST | `/events` | Browse all events | ✅ Student |
| GET/POST | `/register_event/<event_id>` | Register for an event | ✅ Student |
| GET/POST | `/admin` | Admin dashboard | ✅ Admin |
| GET/POST | `/admin/create_event` | Create new event | ✅ Admin |
| GET | `/logout` | Logout current user | ✅ Both |

---

## User Roles

### 1. **Student Role**
- **Access**: Dashboard, Events, Registrations, Notifications
- **Permissions**: 
  - View upcoming events
  - Register for events
  - View own registrations
  - Cannot modify events

### 2. **Admin Role**
- **Access**: Full admin panel
- **Permissions**:
  - Create/Update/Delete events
  - View all registrations
  - Send notifications
  - Add other admins
  - View login activity

### 3. **Guest (No Role)**
- **Access**: Home page, Login, Registration page only
- **Permissions**: None (read-only homepage)

---

## Security Features

### 1. **Password Hashing**
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Passwords are hashed using PBKDF2
hashed = generate_password_hash("plain_password")
```
- Uses PBKDF2 algorithm with 200+ iterations
- Passwords never stored in plain text
- Checked using `check_password_hash()` during login

### 2. **Session Management**
```python
session['user_id'] = student_id  # Session token
```
- Flask sessions use secure cookies
- `login_required` decorator protects routes
- `admin_required` decorator restricts admin access

### 3. **SQL Injection Prevention**
```python
cursor.execute("SELECT * FROM students WHERE email = %s", (email_or_user,))
```
- Using parameterized queries (`%s` placeholders)
- PyMySQL automatically escapes dangerous characters

### 4. **Referential Integrity**
- Foreign keys prevent invalid data relationships
- ON DELETE CASCADE maintains data consistency
- UNIQUE constraints prevent duplicate critical fields

### 5. **Unique Constraints**
- Prevents duplicate emails, usernames, roll numbers
- Prevents duplicate registrations (student + event)

---

## File Descriptions

### `app.py` - Main Application
The Flask application containing all routes and business logic.

**Key Functions**:
- `get_db_connection()` - Creates MySQL connection
- `login_required()` - Decorator to protect student routes
- `admin_required()` - Decorator to protect admin routes
- Routes for login, registration, events, registrations

**Database Operations**:
- Authenticate users (students & admins)
- Register students for events
- Fetch upcoming events
- Record login activity
- Manage event registrations

---

### `database.sql` - Database Schema
Contains all CREATE TABLE statements to initialize the database structure.

**Tables Created**:
1. students
2. admins
3. events
4. registrations
5. notifications
6. login_activity

---

### `setup_db.py` - Initial Setup Script
Initializes the database with tables and sample data.

**What it does**:
1. Creates database `srmap_events`
2. Creates all 6 tables from `database.sql`
3. Inserts test data:
   - Default admin: username `admin`
   - Default student: email `student@srmap.edu.in`
   - Sample event: `Annual Tech Fest`

**Run Once**: After MySQL is set up

---

### `add_admin.py` - Admin Creation Script
Interactive script to add new administrator accounts.

**Usage**:
```bash
python add_admin.py
# Follow prompts to enter new admin username and password
```

**Features**:
- Prompts for username and password
- Hashes password securely
- Prevents duplicate usernames
- Closes connection safely

---

### `patch_db.py` - Database Maintenance
Used for database updates and migrations.

**Current Functionality**:
- Creates `login_activity` table if missing
- Updates admin credentials
- Used when schema changes occur

**Can be extended for**:
- Database version upgrades
- Adding columns to existing tables
- Data migrations
- Fixing schema issues

---

### `requirements.txt` - Python Dependencies
Lists all Python packages required to run the project.

```
Flask==3.0.0           # Web framework
PyMySQL==1.1.0        # MySQL database driver
Werkzeug==3.0.1       # Password hashing & WSGI utilities
cryptography          # Encryption utilities
```

---

## Key DBMS Concepts Implemented

### 1. **ACID Properties**
- ✅ **Atomicity**: Login activity recorded atomically with session
- ✅ **Consistency**: Constraints enforce valid data
- ✅ **Isolation**: Transaction-based operations
- ✅ **Durability**: MySQL persistence

### 2. **Normalization (3NF)**
- ✅ **1NF**: Atomic values only
- ✅ **2NF**: No partial dependencies (no non-key dependency on part of composite key)
- ✅ **3NF**: No transitive dependencies

### 3. **Relationships**
- ✅ **One-to-Many (1:M)**: Student → Registrations
- ✅ **Many-to-Many (M:M)**: Students ↔ Events (via Registrations)
- ✅ **One-to-One (1:1)**: Student → Department implicitly

### 4. **Constraints**
- ✅ **PRIMARY KEY**: Unique row identification
- ✅ **FOREIGN KEY**: Referential integrity
- ✅ **UNIQUE**: Prevent duplicates
- ✅ **NOT NULL**: Required fields
- ✅ **DEFAULT**: Automatic values

### 5. **Indexing** (Implicit)
- PRIMARY KEYs are automatically indexed
- Fast lookups by student_id, event_id, admin_id
- Email and roll_no UNIQUE indexes for fast login

---

## Troubleshooting

### Database Connection Errors
```
Error: Access denied for user 'root'@'localhost'
```
**Solution**: Check DB_PASSWORD in app.py matches your MySQL root password

### Port Already in Use
```
Address already in use
```
**Solution**: 
```bash
# Kill the process using port 5000
# Windows: netstat -ano | findstr :5000
# Or use a different port: flask run --port 5001
```

### Table Doesn't Exist
```
Table 'srmap_events.events' doesn't exist
```
**Solution**: Run `python setup_db.py` to initialize database

### Duplicate Key Error
```
IntegrityError: Duplicate entry
```
**Solution**: Check UNIQUE constraints - roll_no and email must be unique

---

## Future Enhancements

1. **Email Notifications** - Send event reminders via email
2. **QR Code Check-in** - Track student attendance with QR codes
3. **Event Capacity Management** - Auto-close registration when full
4. **Payment Integration** - Handle paid events
5. **Advanced Search** - Filter events by category, date range
6. **User Profiles** - Profile pictures, social media links
7. **Ratings & Reviews** - Students review events
8. **Analytics Dashboard** - Chart trends, popular events
9. **Mobile App** - React Native or Flutter version
10. **API Rate Limiting** - Prevent abuse

---

## Contributing

To contribute to this project:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## License

This project is part of a college DBMS course project.

---

## Contact & Support

For issues or questions:
- Review this README documentation
- Check the database schema diagrams
- Run `setup_db.py` to reset the database
- Verify MySQL credentials in configuration files

---

## Summary

The **SRMAP Event Management System** demonstrates key DBMS concepts:
- **Relational database design** with proper normalization
- **Entity relationships** using foreign keys
- **Data integrity** through constraints
- **Secure password storage** with hashing
- **Session-based authentication**
- **SQL query optimization** with indexes
- **Transaction safety** with atomic operations

This is a practical implementation suitable for college-level DBMS projects and real-world event management scenarios.
