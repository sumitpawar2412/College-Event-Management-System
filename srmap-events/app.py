from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_srmap'

# Database Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mohit@852006')
DB_NAME = 'srmap_events'

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


def table_exists(cursor, table_name):
    cursor.execute("SHOW TABLES LIKE %s", (table_name,))
    return cursor.fetchone() is not None


def column_exists(cursor, table_name, column_name):
    if not table_exists(cursor, table_name):
        return False
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE %s", (column_name,))
    return cursor.fetchone() is not None


def uses_normalized_event_schema(cursor):
    return table_exists(cursor, 'organizers') and column_exists(cursor, 'events', 'organizer_id')


def fetch_event_rows(cursor, search_text=None, limit=None):
    normalized_schema = uses_normalized_event_schema(cursor)

    if normalized_schema:
        query = """
            SELECT e.*, COALESCE(o.organizer_name, '') AS organizer
            FROM events e
            LEFT JOIN organizers o ON e.organizer_id = o.organizer_id
        """
    else:
        query = """
            SELECT e.*
            FROM events e
        """

    params = []
    if search_text:
        if normalized_schema:
            query += """
                WHERE e.event_name LIKE %s
                   OR e.description LIKE %s
                   OR e.venue LIKE %s
                   OR o.organizer_name LIKE %s
            """
        else:
            query += """
                WHERE e.event_name LIKE %s
                   OR e.description LIKE %s
                   OR e.venue LIKE %s
                   OR e.organizer LIKE %s
            """
        sv = f"%{search_text}%"
        params.extend([sv, sv, sv, sv])

    query += " ORDER BY e.event_date ASC"
    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)

    cursor.execute(query, tuple(params))
    return cursor.fetchall()


def fetch_registered_events(cursor, student_id):
    if uses_normalized_event_schema(cursor):
        cursor.execute("""
            SELECT e.*, r.reg_date, COALESCE(o.organizer_name, '') AS organizer
            FROM events e
            LEFT JOIN organizers o ON e.organizer_id = o.organizer_id
            JOIN registrations r ON e.event_id = r.event_id
            WHERE r.student_id = %s
            ORDER BY e.event_date ASC
        """, (student_id,))
    else:
        cursor.execute("""
            SELECT e.*, r.reg_date
            FROM events e
            JOIN registrations r ON e.event_id = r.event_id
            WHERE r.student_id = %s
            ORDER BY e.event_date ASC
        """, (student_id,))

    return cursor.fetchall()


def get_or_create_organizer_id(cursor, organizer_name):
    cursor.execute("SELECT organizer_id FROM organizers WHERE organizer_name = %s", (organizer_name,))
    row = cursor.fetchone()
    if row:
        return row['organizer_id']

    cursor.execute("INSERT INTO organizers (organizer_name) VALUES (%s)", (organizer_name,))
    return cursor.lastrowid


def record_login_activity(cursor, user_id, role):
    try:
        has_admin_id = column_exists(cursor, 'login_activity', 'admin_id')
        has_student_id = column_exists(cursor, 'login_activity', 'student_id')

        if role == 'admin' and has_admin_id:
            cursor.execute("INSERT INTO login_activity (admin_id) VALUES (%s)", (user_id,))
            return

        if role == 'student' and has_student_id:
            cursor.execute("INSERT INTO login_activity (student_id) VALUES (%s)", (user_id,))
            return

        cursor.execute("INSERT INTO login_activity (user_id, role) VALUES (%s, %s)", (user_id, role))
    except Exception:
        # Login should not fail only because activity logging schema differs.
        pass

