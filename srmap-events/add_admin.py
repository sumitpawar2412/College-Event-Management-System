from pathlib import Path
import os
import sys


def _ensure_workspace_venv():
    venv_python = Path(__file__).resolve().parents[1] / '.venv' / 'Scripts' / 'python.exe'
    if venv_python.exists() and Path(sys.executable).resolve() != venv_python.resolve():
        os.execv(str(venv_python), [str(venv_python), *sys.argv])


_ensure_workspace_venv()

import pymysql
from werkzeug.security import generate_password_hash

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1133456@Sumit'
DB_NAME = 'srmap_events'

def add_new_admin():
    print("--- Add New Admin ---")
    username = input("Enter new admin username: ").strip()
    plain_password = input("Enter new admin password: ").strip()
    
    if not username or not plain_password:
        print("Username and password cannot be empty.")
        return

    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        
        # The crucial step: Hashing the password before storing it
        hashed_password = generate_password_hash(plain_password)
        
        cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        print(f"\nSuccess! Added admin '{username}'. You can now log in securely.")
    except pymysql.err.IntegrityError:
        print(f"\nError: Admin '{username}' already exists! Try a different username.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

if __name__ == '__main__':
    add_new_admin()
