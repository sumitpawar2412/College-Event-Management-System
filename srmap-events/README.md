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

#### 1. **Normalization (Enhanced in v2)**
The database follows **3rd Normal Form (3NF)** principles with improved design:

**v2 Improvements:**
- **Eliminated Attribute Redundancy**: Department and Organizer names moved to separate tables
- **Atomic Values**: Each column contains only atomic (indivisible) values
- **No Partial Dependencies**: Non-key attributes depend on the entire primary key
- **No Transitive Dependencies**: Non-key attributes depend only on the primary key
- **Example**: Instead of storing "CSE" in every student record, we store `dept_id` referencing the departments table

#### 2. **Entity-Relationship Model (ER) - Enhanced**
The system is designed using the ER model with clear, normalized relationships:
- **Students** 1:M **Registrations** M:1 **Events**
- **Students** M:1 **Departments** (new in v2)
- **Events** M:1 **Organizers** (new in v2)
- **Notifications** M:1 **Events** (optional link, new in v2)
- **Login_Activity** references both Students and Admins (improved in v2)

**v2 Benefit**: Clearer entity definitions, less data redundancy

#### 3. **Primary Keys (PK)**
- Uniquely identifies each record in a table
- Auto-increment integers used for efficient indexing
- Examples: `student_id`, `event_id`, `dept_id`, `organizer_id`, `admin_id`
- **v2 Addition**: New PKs for departments and organizers tables

#### 4. **Foreign Keys (FK) - Enhanced with Better Constraints**
Maintain **referential integrity** between related tables:
- Prevent orphaned records
- Two types of referential actions in v2:
  - **ON DELETE CASCADE**: Used for "owned" relationships (student registrations, login_activity)
  - **ON DELETE SET NULL**: Used for optional references (student.dept_id, event.organizer_id, notification.event_id)

**Examples**:
- `students.dept_id` → `departments.dept_id` (SET NULL if dept deleted)
- `events.organizer_id` → `organizers.organizer_id` (SET NULL if organizer deleted)
- `registrations.student_id` → `students.student_id` (CASCADE if student deleted)
- `login_activity.student_id` → `students.student_id` (CASCADE if student deleted)

#### 5. **Unique Constraints**
Prevent duplicate entries for critical fields:
- `students.roll_no` - Each student has unique roll number
- `students.email` - Each email is unique
- `admins.username` - Admin usernames must be unique
- `departments.dept_name` - Department names must be unique (v2 new)
- `registrations(student_id, event_id)` - Each student registers once per event

#### 6. **CHECK Constraints (v2 Enhancement)**
Data validation at the database level:
- **login_activity CHECK**: `(student_id IS NOT NULL AND admin_id IS NULL) OR (student_id IS NULL AND admin_id IS NOT NULL)`
  - Ensures login records are either for a student OR admin, never both/neither
  - Type safety at database level

#### 7. **TIMESTAMPS**
Automatic timestamps track when records are created or updated:
- `registrations.reg_date` - When student registered for event
- `notifications.posted_date` - When notification was posted
- `login_activity.login_time` - When user logged in
- **Benefits**: Audit trails, event ordering, security monitoring

#### 8. **Data Integrity**
- **Type Checking**: VARCHAR for text, INT for numbers, DATE/TIME for temporal data
- **NOT NULL Constraints**: Essential fields cannot be empty
- **Default Values**: AUTO_INCREMENT for IDs, CURRENT_TIMESTAMP for dates
- **Referential Integrity**: Foreign keys prevent invalid relationships
- **v2 Improvement**: Better constraint design with CASCADE vs SET NULL options

#### 9. **ACID Properties**
- **Atomicity**: Transactions (e.g., login recording) are all-or-nothing
- **Consistency**: Data always maintains valid state (enforced by constraints)
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

### Table: `departments` (NEW)
```sql
CREATE TABLE departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(50) UNIQUE NOT NULL
);
```
**Purpose**: Stores department information for better normalization
**Fields**:
- `dept_id` - Auto-incremented department ID
- `dept_name` - Unique department name (CSE, ECE, ME, CE, EEE, etc.)

**Sample Data**:
- CSE (Computer Science & Engineering)
- ECE (Electronics & Communication Engineering)
- ME (Mechanical Engineering)
- CE (Civil Engineering)
- EEE (Electrical & Electronics Engineering)

---

### Table: `students` (UPDATED)
```sql
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        ON DELETE SET NULL
);
```
**Purpose**: Stores student profile information
**Changes from v1**: 
- `department` VARCHAR(50) → `dept_id` INT with Foreign Key to `departments` table
- Better normalization: Department names are centralized and not repeated in every student record
**Unique Fields**: `roll_no`, `email`
**Foreign Key**: `dept_id` references `departments.dept_id` with ON DELETE SET NULL (if dept deleted, dept_id becomes NULL)

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
**Security**: Passwords are hashed using Werkzeug PBKDF2

