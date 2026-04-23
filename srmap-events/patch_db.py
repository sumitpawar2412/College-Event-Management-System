import pymysql
from werkzeug.security import generate_password_hash

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1133456@Sumit'

try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database='srmap_events')
    cursor = conn.cursor()

    # Ensure all required tables exist
    print("Checking database schema...")
    
    # Check and create departments table if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            dept_id INT AUTO_INCREMENT PRIMARY KEY,
            dept_name VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    
    # Check and create organizers table if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS organizers (
            organizer_id INT AUTO_INCREMENT PRIMARY KEY,
            organizer_name VARCHAR(100) NOT NULL
        );
    """)
    
    # Add dept_id column to students if it doesn't exist
    cursor.execute("SHOW COLUMNS FROM students LIKE 'dept_id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE students ADD COLUMN dept_id INT")
        cursor.execute("""
            ALTER TABLE students ADD CONSTRAINT fk_dept 
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL
        """)
        print("✓ Added dept_id column to students table")
    
    # Update events table to use organizer_id instead of organizer
    cursor.execute("SHOW COLUMNS FROM events LIKE 'organizer_id'")
    if not cursor.fetchone():
        # Check if old organizer column exists
        cursor.execute("SHOW COLUMNS FROM events LIKE 'organizer'")
        if cursor.fetchone():
            cursor.execute("ALTER TABLE events DROP COLUMN organizer")
        cursor.execute("ALTER TABLE events ADD COLUMN organizer_id INT")
        cursor.execute("""
            ALTER TABLE events ADD CONSTRAINT fk_organizer 
            FOREIGN KEY (organizer_id) REFERENCES organizers(organizer_id) ON DELETE SET NULL
        """)
        print("✓ Updated events table with organizer_id")
    
    # Update login_activity table with new structure
    cursor.execute("SHOW COLUMNS FROM login_activity LIKE 'student_id'")
    if not cursor.fetchone():
        # Drop old columns if they exist
        cursor.execute("SHOW COLUMNS FROM login_activity LIKE 'user_id'")
        if cursor.fetchone():
            cursor.execute("ALTER TABLE login_activity DROP COLUMN user_id")
        cursor.execute("SHOW COLUMNS FROM login_activity LIKE 'role'")
        if cursor.fetchone():
            cursor.execute("ALTER TABLE login_activity DROP COLUMN role")
        
        # Add new columns
        cursor.execute("ALTER TABLE login_activity ADD COLUMN student_id INT")
        cursor.execute("ALTER TABLE login_activity ADD COLUMN admin_id INT")
        cursor.execute("""
            ALTER TABLE login_activity ADD CONSTRAINT fk_login_student 
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
        """)
        cursor.execute("""
            ALTER TABLE login_activity ADD CONSTRAINT fk_login_admin 
            FOREIGN KEY (admin_id) REFERENCES admins(admin_id) ON DELETE CASCADE
        """)
        print("✓ Updated login_activity table structure")
    
    # Add event_id to notifications if it doesn't exist
    cursor.execute("SHOW COLUMNS FROM notifications LIKE 'event_id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE notifications ADD COLUMN event_id INT")
        cursor.execute("""
            ALTER TABLE notifications ADD CONSTRAINT fk_notification_event 
            FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE SET NULL
        """)
        print("✓ Added event_id column to notifications table")
    
    conn.commit()
    print("\n✓ Database patched successfully! Schema is up to date.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
