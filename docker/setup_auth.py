#!/usr/bin/env python3
"""
Sovereign Authentication & User Credential Management for HRMS
Stores credentials strictly in the sovereign MariaDB database (`tabUser` and `__auth`).
Supports PBKDF2-SHA256 password hashing and verification.
"""

import hashlib
import os
import secrets
import sys
import pymysql

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "hrms")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        autocommit=True
    )

def hash_password(plain_password: str, salt: str = None) -> str:
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return f"pbkdf2_sha256${salt}${hashed}"

def verify_password(plain_password: str, stored_hash: str) -> bool:
    if not stored_hash or not plain_password:
        return False
    if stored_hash.startswith("pbkdf2_sha256$"):
        parts = stored_hash.split("$")
        if len(parts) == 3:
            salt, expected_hash = parts[1], parts[2]
            computed_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
            return secrets.compare_digest(computed_hash, expected_hash)
    # Direct match fallback for legacy plain or simple hashes
    return secrets.compare_digest(plain_password, stored_hash)

def set_password(username_or_email: str, plain_password: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Find username and email from tabUser
            cur.execute("SELECT name, email FROM `tabUser` WHERE name = %s OR email = %s", (username_or_email, username_or_email))
            user = cur.fetchone()
            name = user[0] if user else username_or_email
            email = user[1] if user else username_or_email
            
            pwd_hash = hash_password(plain_password)
            for identifier in set([name, email, username_or_email]):
                if identifier:
                    cur.execute(
                        "REPLACE INTO `__auth` (doctype, name, fieldname, password, encrypted) VALUES (%s, %s, %s, %s, %s)",
                        ("User", identifier, "password", pwd_hash, 0)
                    )
            print(f"[AUTH] Successfully updated password for '{username_or_email}' in database.")
    finally:
        conn.close()

def authenticate_user(username_or_email: str, plain_password: str):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT name, email, first_name, last_name, user_type, enabled FROM `tabUser` WHERE name = %s OR email = %s", (username_or_email, username_or_email))
            user = cur.fetchone()
            if not user:
                return None, "User not found"
            if not user.get("enabled", 1):
                return None, "User account is disabled"
            
            # Check __auth
            cur.execute("SELECT password FROM `__auth` WHERE doctype = 'User' AND name IN (%s, %s) AND fieldname = 'password' LIMIT 1", (user["name"], user["email"]))
            auth = cur.fetchone()
            if not auth:
                # If no password set yet, default allow 'admin' for initial Administrator
                if user["name"] == "Administrator" and plain_password == "admin":
                    set_password("Administrator", "admin")
                    return user, None
                return None, "Password not configured in database"
            
            if verify_password(plain_password, auth["password"]):
                return user, None
            else:
                return None, "Incorrect password"
    finally:
        conn.close()

def create_user_if_missing(name: str, email: str, first_name: str, password: str, is_admin: bool = False):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT name FROM `tabUser` WHERE name = %s OR email = %s", (name, email))
            existing = cur.fetchone()
            if not existing:
                cur.execute(
                    """INSERT INTO `tabUser` (name, email, first_name, full_name, user_type, enabled, creation, modified, modified_by, owner)
                       VALUES (%s, %s, %s, %s, %s, 1, NOW(), NOW(), 'Administrator', 'Administrator')""",
                    (name, email, first_name, first_name, "System User" if is_admin else "Website User")
                )
                print(f"[AUTH] Created new user '{name}' ({email}) in tabUser.")
        set_password(name, password)
    finally:
        conn.close()

def ensure_employee_link():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE `tabEmployee` SET `user_id` = 'Administrator' WHERE `name` = 'HR-EMP-00001' OR `employee_name` = 'Abhishek'")
            print(f"[AUTH] Ensured Employee HR-EMP-00001 is mapped to 'Administrator'.")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Initializing Sovereign HRMS Authentication...")
    # Seed default Administrator
    create_user_if_missing("Administrator", "admin@example.com", "Administrator", "admin", is_admin=True)
    ensure_employee_link()
    # Test authentication
    user, err = authenticate_user("admin@example.com", "admin")
    if user:
        print(f"Auth Test SUCCESS: Logged in as {user['name']} ({user['email']})")
    else:
        print(f"Auth Test FAILED: {err}")