---

### Table: `organizers` (NEW)
```sql
CREATE TABLE organizers (
    organizer_id INT AUTO_INCREMENT PRIMARY KEY,
    organizer_name VARCHAR(100) NOT NULL
);
```
**Purpose**: Stores event organizer information
**Fields**:
- `organizer_id` - Auto-incremented ID
- `organizer_name` - Name of the club/committee organizing events

**Sample Data**:
- Tech Club
- Cultural Club
- Sports Committee
- Academic Association

---

### Table: `events` (UPDATED)
```sql
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(150) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue VARCHAR(100),
    organizer_id INT,
    capacity INT DEFAULT 100,
    FOREIGN KEY (organizer_id) REFERENCES organizers(organizer_id)
        ON DELETE SET NULL
);
```
**Purpose**: Stores event information
**Changes from v1**: 
- `organizer` VARCHAR(100) → `organizer_id` INT with Foreign Key to `organizers` table
- Better normalization: Organizer names are stored once, referenced by ID
**Foreign Key**: `organizer_id` references `organizers.organizer_id` with ON DELETE SET NULL
**Key Fields**:
- `event_date` - When the event occurs
- `event_time` - Time of the event
- `capacity` - Maximum registrations allowed (default 100)

---

### Table: `registrations`
```sql
CREATE TABLE registrations (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
        ON DELETE CASCADE,
    UNIQUE(student_id, event_id)
);
```
**Purpose**: Junction table linking students to events (Many-to-Many relationship)
**Important Features**:
- **UNIQUE Constraint**: `(student_id, event_id)` - Each student registers only once per event
- **Referential Integrity**: Foreign keys ensure valid student and event IDs
- **ON DELETE CASCADE**: Auto-delete registrations if student/event is deleted
- **Automatic Timestamp**: Records exact registration date/time

---

### Table: `notifications` (UPDATED)
```sql
CREATE TABLE notifications (
    notice_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    event_id INT NULL,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
        ON DELETE SET NULL
);
```
**Purpose**: Stores system announcements and event-specific notifications
**Changes from v1**: 
- Added `event_id` INT NULL field
- Added Foreign Key to link notifications to specific events
- Allows event-specific notifications (event cancellations, updates, etc.)
**Key Fields**:
- `title` - Notification headline
- `message` - Full notification text
- `event_id` - Optional link to an event (NULL for general announcements)
- `posted_date` - When notification was posted

---

### Table: `login_activity` (UPDATED)
```sql
CREATE TABLE login_activity (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NULL,
    admin_id INT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (student_id IS NOT NULL AND admin_id IS NULL) OR
        (student_id IS NULL AND admin_id IS NOT NULL)
    ),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admins(admin_id)
        ON DELETE CASCADE
);
```
**Purpose**: Audit trail for tracking user logins
**Changes from v1**: 
- `user_id` INT + `role` VARCHAR → Separate `student_id` and `admin_id` columns
- Added CHECK constraint to ensure data integrity
- Added Foreign Keys for both student and admin logins
**Important Features**:
- **CHECK Constraint**: Ensures exactly ONE of `student_id` or `admin_id` is NOT NULL
  - Either a student logged in (student_id has value, admin_id is NULL)
  - Or an admin logged in (admin_id has value, student_id is NULL)
  - Never both, never neither
- **Foreign Keys**: Maintain referential integrity
- **ON DELETE CASCADE**: Remove login records if user account is deleted
- **Automatic Timestamp**: Records exact login time

---

## Database Normalization Improvements

### Version 1 → Version 2 Changes

| Aspect | v1 | v2 | Benefit |
|--------|----|----|---------|
| **Departments** | VARCHAR field in students | Separate `departments` table | Eliminates data redundancy, easier updates |
| **Organizers** | VARCHAR field in events | Separate `organizers` table | Eliminates data redundancy, consistent naming |
| **Student-Dept Link** | Direct string storage | Foreign Key relationship | Data integrity, enforces valid departments |
| **Event-Organizer Link** | Direct string storage | Foreign Key relationship | Data integrity, enforces valid organizers |
| **Login Tracking** | Single `user_id` + `role` | Separate `student_id`/`admin_id` | Type safety, CHECK constraint, clearer intent |
| **Notifications** | Generic announcements only | Can link to events | Better context, event-specific alerts |

### 3NF Compliance

The new schema strictly follows **Third Normal Form (3NF)**:

1. **First Normal Form (1NF)**: All values are atomic (no repeating groups)
2. **Second Normal Form (2NF)**: No partial dependencies on composite keys
3. **Third Normal Form (3NF)**: No transitive dependencies
   - Student depends only on student_id
   - Department info depends on dept_id (not embedded in students)
   - Event organizer depends on organizer_id (not embedded in events)

