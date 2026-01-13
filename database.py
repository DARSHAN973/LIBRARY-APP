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
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Books table - Enhanced with analytics fields
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
                views INTEGER DEFAULT 0,
                rating REAL DEFAULT 0,
                rating_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Book Views Tracking
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS book_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_id INTEGER,
                view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        '''
        )
        
        # Reading Sessions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reading_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                duration_minutes INTEGER,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # User Activity Log
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_type TEXT NOT NULL,
                activity_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Watchlist - User's saved/favorite books
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, book_id)
            )
        ''')
        
        # Reading History - Track when user opens PDFs
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reading_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # System Statistics (for dashboard analytics)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stat_date DATE DEFAULT (date('now')),
                total_users INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0,
                total_books INTEGER DEFAULT 0,
                new_registrations INTEGER DEFAULT 0,
                UNIQUE(stat_date)
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
                        content_type, book_type, pdf_link, thumbnail_link,
                        views, downloads
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    book.get('thumbnailLink'),
                    0,  # views (will be randomized later)
                    0   # downloads (will be randomized later)
                ))
                imported += 1
            except Exception as e:
                print(f"Error importing book {book.get('id')}: {e}")
                
        self.conn.commit()
        self.close()
        print(f"✓ Imported {imported} books from {json_file}")
        return imported
    
    def generate_sample_analytics_data(self):
        """Generate sample data for testing analytics dashboard"""
        import random
        from datetime import timedelta
        
        self.connect()
        
        # Get all books
        self.cursor.execute("SELECT id FROM books LIMIT 100")
        book_ids = [row[0] for row in self.cursor.fetchall()]
        
        # Get all users
        self.cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in self.cursor.fetchall()]
        
        if not user_ids:
            # Create some sample users
            for i in range(10):
                username = f"user{i+1}"
                password_hash = self.hash_password(f"password{i+1}")
                try:
                    self.cursor.execute(
                        "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                        (username, password_hash, f"{username}@library.com")
                    )
                except:
                    pass
            self.conn.commit()
            self.cursor.execute("SELECT id FROM users")
            user_ids = [row[0] for row in self.cursor.fetchall()]
        
        # Update books with random views and downloads
        for book_id in book_ids:
            views = random.randint(50, 500)
            downloads = random.randint(10, min(views // 2, 200))
            rating = round(random.uniform(3.5, 5.0), 1)
            rating_count = random.randint(5, 100)
            
            self.cursor.execute('''
                UPDATE books 
                SET views = ?, downloads = ?, rating = ?, rating_count = ?
                WHERE id = ?
            ''', (views, downloads, rating, rating_count, book_id))
        
        # Generate book downloads for last 30 days
        for _ in range(200):
            if user_ids and book_ids:
                user_id = random.choice(user_ids) if random.random() > 0.2 else None
                book_id = random.choice(book_ids)
                days_ago = random.randint(0, 30)
                download_date = datetime.now() - timedelta(days=days_ago)
                
                try:
                    self.cursor.execute('''
                        INSERT INTO book_downloads (book_id, user_id, download_date)
                        VALUES (?, ?, ?)
                    ''', (book_id, user_id, download_date))
                except:
                    pass
        
        # Generate reading sessions
        for _ in range(300):
            if user_ids and book_ids:
                book_id = random.choice(book_ids)
                user_id = random.choice(user_ids)
                days_ago = random.randint(0, 30)
                start_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 12))
                duration = random.randint(5, 180)  # 5 to 180 minutes
                end_time = start_time + timedelta(minutes=duration)
                
                try:
                    self.cursor.execute('''
                        INSERT INTO reading_sessions (book_id, user_id, start_time, end_time, duration_minutes)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (book_id, user_id, start_time, end_time, duration))
                except:
                    pass
        
        # Generate book views for analytics
        for _ in range(500):
            if user_ids and book_ids:
                book_id = random.choice(book_ids)
                user_id = random.choice(user_ids) if random.random() > 0.3 else None
                days_ago = random.randint(0, 30)
                view_date = datetime.now() - timedelta(days=days_ago)
                
                try:
                    self.cursor.execute('''
                        INSERT INTO book_views (book_id, user_id, view_date)
                        VALUES (?, ?, ?)
                    ''', (book_id, user_id, view_date))
                except:
                    pass
        
        # Update system stats for last 7 days
        for days_ago in range(7):
            stat_date = datetime.now().date() - timedelta(days=days_ago)
            total_users = len(user_ids) - random.randint(0, days_ago)
            active_users = random.randint(total_users // 2, total_users)
            total_books = len(book_ids)
            books_downloaded = random.randint(20, 80)
            new_registrations = random.randint(0, 5)
            
            try:
                self.cursor.execute('''
                    INSERT OR REPLACE INTO system_stats 
                    (stat_date, total_users, active_users, total_books, books_downloaded, new_registrations)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (stat_date, total_users, active_users, total_books, books_downloaded, new_registrations))
            except:
                pass
        
        self.conn.commit()
        self.close()
        print("✓ Sample analytics data generated successfully")


if __name__ == '__main__':
    # Initialize database
    db = Database()
    db.create_tables()
    
    # Create default admin user
    db.create_admin('admin', 'admin123', 'admin@library.com')
    
    # Import books from JSON
    db.import_books_from_json()
    
    # Generate sample analytics data
    db.generate_sample_analytics_data()
