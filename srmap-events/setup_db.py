import pymysql
from werkzeug.security import generate_password_hash

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1133456@Sumit'

print("Setting up SRMAP Event Management System Database...")

try:
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = connection.cursor()
    
    with open('database.sql', 'r') as file:
        sql_commands = file.read().split(';')
        
    for command in sql_commands:
        if command.strip():
            cursor.execute(command)
            
    db_conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database='srmap_events')
    db_cursor = db_conn.cursor()
    
    password_hash = generate_password_hash("1133456@Sumit")
    
    # Insert Departments
    print("Inserting departments...")
    departments = [
        ('CSE', ),
        ('ECE', ),
        ('ME', ),
        ('CE', ),
        ('EEE', ),
    ]
    for dept in departments:
        db_cursor.execute("SELECT * FROM departments WHERE dept_name=%s", dept)
        if not db_cursor.fetchone():
            db_cursor.execute("INSERT INTO departments (dept_name) VALUES (%s)", dept)
    
    # Insert Organizers
    print("Inserting organizers...")
    organizers = [
        ('Tech Club', ),
        ('Cultural Club', ),
        ('Sports Committee', ),
        ('Academic Association', ),
    ]
    for org in organizers:
        db_cursor.execute("SELECT * FROM organizers WHERE organizer_name=%s", org)
        if not db_cursor.fetchone():
            db_cursor.execute("INSERT INTO organizers (organizer_name) VALUES (%s)", org)
    
    # Dummy Admin
    print("Inserting admin...")
    db_cursor.execute("SELECT * FROM admins WHERE username='admin'")
    if not db_cursor.fetchone():
        db_cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", ('admin', password_hash))
        
    # Get CSE department ID
    db_cursor.execute("SELECT dept_id FROM departments WHERE dept_name='CSE'")
    cse_dept = db_cursor.fetchone()
    cse_dept_id = cse_dept['dept_id'] if cse_dept else None
    
    # Dummy Student
    print("Inserting sample student...")
    db_cursor.execute("SELECT * FROM students WHERE email='student@srmap.edu.in'")
    if not db_cursor.fetchone():
        db_cursor.execute("""
            INSERT INTO students (name, roll_no, email, password, dept_id) 
            VALUES (%s, %s, %s, %s, %s)
        """, ('Sumit Student', 'AP21110010001', 'student@srmap.edu.in', password_hash, cse_dept_id))
        
    # Get Tech Club organizer ID
    db_cursor.execute("SELECT organizer_id FROM organizers WHERE organizer_name='Tech Club'")
    tech_org = db_cursor.fetchone()
    tech_org_id = tech_org['organizer_id'] if tech_org else None
    
    # Dummy Event
    print("Inserting sample event...")
    db_cursor.execute("SELECT * FROM events")
    if not db_cursor.fetchone():
        db_cursor.execute("""
            INSERT INTO events (event_name, description, event_date, event_time, venue, organizer_id, capacity) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, ('Annual Tech Fest', 'Biggest tech festival of the year!', '2026-05-10', '10:00:00', 'Main Auditorium', tech_org_id, 500))
        
    db_conn.commit()
    print("\n✓ Database setup complete!")
    print("✓ Departments: CSE, ECE, ME, CE, EEE")
    print("✓ Organizers: Tech Club, Cultural Club, Sports Committee, Academic Association")
    print("\nTest Credentials:")
    print("Admin - username: admin, password: 1133456@Sumit")
    print("Student - email: student@srmap.edu.in, password: 1133456@Sumit")
    
except Exception as e:
    print(f"Error setting up database: {e}")
finally:
    if 'db_conn' in locals() and db_conn.open:
        db_conn.close()