---

## Relationship Diagram

```
┌──────────────────┐
│  departments     │
├──────────────────┤
│ dept_id ◄────────┼────┐
│ dept_name        │    │
└──────────────────┘    │ Foreign Key
                        │
┌──────────────┐        │
│   students   │        │
├──────────────┤        │
│ student_id   │◄───┐   │
│ name         │    │   │
│ roll_no      │    │   │
│ email        │    │   │
│ password     │    │   │
│ dept_id ─────┼────┘───┘
└──────────────┘

                        ┌─────────────────┐
                        │  organizers     │
                        ├─────────────────┤
                        │ organizer_id ◄──┼────┐
                        │ organizer_name  │    │
                        └─────────────────┘    │
                                               │ Foreign Key
┌──────────────┐                               │
│    events    │                               │
├──────────────┤                               │
│ event_id  ◄──┼────────┐                      │
│ event_name   │        │                      │
│ description  │        │                      │
│ event_date   │        │                      │
│ event_time   │        │  Foreign Key         │
│ venue        │        │                      │
│ organizer_id ─────────┴──────────────────────┘
│ capacity     │        
└──────────────┘        
       ▲                 
       │ Foreign Key    
       │                 
  ┌────┴──────────────┐
  │ registrations     │
  ├───────────────────┤
  │ reg_id            │
  │ student_id ───────┼──────► students
  │ event_id ─────────┼──────► events
  │ reg_date          │
  └───────────────────┘

┌────────────────────────┐
│   notifications        │
├────────────────────────┤
│ notice_id              │
│ title                  │
│ message                │
│ event_id ──────────────┼──────► events (optional)
│ posted_date            │
└────────────────────────┘

┌────────────────────┐
│   admins           │
├────────────────────┤
│ admin_id  ◄────────┼────┐
│ username           │    │ Foreign Key
│ password           │    │
└────────────────────┘    │

┌────────────────────────────┐
│ login_activity             │
├────────────────────────────┤
│ login_id                   │
│ student_id ────────────────┼──────► students (NULL if admin)
│ admin_id ──────────────────┼──────► admins (NULL if student)
│ login_time                 │
│ CHECK: Only one is NOT NULL│
└────────────────────────────┘
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

### 2. **Normalization (3NF) - v2 Enhanced**
- ✅ **1NF**: Atomic values only (no repeating groups)
- ✅ **2NF**: No partial dependencies on composite keys
- ✅ **3NF**: No transitive dependencies
  - v2: Department info is in separate table, not embedded in students
  - v2: Organizer info is in separate table, not embedded in events

### 3. **Relationships (Improved in v2)**
- ✅ **One-to-Many (1:M)**: 
  - Student → Registrations
  - Department → Students
  - Organizer → Events
- ✅ **Many-to-Many (M:M)**: Students ↔ Events (via Registrations table)
- ✅ **Optional One-to-Many**: Events ← Notifications

### 4. **Constraints (Enhanced in v2)**
- ✅ **PRIMARY KEY**: Unique row identification for all tables
- ✅ **FOREIGN KEY**: Referential integrity
  - v2: Uses CASCADE for "owned" relationships
  - v2: Uses SET NULL for optional relationships
- ✅ **UNIQUE**: Prevent duplicates (roll_no, email, username, dept_name)
- ✅ **CHECK** (v2 new): login_activity can only have student_id OR admin_id, not both
- ✅ **NOT NULL**: Required fields
- ✅ **DEFAULT**: Automatic values (CURRENT_TIMESTAMP, 100)

### 5. **Indexing** (Implicit & Efficient)
- PRIMARY KEYs are automatically indexed for fast lookups
- Fast queries by student_id, event_id, admin_id, dept_id, organizer_id
- UNIQUE constraint fields automatically indexed
- Email and roll_no UNIQUE indexes enable fast login lookups

### 6. **Data Redundancy Elimination (v2 Focus)**
- **Before**: Department name stored in every student record
- **After**: Stored once in departments table, referenced by ID
- **Before**: Organizer name stored in every event record
- **After**: Stored once in organizers table, referenced by ID
- **Result**: Better normalization, easier updates, less storage

### 7. **Referential Integrity Strategy (v2 Improved)**
- **Owned Relationships** (ON DELETE CASCADE):
  - Registrations owned by Students/Events
  - Login_activity owned by Student/Admin
  - If parent deleted, child records automatically deleted
  
- **Optional Relationships** (ON DELETE SET NULL):
  - Student may not have Department
  - Event may not have Organizer
  - Notification may not link to Event
  - If parent deleted, foreign key becomes NULL (data preserved)

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
