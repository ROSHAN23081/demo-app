import sqlite3
from datetime import datetime
import hashlib

class MobileObjexDB:
    def __init__(self, db_name='mobile_objex.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table (Registration)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                company TEXT,
                is_verified BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Brands table (Companies sending SMS)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                industry TEXT,
                safety_mark_approved BOOLEAN DEFAULT 0,
                sms_credits INTEGER DEFAULT 1000,
                api_key TEXT UNIQUE
            )
        ''')
        
        # Campaigns table (SMS campaigns)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_id INTEGER,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'draft',
                recipients_count INTEGER DEFAULT 0,
                sent_at TIMESTAMP,
                FOREIGN KEY (brand_id) REFERENCES brands (id)
            )
        ''')
        
        # Scam reports (for AI training)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scam_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                message_content TEXT,
                reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_verified_scam BOOLEAN DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, email, password, phone, first_name="", last_name=""):
        # Simple password hashing for beginners
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (email, password_hash, phone, first_name, last_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, password_hash, phone, first_name, last_name))
            self.conn.commit()
            return True
        except:
            return False
    
    def verify_user(self, phone):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET is_verified=1 WHERE phone=?', (phone,))
        self.conn.commit()
    
    def get_user(self, email):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        return cursor.fetchone()

# Create database instance
db = MobileObjexDB()
