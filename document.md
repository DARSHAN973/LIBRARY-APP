# Library Mobile App - Project Synopsis

## 📱 Project Overview
A mobile library management application built with Kivy/KivyMD framework. Supports dual access: User and Admin panels with complete book management and reading tracking.

---

## 🗂️ Core Files

### **main.py**
Entry point for the application.

**Functions:**
- `LoginScreen` class - Main login interface with 3 modes
  - `build_ui()` - Creates header with library branding
  - `build_user_login_form()` - User login form with emoji icons
  - `build_user_signup_form()` - New user registration
  - `build_admin_login_form()` - Admin authentication
  - `user_login()` - Validates user credentials
  - `user_signup()` - Creates new user account
  - `admin_login()` - Validates admin credentials
  - `show_success_dialog()` - Attractive success modal with checkmark
  - `go_to_dashboard()` - Navigates to User/Admin dashboard

### **database.py**
Database schema and operations handler.

**Functions:**
- `Database` class - SQLite database manager
  - `connect()` - Establishes database connection
  - `create_tables()` - Creates all database tables
  - `hash_password()` - SHA-256 password encryption
  - `verify_admin()` - Validates admin credentials
  - `create_default_admin()` - Creates default admin account

**Tables:**
- `admins` - Admin accounts
- `users` - User accounts
- `books` - Book catalog with analytics (views, rating)
- `book_views` - Track book view history
- `reading_sessions` - Reading time tracking
- `reading_history` - Books opened by users
- `watchlist` - User saved books
- `book_downloads` - Download tracking
- `user_activity` - User action logs
- `system_stats` - App statistics

### **utils.py**
Utility functions for data loading.

**Functions:**
- `load_books_from_json()` - Imports books from data.json to database

---

## 👤 User Modules (user_modules/)

### **user_dashboard.py**
Main user interface container with bottom navigation.

**Functions:**
- `UserDashboard` class
  - `__init__()` - Initializes dashboard with user data
  - `setup_ui()` - Creates top bar with library icon
  - `load_tab()` - Tab switching handler (Home/Browse/Search/Profile)

**Navigation:**
- Home Tab
- Browse Tab
- Search Tab
- Profile Tab

### **home_tab.py**
User home screen with personalized content.

**Functions:**
- `load_home_tab()` - Main home screen builder
- `create_greeting_section()` - Welcome banner with emoji
- `create_stats_section()` - Books read & saved count cards
- `create_popular_books_section()` - Most viewed books carousel
- `create_recent_books_section()` - Recently added books
- `create_recommended_books_section()` - Personalized recommendations
- `show_book_details()` - Book detail modal with read/save options
- `add_to_watchlist()` - Save book to user's list
- `remove_from_watchlist()` - Remove book from saved list
- `open_book()` - Track reading history & open PDF

### **browse_tab.py**
Browse books by subject categories.

**Functions:**
- `load_browse_tab()` - Creates subject category grid
- `create_subject_card()` - Individual subject card with icon
- `show_subject_books()` - Modal showing books in selected subject

### **search_tab.py**
Book search with live suggestions.

**Functions:**
- `load_search_tab()` - Search interface builder
- `on_search_text()` - Live search suggestions handler
- `show_suggestions()` - Display search suggestion list
- `hide_suggestions()` - Clear suggestion dropdown
- `search_books()` - Execute full search query
- `save_recent_search()` - Save search to history
- `load_recent_searches()` - Display recent search chips

### **profile_tab.py**
User profile with stats and book lists.

**Functions:**
- `load_profile_tab()` - Profile interface builder
- `create_stat_card_modern()` - Stats cards (books read/saved)
- `create_action_card()` - Action buttons with icons
- `show_reading_history()` - Modal with all read books
- `show_watchlist()` - Modal with saved books
- `logout()` - User logout handler
- Displays: User info, email, phone, reading stats, logout

---

## 🛡️ Admin Modules (admin_modules/)

### **admin_dashboard.py**
Admin control panel with tab navigation.

**Functions:**
- `AdminDashboard` class
  - `__init__()` - Initializes admin panel
  - `setup_ui()` - Creates admin interface with tabs
  - `load_tab()` - Tab switching (Dashboard/Books/Users/Settings)

