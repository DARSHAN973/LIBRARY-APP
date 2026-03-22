"""Fast migration of books data to PostgreSQL with batch processing"""

import os
import sqlite3 as _sqlite3
import pg8000.dbapi
from urllib.parse import urlparse

RAILWAY_DATABASE_URL = (
    "postgresql://postgres:LaOEWdgPFEnQiGytKyaykfAfHDdaBQGY"
    "@caboose.proxy.rlwy.net:24267/railway"
)
SQLITE_DB = "library.db"
BATCH_SIZE = 500


def parse_database_url(url):
    parsed = urlparse(url)
    return {
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "database": (parsed.path or "").lstrip("/"),
    }


def migrate_books_fast():
    """Migrate books from SQLite to PostgreSQL with batch inserts"""
    print("Reading books from SQLite...")
    
    # Read from SQLite
    sqlite_conn = _sqlite3.connect(SQLITE_DB)
    sqlite_cursor = sqlite_conn.cursor()
    
    sqlite_cursor.execute("""
        SELECT id, title, author, publisher, medium, standard, issn, subject,
               syllabus, description, year_of_publication, content_type,
               book_type, pdf_link, thumbnail_link
        FROM books
        ORDER BY id
    """)
    
    books = sqlite_cursor.fetchall()
    sqlite_conn.close()
    
    print(f"Found {len(books)} books in SQLite")
    
    if not books:
        print("No books to migrate")
        return
    
    # Connect to PostgreSQL
    print("Connecting to PostgreSQL...")
    db_url = os.getenv("DATABASE_URL", RAILWAY_DATABASE_URL)
    conf = parse_database_url(db_url)
    pg_conn = pg8000.dbapi.connect(
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        database=conf["database"],
    )
    
    pg_cursor = pg_conn.cursor()
    
    # Clear existing books
    print("Clearing existing books from PostgreSQL...")
    pg_cursor.execute("DELETE FROM books")
    pg_conn.commit()
    
    # Insert in batches
    print(f"Inserting {len(books)} books in batches of {BATCH_SIZE}...")
    
    insert_query = """
        INSERT INTO books (
            id, title, author, publisher, medium, standard, issn, subject,
            syllabus, description, year_of_publication, content_type,
            book_type, pdf_link, thumbnail_link, views, downloads, rating, rating_count
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, 0, 0, 0)
    """
    
    for i in range(0, len(books), BATCH_SIZE):
        batch = books[i:i+BATCH_SIZE]
        pg_cursor.executemany(insert_query, batch)
        pg_conn.commit()
        print(f"  Inserted {min(i+BATCH_SIZE, len(books))}/{len(books)} books")
    
    # Reset sequence
    print("Resetting database sequence...")
    pg_cursor.execute("SELECT setval('books_id_seq', (SELECT MAX(id) FROM books), true)")
    pg_conn.commit()
    
    pg_cursor.close()
    pg_conn.close()
    
    print(f"\n✓ Successfully migrated {len(books)} books to PostgreSQL!")


if __name__ == "__main__":
    migrate_books_fast()
