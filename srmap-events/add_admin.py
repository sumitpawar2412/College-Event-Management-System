from pathlib import Path
import argparse
import getpass
import os
import sys


def _ensure_workspace_venv():
    venv_python = Path(__file__).resolve().parents[1] / '.venv' / 'Scripts' / 'python.exe'
    if venv_python.exists() and Path(sys.executable).resolve() != venv_python.resolve():
        os.execv(str(venv_python), [str(venv_python), *sys.argv])


_ensure_workspace_venv()

import pymysql
from werkzeug.security import generate_password_hash

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'srmap_events')

def add_new_admin(username, plain_password):
    if not username or not plain_password:
        print("Username and password cannot be empty.")
        return False

    if len(plain_password) < 6:
        print("Password must be at least 6 characters long.")
        return False

    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES LIKE 'admins'")
        if not cursor.fetchone():
            print("\nError: 'admins' table not found. Run setup_db.py first.")
            return False

        cursor.execute("SELECT admin_id FROM admins WHERE username = %s", (username,))
        if cursor.fetchone():
            print(f"\nError: Admin '{username}' already exists! Try a different username.")
            return False
        
        # The crucial step: Hashing the password before storing it
        hashed_password = generate_password_hash(plain_password)
        
        cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        print(f"\nSuccess! Added admin '{username}'. You can now log in securely.")
        return True
    except pymysql.err.OperationalError as e:
        print(f"\nDatabase connection error: {e}")
        print("Check DB_HOST, DB_USER, DB_PASSWORD, and whether MySQL is running.")
        return False
    except pymysql.err.IntegrityError:
        print(f"\nError: Admin '{username}' already exists! Try a different username.")
        return False
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return False
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Add a new admin user to the SRMAP Events database."
    )
    parser.add_argument('--username', help='New admin username')
    parser.add_argument('--password', help='New admin password (min 6 chars)')
    return parser.parse_args()


def main():
    args = parse_args()

    if args.username and args.password:
        success = add_new_admin(args.username.strip(), args.password)
        raise SystemExit(0 if success else 1)

    print("--- Add New Admin ---")
    username = (args.username or input("Enter new admin username: ")).strip()
    plain_password = args.password or getpass.getpass("Enter new admin password: ")

    success = add_new_admin(username, plain_password)
    raise SystemExit(0 if success else 1)

main()