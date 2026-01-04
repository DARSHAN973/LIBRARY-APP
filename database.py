"""
Database Module for Library Mobile App
Handles SQLite database operations including admin authentication
"""

import sqlite3
import hashlib
import json
from datetime import datetime


class Database:
    def __init__(self, db_name='library.db'):
        """Initialize database connection"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.conn
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            
    def create_tables(self):
        """Create all necessary tables"""
        self.connect()
        
        # Admin table for authentication
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Users table for regular users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Books table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                publisher TEXT,
                medium TEXT,
                standard TEXT,
                issn TEXT,
                subject TEXT,
                syllabus TEXT,
                description TEXT,
                year_of_publication TEXT,
                content_type TEXT,
                book_type TEXT,
                pdf_link TEXT,
                thumbnail_link TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        self.close()
        print("✓ Database tables created successfully")
        
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def create_admin(self, username, password, email=None):
        """Create a new admin user"""
        self.connect()
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute(
                'INSERT INTO admins (username, password_hash, email) VALUES (?, ?, ?)',
                (username, password_hash, email)
            )
            self.conn.commit()
            print(f"✓ Admin user '{username}' created successfully")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Admin user '{username}' already exists")
            return False
        finally:
            self.close()
            
    def verify_admin(self, username, password):
        """Verify admin credentials"""
        self.connect()
        password_hash = self.hash_password(password)
        
        self.cursor.execute(
            'SELECT id, username FROM admins WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        result = self.cursor.fetchone()
        
        if result:
            # Update last login time
            self.cursor.execute(
                'UPDATE admins SET last_login = ? WHERE id = ?',
                (datetime.now(), result[0])
            )
            self.conn.commit()
            self.close()
            return True
        
        self.close()
        return False
        
    def create_user(self, username, password, email=None, phone=None):
        """Create a new regular user"""
        self.connect()
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute(
                'INSERT INTO users (username, password_hash, email, phone) VALUES (?, ?, ?, ?)',
                (username, password_hash, email, phone)
            )
            self.conn.commit()
            print(f"✓ User '{username}' created successfully")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ User '{username}' already exists")
            return False
        finally:
            self.close()
            
    def verify_user(self, username, password):
        """Verify user credentials"""
        self.connect()
        password_hash = self.hash_password(password)
        
        self.cursor.execute(
            'SELECT id, username FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        result = self.cursor.fetchone()
        
        if result:
            # Update last login time
            self.cursor.execute(
                'UPDATE users SET last_login = ? WHERE id = ?',
                (datetime.now(), result[0])
            )
            self.conn.commit()
            self.close()
            return True
        
        self.close()
        return False
        
    def import_books_from_json(self, json_file='data.json'):
        """Import books from JSON file to database"""
        self.connect()
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Skip header, get raw data
        books = data[1]['data'] if len(data) > 1 else []
        
        imported = 0
        for book in books:
            try:
                self.cursor.execute('''
                    INSERT OR REPLACE INTO books (
                        id, title, author, publisher, medium, standard,
                        issn, subject, syllabus, description, year_of_publication,
                        content_type, book_type, pdf_link, thumbnail_link
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    book.get('id'),
                    book.get('title'),
                    book.get('author'),
                    book.get('publisher'),
                    book.get('medium'),
                    book.get('standard'),
                    book.get('issn'),
                    book.get('subject'),
                    book.get('syllabus'),
                    book.get('description'),
                    book.get('yearOfPublication'),
                    book.get('contentType'),
                    book.get('bookType'),
                    book.get('pdfLink'),
                    book.get('thumbnailLink')
                ))
                imported += 1
            except Exception as e:
                print(f"Error importing book {book.get('id')}: {e}")
                
        self.conn.commit()
        self.close()
        print(f"✓ Imported {imported} books from {json_file}")
        return imported


if __name__ == '__main__':
    # Initialize database
    db = Database()
    db.create_tables()
    
    # Create default admin user
    db.create_admin('admin', 'admin123', 'admin@library.com')
    
    # Import books from JSON
    db.import_books_from_json()
