"""
Script to remove all books without PDF links from the database
"""

import sqlite3


def remove_books_without_links():
    """
    Remove all books that have no PDF link
    """
    # Connect to database
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Get all books without PDF links
    cursor.execute("SELECT id, title FROM books WHERE pdf_link IS NULL OR pdf_link = ''")
    books_without_links = cursor.fetchall()
    
    print(f"Total books without PDF links found: {len(books_without_links)}")
    
    if books_without_links:
        print("\nBooks to be deleted:")
        for book_id, title in books_without_links:
            print(f"  ID {book_id}: {title}")
        
        # Get IDs
        book_ids = [book[0] for book in books_without_links]
        placeholders = ','.join('?' * len(book_ids))
        
        # Delete from related tables first (foreign key constraints)
        try:
            cursor.execute(f"DELETE FROM book_views WHERE book_id IN ({placeholders})", book_ids)
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute(f"DELETE FROM book_reviews WHERE book_id IN ({placeholders})", book_ids)
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute(f"DELETE FROM watchlist WHERE book_id IN ({placeholders})", book_ids)
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute(f"DELETE FROM reading_history WHERE book_id IN ({placeholders})", book_ids)
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute(f"DELETE FROM reading_sessions WHERE book_id IN ({placeholders})", book_ids)
        except sqlite3.OperationalError:
            pass
        
        # Delete from books table
        cursor.execute(f"DELETE FROM books WHERE id IN ({placeholders})", book_ids)
        
        conn.commit()
        print(f"\n✓ Successfully deleted {len(book_ids)} books without PDF links")
    else:
        print("\nNo books without PDF links found")
    
    # Verify remaining books
    cursor.execute("SELECT COUNT(*) FROM books")
    remaining = cursor.fetchone()[0]
    print(f"Remaining books in database: {remaining}")
    
    # Count how many have links
    cursor.execute("SELECT COUNT(*) FROM books WHERE pdf_link IS NOT NULL AND pdf_link != ''")
    with_links = cursor.fetchone()[0]
    print(f"Books with PDF links: {with_links}")
    
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Removing Books Without PDF Links from Database")
    print("=" * 60)
    remove_books_without_links()
    print("=" * 60)
    print("Done!")