**Tabs:**
- Dashboard - Analytics overview
- Manage Books - Book CRUD operations
- Manage Users - User management
- Settings - App configuration

### **admin_auth.py**
Admin session management.

**Functions:**
- `save_session()` - Persist admin login session
- `load_session()` - Retrieve saved session
- `clear_session()` - Logout admin

### **dashboard_layout.py**
Admin dashboard analytics view.

**Functions:**
- `load_dashboard()` - Main analytics screen
- `create_stat_card()` - Statistical cards for metrics
- `create_recent_activity_card()` - Recent user activity log

**Displays:**
- Total books, users, active users
- Today's views, downloads
- Recent user activity

### **manage_books.py**
Complete book management interface.

**Functions:**
- `load_manage_books()` - Book management screen
- `load_books()` - Display all books in grid
- `search_books()` - Filter books by search query
- `show_add_book_dialog()` - Add new book form
- `show_edit_book_dialog()` - Edit existing book
- `save_book()` - Insert/update book in database
- `delete_book()` - Remove book with confirmation

**Features:**
- Search functionality
- Add/Edit/Delete books
- Book details modal
- View count & rating display

### **manage_users.py**
User account management.

**Functions:**
- `load_manage_users()` - User management screen
- `load_users()` - Display all users in list
- `search_users()` - Filter users by search
- `show_user_details()` - User detail modal
- `toggle_user_status()` - Activate/deactivate user
- `delete_user()` - Remove user with confirmation

**Features:**
- Search users
- View user details
- Toggle active status
- Delete users

### **settings.py**
App configuration panel.

**Functions:**
- `load_settings()` - Settings interface
- `save_app_settings()` - Persist configuration
- `load_app_settings()` - Load saved settings
- `reset_app_data()` - Clear app cache/data

**Settings:**
- App name, version
- Theme preferences
- Data management

---

## 📊 Data Files

### **data.json**
Source data file containing book catalog for import.

### **data/admin_session.json**
Stores admin login session data.

### **data/app_settings.json**
Application configuration settings.

### **data/recent_searches.json**
User search history storage.

### **library.db**
SQLite database storing all application data.

---

## 🎨 UI Features

**Theme:**
- Primary Blue: `#2196F3` (0.13, 0.59, 0.95, 1)
- Secondary Red: `#F44336` (0.96, 0.26, 0.21, 1)
- Card radius: 12-16dp
- Emoji icons for reliability

**Components:**
- Modal dialogs for details
- Cards with rounded corners
- Gradient backgrounds
- Bottom navigation
- Live search suggestions
- Success/Error feedback
- Confirmation dialogs

---

## 🔐 Authentication Flow

1. **User Login:** Username + Password → UserDashboard
2. **User Signup:** Create account → Auto-login → UserDashboard
3. **Admin Login:** Admin ID + Password → AdminDashboard

Default Admin: `admin` / `admin123`

---

## 📈 Key Functionalities

**User Side:**
- Browse books by subject
- Search with live suggestions
- View book details
- Save books to watchlist
- Track reading history
- Open PDF books
- View profile stats

**Admin Side:**
- View analytics dashboard
- Add/Edit/Delete books
- Manage user accounts
- Monitor user activity
- Configure app settings
- View system statistics

---

## 🗃️ Database Tables Summary

| Table | Purpose |
|-------|---------|
| admins | Admin authentication |
| users | User accounts |
| books | Book catalog |
| book_views | View tracking |
| reading_sessions | Reading time logs |
| reading_history | Books opened |
| watchlist | Saved books |
| book_downloads | Download tracking |
| user_activity | User actions |
| system_stats | App metrics |

---

## 🚀 Setup & Run

```bash
# Install dependencies
pip install kivy kivymd

# Run application
python main.py

# Import books from JSON
python -c "from utils import load_books_from_json; load_books_from_json()"
```

---

## 📱 Screen Size
Window: 360x640 (Mobile viewport for testing)

---

*Project completed with modern UI, emoji icons, and complete library management functionality.*
