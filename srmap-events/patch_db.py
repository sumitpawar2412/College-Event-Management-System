import pymysql
from werkzeug.security import generate_password_hash

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1133456@Sumit'

try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database='srmap_events')
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_activity (
            login_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            role VARCHAR(20),
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Update admin credentials
    password_hash = generate_password_hash("1133456@S")
    cursor.execute("UPDATE admins SET username=%s, password=%s WHERE username='admin'", ('sumit_pawar@1133456', password_hash))
    
    conn.commit()
    print("Database patched successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