# Decorators for auth
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and 'admin_id' not in session:
            flash("Please log in to access this page.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash("Admin access required.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        upcoming_events = fetch_event_rows(cursor, limit=3)
        conn.close()
        return render_template('index.html', events=upcoming_events)
    except Exception as e:
        print(f"Error fetching front page events: {e}")
        return render_template('index.html', events=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_user = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if Admin
        cursor.execute("SELECT * FROM admins WHERE username = %s", (email_or_user,))
        admin = cursor.fetchone()
        if admin and check_password_hash(admin['password'], password):
            session['admin_id'] = admin['admin_id']
            session['username'] = admin['username']
            session['role'] = 'admin'
            record_login_activity(cursor, admin['admin_id'], 'admin')
            conn.commit()
            flash("Logged in successfully as Admin.", "success")
            conn.close()
            return redirect(url_for('admin_dashboard'))
            
        # Check if Student
        cursor.execute("SELECT * FROM students WHERE email = %s", (email_or_user,))
        student = cursor.fetchone()
        if student and check_password_hash(student['password'], password):
            session['user_id'] = student['student_id']
            session['name'] = student['name']
            session['role'] = 'student'
            record_login_activity(cursor, student['student_id'], 'student')
            conn.commit()
            flash("Logged in successfully.", "success")
            conn.close()
            return redirect(url_for('dashboard'))
            
        conn.close()
        flash("Invalid credentials.", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        email = request.form['email']
        password = request.form['password']
        dept_id = request.form.get('dept_id')
        
        hashed_pw = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check for duplicates
        cursor.execute("SELECT * FROM students WHERE email=%s OR roll_no=%s", (email, roll_no))
        existing_student = cursor.fetchone()
        if existing_student:
            flash("Email or Roll Number already registered.", "danger")
            conn.close()
            return redirect(url_for('register'))
            
        try:
            cursor.execute("""
                INSERT INTO students (name, roll_no, email, password, dept_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (name, roll_no, email, hashed_pw, dept_id if dept_id else None))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error registering user: {e}", "danger")
        finally:
            conn.close()
    
    # Get departments for dropdown
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments ORDER BY dept_name ASC")
        departments = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error fetching departments: {e}")
        departments = []
            
    return render_template('register.html', departments=departments)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

@app.route('/events')
def events():
    search = request.args.get('search', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    all_events = fetch_event_rows(cursor, search_text=search)
    conn.close()
    return render_template('events.html', events=all_events, search=search)

@app.route('/register_event/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    if session.get('role') != 'student':
        flash("Only students can register for events.", "danger")
        return redirect(url_for('events'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check duplicate
        cursor.execute("SELECT * FROM registrations WHERE student_id=%s AND event_id=%s", (user_id, event_id))
        if cursor.fetchone():
            flash("You are already registered for this event.", "warning")
            return redirect(url_for('dashboard'))
            
        # Check capacity
        cursor.execute("SELECT capacity FROM events WHERE event_id=%s", (event_id,))
        event = cursor.fetchone()
        if not event:
            flash("Event not found.", "danger")
            return redirect(url_for('events'))
            
        cursor.execute("SELECT COUNT(*) as count FROM registrations WHERE event_id=%s", (event_id,))
        reg_count = cursor.fetchone()['count']
        
        if reg_count >= event['capacity']:
            flash("Sorry, this event is fully booked.", "danger")
            return redirect(url_for('events'))
            
        cursor.execute("INSERT INTO registrations (student_id, event_id) VALUES (%s, %s)", (user_id, event_id))
        conn.commit()
        flash("Successfully registered for the event!", "success")
    except Exception as e:
        flash("Registration failed.", "danger")
    finally:
        conn.close()
        
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('admin_dashboard'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user profile with department info
    if table_exists(cursor, 'departments') and column_exists(cursor, 'students', 'dept_id'):
        cursor.execute("""
            SELECT s.*, d.dept_name AS department
            FROM students s
            LEFT JOIN departments d ON s.dept_id = d.dept_id
            WHERE s.student_id = %s
        """, (user_id,))
    else:
        cursor.execute("SELECT * FROM students WHERE student_id=%s", (user_id,))
    student = cursor.fetchone()
    
    # Get registered events
    registered_events = fetch_registered_events(cursor, user_id)
    
    conn.close()
    return render_template('dashboard.html', student=student, events=registered_events)

@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Overview stats
    cursor.execute("SELECT COUNT(*) as scount FROM students")
    students_count = cursor.fetchone()['scount']
    
    cursor.execute("SELECT COUNT(*) as ecount FROM events")
    events_count = cursor.fetchone()['ecount']
    
    all_events = fetch_event_rows(cursor)
    
    # Enhance events with registration counts
    for event in all_events:
        cursor.execute("SELECT COUNT(*) as count FROM registrations WHERE event_id=%s", (event['event_id'],))
        event['reg_count'] = cursor.fetchone()['count']
        
    cursor.execute("SELECT * FROM students LIMIT 10") # Just showing 10 recent
    recent_students = cursor.fetchall()
    
    conn.close()
    return render_template('admin.html', 
                           scount=students_count, ecount=events_count, 
                           events=all_events, students=recent_students)

@app.route('/admin/event/add', methods=['POST'])
@admin_required
def add_event():
    name = request.form['event_name']
    desc = request.form['description']
    date = request.form['event_date']
    time = request.form['event_time']
    venue = request.form['venue']
    organizer = request.form.get('organizer', '').strip()
    capacity = int(request.form['capacity'])
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if uses_normalized_event_schema(cursor):
            organizer_id = get_or_create_organizer_id(cursor, organizer or 'Unknown Organizer')
            cursor.execute("""
                INSERT INTO events (event_name, description, event_date, event_time, venue, organizer_id, capacity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, desc, date, time, venue, organizer_id, capacity))
        else:
            cursor.execute("""
                INSERT INTO events (event_name, description, event_date, event_time, venue, organizer, capacity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, desc, date, time, venue, organizer, capacity))
        conn.commit()
        flash("Event added successfully.", "success")
    except Exception as e:
        flash(f"Error adding event: {e}", "danger")
    finally:
        conn.close()
        
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/add', methods=['POST'])
@admin_required
def add_admin():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not username:
        flash("Admin username is required.", "danger")
        return redirect(url_for('admin_dashboard'))

    if len(password) < 6:
        flash("Password must be at least 6 characters long.", "danger")
        return redirect(url_for('admin_dashboard'))

    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for('admin_dashboard'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT admin_id FROM admins WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("Username already exists. Please choose another one.", "warning")
            return redirect(url_for('admin_dashboard'))

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO admins (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        flash(f"Admin '{username}' added successfully.", "success")
    except Exception as e:
        flash(f"Error adding admin: {e}", "danger")
    finally:
        conn.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/event/delete/<int:event_id>', methods=['POST'])
@admin_required
def delete_event(event_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE event_id=%s", (event_id,))
        conn.commit()
        flash("Event deleted successfully.", "success")
    except Exception as e:
        flash("Error deleting event.", "danger")
    finally:
        conn.close()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
