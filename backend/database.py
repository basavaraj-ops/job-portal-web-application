import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy

# Get base directory and define database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

# Initialize SQLAlchemy
db = SQLAlchemy()

# -----------------------------
# Job model (for Flask-SQLAlchemy)
# -----------------------------
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    vacancy = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    Categories = db.Column(db.String(100), nullable=False)

# Create all tables manually 
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        confirm_password TEXT NOT NULL,
        role TEXT CHECK(role IN ('recruiter', 'job_seeker')) NOT NULL
    )
''')

# Login attempts table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Jobs table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        experience TEXT NOT NULL,
        vacancy TEXT NOT NULL,
        location TEXT NOT NULL,
        skills TEXT NOT NULL,
        salary TEXT NOT NULL,
        Categories TEXT NOT NULL
    )
''')

# Check if 'Categories' column exists in 'jobs', add if missing
cursor.execute("PRAGMA table_info(jobs)")
columns = [col[1] for col in cursor.fetchall()]
if 'Categories' not in columns:
    cursor.execute("ALTER TABLE jobs ADD COLUMN Categories TEXT NOT NULL DEFAULT ''")

# Job applications table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position TEXT NOT NULL,
        fullname TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        degree TEXT,
        school TEXT,
        year_completed TEXT,
        certifications TEXT,
        company TEXT,
        position_held TEXT,
        start_date TEXT,
        end_date TEXT,
        skills TEXT,
        ref_name TEXT,
        ref_phone TEXT,
        resume_filename TEXT NOT NULL,
        terms_accepted INTEGER NOT NULL CHECK (terms_accepted IN (0, 1)),
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
