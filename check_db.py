"""Check if books table exists and has correct schema"""

import pg8000.dbapi
import os
from urllib.parse import urlparse

RAILWAY_DATABASE_URL = (
    "postgresql://postgres:LaOEWdgPFEnQiGytKyaykfAfHDdaBQGY"
    "@caboose.proxy.rlwy.net:24267/railway"
)


def parse_database_url(url):
    parsed = urlparse(url)
    return {
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "database": (parsed.path or "").lstrip("/"),
    }


print("Connecting to Railway PostgreSQL...")
db_url = os.getenv("DATABASE_URL", RAILWAY_DATABASE_URL)
conf = parse_database_url(db_url)

try:
    conn = pg8000.dbapi.connect(
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        database=conf["database"],
    )
    print("✓ Connected successfully!")
    
    cursor = conn.cursor()
    
    # Check if books table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'books'
        )
    """)
    result = cursor.fetchone()
    print(f"Books table exists: {result[0]}")
    
    if result[0]:
        # Count books
        cursor.execute("SELECT COUNT(*) FROM books")
        count = cursor.fetchone()[0]
        print(f"Current book count in PostgreSQL: {count}")
        
        # Show columns
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'books'
            ORDER BY ordinal_position
        """)
        print("\nBooks table columns:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
    
    cursor.close()
    conn.close()
    print("\n✓ Database check complete")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
