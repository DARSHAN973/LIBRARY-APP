"""
Flask REST API for Library Mobile App
Runs on Railway and provides HTTP endpoints for mobile app authentication and book operations
"""

from flask import Flask, request, jsonify
from functools import wraps
import sqlite3
import json
from datetime import datetime
from database import Database
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'library-mobile-secret-key-2024'


def get_db():
    """Get database instance"""
    return Database()


def token_required(f):
    """Decorator to check for valid session token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Session-Token')
        if not token:
            return jsonify({'error': 'Missing session token'}), 401
        
        db = get_db()
        try:
            # Verify token exists in active sessions
            cursor = db.conn.cursor()
            cursor.execute('SELECT uid FROM users WHERE session_token = ? LIMIT 1', (token,))
            user = cursor.fetchone()
            if not user:
                return jsonify({'error': 'Invalid session token'}), 401
            request.uid = user[0]
        except Exception as e:
            return jsonify({'error': f'Error verifying token: {str(e)}'}), 500
        finally:
            db.conn.close()
        
        return f(*args, **kwargs)
    return decorated


# ============= AUTH ENDPOINTS =============

@app.route('/api/auth/login', methods=['POST'])
def user_login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400
        
        db = get_db()
        result = db.user_login(email, password)
        db.conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'uid': result[0],
                'name': result[1],
                'session_token': result[2]
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/signup', methods=['POST'])
def user_signup():
    """User signup endpoint"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        
        if not all([name, email, phone, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        db = get_db()
        result = db.user_signup(name, email, phone, password)
        db.conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'uid': result[0],
                'name': result[1],
                'session_token': result[2]
            }), 200
        else:
            return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/admin-login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
        
        db = get_db()
        result = db.admin_login(username, password)
        db.conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'aid': result[0],
                'name': result[1],
                'session_token': result[2]
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout():
    """Logout endpoint - clear session token"""
    try:
        db = get_db()
        cursor = db.conn.cursor()
        cursor.execute('UPDATE users SET session_token = NULL WHERE uid = ?', (request.uid,))
        db.conn.commit()
        db.conn.close()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= BOOK ENDPOINTS =============

@app.route('/api/books', methods=['GET'])
def get_books():
    """Get all books with optional filters"""
    try:
        search = request.args.get('search', '')
        subject = request.args.get('subject', '')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        db = get_db()
        books = db.get_books(search=search, subject=subject, limit=limit, offset=offset)
        db.conn.close()
        
        return jsonify({
            'success': True,
            'books': books,
            'count': len(books)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/books/<int:bid>', methods=['GET'])
def get_book(bid):
    """Get book details"""
    try:
        db = get_db()
        cursor = db.conn.cursor()
        cursor.execute('''
            SELECT bid, title, author, subject, pdf_link 
            FROM books WHERE bid = ?
        ''', (bid,))
        book = cursor.fetchone()
        db.conn.close()
        
        if book:
            return jsonify({
                'success': True,
                'book': {
                    'bid': book[0],
                    'title': book[1],
                    'author': book[2],
                    'subject': book[3],
                    'pdf_link': book[4]
                }
            }), 200
        else:
            return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= PROFILE ENDPOINTS =============

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    try:
        db = get_db()
        cursor = db.conn.cursor()
        cursor.execute('''
            SELECT uid, name, email, phone FROM users WHERE uid = ?
        ''', (request.uid,))
        user = cursor.fetchone()
        db.conn.close()
        
        if user:
            return jsonify({
                'success': True,
                'profile': {
                    'uid': user[0],
                    'name': user[1],
                    'email': user[2],
                    'phone': user[3]
                }
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= READING HISTORY ENDPOINTS =============

@app.route('/api/reading-history', methods=['GET'])
@token_required
def get_reading_history():
    """Get user's reading history"""
    try:
        db = get_db()
        cursor = db.conn.cursor()
        
        # Get deduped reading history (group by book_id, show latest)
        cursor.execute('''
            SELECT b.bid, b.title, b.author, b.subject, b.pdf_link, 
                   MAX(rh.opened_at) as last_opened
            FROM reading_history rh
            JOIN books b ON rh.bid = b.bid
            WHERE rh.uid = ?
            GROUP BY b.bid, b.title, b.author, b.subject, b.pdf_link
            ORDER BY last_opened DESC
        ''', (request.uid,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'bid': row[0],
                'title': row[1],
                'author': row[2],
                'subject': row[3],
                'pdf_link': row[4],
                'last_opened': row[5]
            })
        
        db.conn.close()
        return jsonify({'success': True, 'history': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reading-history', methods=['POST'])
@token_required
def add_reading_history():
    """Add to reading history"""
    try:
        data = request.get_json()
        bid = data.get('bid')
        
        if not bid:
            return jsonify({'error': 'Missing book id'}), 400
        
        db = get_db()
        cursor = db.conn.cursor()
        cursor.execute('''
            INSERT INTO reading_history (uid, bid, opened_at)
            VALUES (?, ?, ?)
        ''', (request.uid, bid, datetime.now().isoformat()))
        db.conn.commit()
        db.conn.close()
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= WATCHLIST ENDPOINTS =============

@app.route('/api/watchlist', methods=['GET'])
@token_required
def get_watchlist():
    """Get user's watchlist"""
    try:
        db = get_db()
        cursor = db.conn.cursor()
        cursor.execute('''
            SELECT b.bid, b.title, b.author, b.subject, b.pdf_link
            FROM watchlist w
            JOIN books b ON w.bid = b.bid
            WHERE w.uid = ?
            ORDER BY w.added_at DESC
        ''', (request.uid,))
        
        watchlist = []
        for row in cursor.fetchall():
            watchlist.append({
                'bid': row[0],
                'title': row[1],
                'author': row[2],
                'subject': row[3],
                'pdf_link': row[4]
            })
        
        db.conn.close()
        return jsonify({'success': True, 'watchlist': watchlist}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/watchlist', methods=['POST'])
@token_required
def add_watchlist():
    """Add to watchlist"""
    try:
        data = request.get_json()
        bid = data.get('bid')
        
        if not bid:
            return jsonify({'error': 'Missing book id'}), 400
        
        db = get_db()
        cursor = db.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO watchlist (uid, bid, added_at)
            VALUES (?, ?, ?)
        ''', (request.uid, bid, datetime.now().isoformat()))
        db.conn.commit()
        db.conn.close()
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/watchlist/<int:bid>', methods=['DELETE'])
@token_required
def remove_watchlist(bid):
    """Remove from watchlist"""
    try:
        db = get_db()
        cursor = db.conn.cursor()
        cursor.execute('DELETE FROM watchlist WHERE uid = ? AND bid = ?', (request.uid, bid))
        db.conn.commit()
        db.conn.close()
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= HEALTH CHECK =============

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Library API'}), 200


if __name__ == '__main__':
    # For local testing
    app.run(debug=True, host='0.0.0.0', port=5000)
