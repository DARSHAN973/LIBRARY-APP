"""
HTTP Client for Library Mobile App
Communicates with the Flask REST API instead of direct database access
"""

import requests
import json
from urllib.parse import urljoin


class APIClient:
    """HTTP client for API communication"""
    
    def __init__(self, base_url="http://localhost:5000"):
        """Initialize with API base URL"""
        self.base_url = base_url
        self.session_token = None
        self.uid = None
        self.aid = None
    
    def _make_request(self, method, endpoint, data=None, require_token=False):
        """Make HTTP request to API"""
        try:
            url = urljoin(self.base_url, endpoint)
            headers = {'Content-Type': 'application/json'}
            
            if require_token and self.session_token:
                headers['X-Session-Token'] = self.session_token
            
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return {'error': f'Unsupported method: {method}'}
            
            if response.status_code == 200 or response.status_code == 201:
                return response.json()
            else:
                try:
                    return response.json()
                except:
                    return {'error': f'HTTP {response.status_code}: {response.text}'}
        except requests.exceptions.Timeout:
            return {'error': 'Connection timeout'}
        except requests.exceptions.ConnectionError:
            return {'error': 'Connection failed'}
        except Exception as e:
            return {'error': str(e)}
    
    # ===== AUTH METHODS =====
    
    def user_login(self, email, password):
        """User login"""
        result = self._make_request('POST', '/api/auth/login', {
            'email': email,
            'password': password
        })
        
        if result.get('success'):
            self.session_token = result.get('session_token')
            self.uid = result.get('uid')
        
        return result
    
    def user_signup(self, name, email, phone, password):
        """User signup"""
        result = self._make_request('POST', '/api/auth/signup', {
            'name': name,
            'email': email,
            'phone': phone,
            'password': password
        })
        
        if result.get('success'):
            self.session_token = result.get('session_token')
            self.uid = result.get('uid')
        
        return result
    
    def admin_login(self, username, password):
        """Admin login"""
        result = self._make_request('POST', '/api/auth/admin-login', {
            'username': username,
            'password': password
        })
        
        if result.get('success'):
            self.session_token = result.get('session_token')
            self.aid = result.get('aid')
        
        return result
    
    def logout(self):
        """Logout"""
        return self._make_request('POST', '/api/auth/logout', require_token=True)
    
    # ===== BOOK METHODS =====
    
    def get_books(self, search='', subject='', limit=50, offset=0):
        """Get books"""
        endpoint = f'/api/books?search={search}&subject={subject}&limit={limit}&offset={offset}'
        return self._make_request('GET', endpoint)
    
    def get_book(self, bid):
        """Get single book"""
        return self._make_request('GET', f'/api/books/{bid}')
    
    # ===== PROFILE METHODS =====
    
    def get_profile(self):
        """Get user profile"""
        return self._make_request('GET', '/api/profile', require_token=True)
    
    # ===== READING HISTORY METHODS =====
    
    def get_reading_history(self):
        """Get reading history"""
        return self._make_request('GET', '/api/reading-history', require_token=True)
    
    def add_reading_history(self, bid):
        """Add to reading history"""
        return self._make_request('POST', '/api/reading-history', {'bid': bid}, require_token=True)
    
    # ===== WATCHLIST METHODS =====
    
    def get_watchlist(self):
        """Get watchlist"""
        return self._make_request('GET', '/api/watchlist', require_token=True)
    
    def add_watchlist(self, bid):
        """Add to watchlist"""
        return self._make_request('POST', '/api/watchlist', {'bid': bid}, require_token=True)
    
    def remove_watchlist(self, bid):
        """Remove from watchlist"""
        return self._make_request('DELETE', f'/api/watchlist/{bid}', require_token=True)
    
    # ===== HEALTH CHECK =====
    
    def health_check(self):
        """Check API health"""
        return self._make_request('GET', '/api/health')
