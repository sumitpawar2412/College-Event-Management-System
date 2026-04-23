from pathlib import Path
import os

import pymysql
from werkzeug.security import generate_password_hash

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

print("Setting up SRMAP Event Management System Database...")

try:
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = connection.cursor()
    
    sql_path = Path(__file__).resolve().with_name('database.sql')
    with sql_path.open('r', encoding='utf-8') as file:
        sql_commands = file.read().split(';')
        
    for command in sql_commands:
        if command.strip():
            cursor.execute(command)
            
    db_conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database='srmap_events')
    db_cursor = db_conn.cursor()
    
    password_hash = generate_password_hash("1133456@Sumit")
    
    # Dummy Admin
    db_cursor.execute("SELECT * FROM admins WHERE username='admin'")
    if not db_cursor.fetchone():
        db_cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", ('admin', password_hash))
        
    # Dummy Student
    db_cursor.execute("SELECT * FROM students WHERE email='student@srmap.edu.in'")
    if not db_cursor.fetchone():
        db_cursor.execute("INSERT INTO students (name, roll_no, email, password, department) VALUES (%s, %s, %s, %s, %s)",
                          ('Sumit Student', 'AP21110010001', 'student@srmap.edu.in', password_hash, 'CSE'))
        
    # Dummy Event
    db_cursor.execute("SELECT * FROM events")
    if not db_cursor.fetchone():
        db_cursor.execute("SHOW COLUMNS FROM events LIKE 'venue_id'")
        normalized_schema = db_cursor.fetchone() is not None

        if normalized_schema:
            db_cursor.execute("INSERT INTO venues (venue_name, location, capacity) VALUES (%s, %s, %s)",
                              ('Main Auditorium', 'SRMAP Campus', 500))
            venue_id = db_cursor.lastrowid

            db_cursor.execute("INSERT INTO organizers (organizer_name, contact, email) VALUES (%s, %s, %s)",
                              ('Tech Club', '9999999999', 'techclub@srmap.edu.in'))
            organizer_id = db_cursor.lastrowid

            db_cursor.execute("""
                INSERT INTO events (event_name, description, event_date, event_time, venue_id, organizer_id, capacity) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, ('Annual Tech Fest', 'Biggest tech festival of the year!', '2026-05-10', '10:00:00', venue_id, organizer_id, 500))
        else:
            db_cursor.execute("""
                INSERT INTO events (event_name, description, event_date, event_time, venue, organizer, capacity) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, ('Annual Tech Fest', 'Biggest tech festival of the year!', '2026-05-10', '10:00:00', 'Main Auditorium', 'Tech Club', 500))
        
    db_conn.commit()
    print("Database setup complete! Fake user and admin injected.")
    print("Admin credentials: admin / 1133456@Sumit")
    print("Student credentials: student@srmap.edu.in / 1133456@Sumit")
    
except Exception as e:
    print(f"Error setting up database: {e}")
