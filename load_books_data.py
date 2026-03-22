"""Load books data from data.json into SQLite database"""

import json
import os
import sqlite3 as _sqlite3

DATA_JSON_PATH = os.path.join(os.path.dirname(__file__), "data.json")

# Use same path logic as database.py
def get_db_path():
    """Get database path - same location as data.json for initial setup"""
    db_path = os.path.join(os.path.dirname(__file__), "library.db")
    return db_path

SQLITE_DB = get_db_path()


def create_books_table(cursor):
    """Create books table if it doesn't exist"""
    cursor.execute('''
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
            downloads INTEGER DEFAULT 0,
            rating REAL DEFAULT 0,
            rating_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')


def load_books_from_json():
    """Load books data from data.json (PHPMyAdmin export format) into SQLite"""
    
    # Read data.json
    print(f"Reading {DATA_JSON_PATH}...")
    with open(DATA_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract the raw data array
    if not isinstance(data, list):
        print("ERROR: data.json must be a list")
        return False
    
    # Find the "raw" data section (PHPMyAdmin export format)
    raw_data = None
    for item in data:
        if isinstance(item, dict) and item.get("type") == "raw":
            raw_data = item.get("data", [])
            break
    
    if not raw_data:
        print("ERROR: No raw data found in data.json")
        return False
    
    print(f"Found {len(raw_data)} books in data.json")
    
    # Get direct SQLite connection (bypass remote API)
    conn = _sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    # Create books table
    create_books_table(cursor)
    print("Books table created/verified")
    
    # Clear existing books
    cursor.execute("DELETE FROM books")
    conn.commit()
    print("Cleared existing books from database")
    
    # Insert books
    inserted = 0
    errors = 0
    
    for book in raw_data:
        try:
            # Handle field name mismatches - use positional parameters for SQLite
            cursor.execute('''
                INSERT INTO books (
                    id, title, author, publisher, medium, standard, issn,
                    subject, syllabus, description, year_of_publication,
                    content_type, book_type, pdf_link, thumbnail_link,
                    views, downloads, rating, rating_count
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?
                )
            ''', (
                int(book.get('id')),
                book.get('title', ''),
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
                0,  # views
                0,  # downloads
                0.0,  # rating
                0,  # rating_count
            ))
            inserted += 1
            
        except Exception as e:
            print(f"Error inserting book {book.get('id', 'unknown')}: {e}")
            errors += 1
    
    conn.commit()
    conn.close()
    
    print(f"\nBooks loaded successfully!")
    print(f"  Inserted: {inserted}")
    print(f"  Errors: {errors}")
    
    return inserted > 0


if __name__ == "__main__":
    load_books_from_json()
