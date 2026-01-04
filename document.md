# Library Mobile App - Project Documentation

**Project Start Date:** January 4, 2026  
**Tech Stack:** Kivy + Python + SQLite

---

## Latest Update: Code Organization & Modern Dashboard (Jan 4, 2026)

### ✅ Major Changes Implemented

**1. Code Organization**
- Created separate `dashboard_layout.py` module for dashboard components
- Separated UI components from business logic
- Modular, reusable functions for dashboard widgets

**2. Fixed Navigation Issues**
- ✅ Hamburger menu now closes automatically when tab is clicked
- ✅ Admin navigates directly to selected page
- ✅ Tab highlighting works correctly
- ✅ Removed duplicate `navigate_to()` methods

**3. Modern Dashboard Implementation**
All sections now display real data from database:

**📊 Top Section - KPI Cards (4 Cards in 2x2 Grid):**
- 📚 Total Books (from database)
- 👤 Active Users (from database)
- 🌐 Languages (3: English, Hindi, Marathi)
- 📘 Publishers (18 unique)

**📈 Middle Section - Insights:**
- 📊 Books by Subject (Top 5 with progress bars)
- 🕒 Recently Added Books (5 latest entries)

**⚡ Bottom Section - Quick Actions:**
- ➕ Add New Book (navigates to Manage Books)
- 👥 Manage Users (navigates to Manage Users)
- ⚙️ System Settings (navigates to Settings)

**Footer - System Status:**
- Database connection status
- Storage type
- Last updated timestamp

---

## File Structure

```
library_mobile_app/
├── main.py                  # App entry point, login screens
├── admin_dashboard.py       # Admin panel with navigation drawer
├── dashboard_layout.py      # Dashboard UI components (NEW)
├── database.py              # SQLite operations
├── data.json                # 2393 book records
├── document.md              # This documentation
└── .venv/                   # Virtual environment
```

---

## Latest Update: Update 6 - Menu Positioning Fix & Code Documentation (Jan 4, 2026)

### Critical Fixes Implemented
1. **✅ Menu Items Positioning**: Hamburger drawer menu now displays at TOP of screen
2. **✅ Half-Screen Dark Overlay**: Overlay only darkens right portion (250dp offset)
3. **✅ Click-to-Close**: Tapping dark area closes drawer
4. **✅ Comprehensive Code Documentation**: All methods documented with detailed docstrings

### Technical Solution: Kivy Layout Fix

**Problem**: Menu items appeared at bottom of screen  
**Root Cause**: Kivy coordinate system - (0,0) is bottom-left, BoxLayout fills bottom-up  
**Solution**: Add spacer widget at bottom to push content upward

```python
# Critical widget order (added bottom to top):
bottom_spacer = Widget(size_hint_y=1)      # Fills remaining space
self.drawer.add_widget(bottom_spacer)      # 1st: Spacer at bottom
self.drawer.add_widget(menu_container)     # 2nd: Menu in middle  
self.drawer.add_widget(drawer_header)      # 3rd: Header at top
```

### Overlay Behavior Implementation
```python
# Overlay only covers right portion, not drawer area
self.overlay = Widget(
    size=(Window.width - dp(250), Window.height),  # Right side only
    pos=(dp(250), 0),                              # Offset by drawer width
    opacity=0
)
# Click handler to close drawer
self.overlay.bind(on_touch_down=self.close_drawer_on_overlay)
```

---

## Project Overview
A mobile application for managing a library system with educational books. The app includes an admin panel for managing the library database.

## Tech Stack
- **Frontend:** Kivy (Mobile UI Framework)
- **UI Components:** KivyMD (Material Design)
- **Backend:** Python
- **Database:** SQLite
- **Additional Libraries:** Pillow, Requests

## Development Tools & Extensions
- **VS Code Extension:** BattleBas.kivy-vscode
  - Provides Kivy/KV file syntax highlighting
  - Code snippets for Kivy widgets
  - Auto-completion for Kivy properties

## Data Source
- `data.json` - Contains 2393 library book records with fields:
  - id, title, author, publisher, medium, standard
  - pdfLink, thumbnailLink, subject, syllabus
  - yearOfPublication, issn, contentType, bookType

---

## Development Progress

### Phase 1: Setup & Dependencies ✓
- [x] Python virtual environment configured (Python 3.12.3)
- [x] Installed Kivy, KivyMD, Pillow, Requests
- [x] SQLite (built-in with Python)

### Phase 2: Admin Panel ✓
- [x] Admin login screen
- [x] Database initialization
- [x] Admin authentication

---

## Code Documentation

### 1. database.py - Database Management Module

**Purpose:** Handles all SQLite database operations

**Key Features:**
- Database initialization and table creation
- Admin user management with password hashing (SHA256)
- Book data import from JSON
- Secure authentication

**Tables:**
- `admins` - Stores admin credentials and login history
  - Fields: id, username, password_hash, email, created_at, last_login
- `users` - Stores regular user credentials and login history  
  - Fields: id, username, password_hash, email, phone, created_at, last_login
- `books` - Stores library book information
  - Fields: id, title, author, publisher, medium, standard, issn, subject, syllabus, description, year_of_publication, content_type, book_type, pdf_link, thumbnail_link, created_at

**Key Methods:**
- `create_tables()` - Initialize database schema
- `create_admin(username, password, email)` - Create new admin user
- `verify_admin(username, password)` - Authenticate admin login
- `create_user(username, password, email, phone)` - Create new regular user
- `verify_user(username, password)` - Authenticate user login
- `import_books_from_json(json_file)` - Import book data from JSON file

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@library.com`

### 2. main.py - Main Application & Multi-Option Login Screen

**Purpose:** Kivy/KivyMD mobile application with user/admin login interface

**Key Features:**
- Material Design UI components
- Three login modes in one screen:
  - **User Login** - For regular users
  - **User Signup** - New user registration
  - **Admin Login** - For administrators
- Real-time authentication
- Error handling and validation
- Responsive scrollable interface

**Login Modes:**

1. **User Login**
   - Username and password fields
   - Verifies against `users` table
   - Access to user dashboard

2. **User Signup**
   - Username (required)
   - Email (optional)
   - Phone (optional)
   - Password with confirmation (min 6 characters)
   - Creates new user account
   - Auto-switches to login after signup

3. **Admin Login**
   - Admin ID field
   - Admin password field
   - Verifies against `admins` table
   - Default credentials: `admin` / `admin123`
   - Access to admin dashboard

**Screens:**
- `LoginScreen` - Multi-mode authentication interface
  - Mode switcher buttons at top
  - Dynamic form based on selected mode
  - Password validation for signup
  - Success/error dialogs
  
- `UserDashboard` - User's main screen after login
  - Welcome header with username
  - Logout functionality
  - Placeholder for book browsing features
  
- `AdminDashboard` - Admin's control panel
  - Admin identification display
  - Logout functionality
  - Placeholder for management features
  - Stats display (books, users, sessions)

**App Configuration:**
- Theme: Material Design (Blue, Light mode)
- Window Size: 360x640 (for testing)
- Screen Management: ScreenManager for navigation

**Login Flow:**
1. User selects login mode (User Login/Signup/Admin)
2. Form updates dynamically
3. User enters credentials
4. System validates input
5. Checks against appropriate database table
6. Shows success or error message
7. Updates last login timestamp
8. Navigates to dashboard

### 3. Running the Application

```bash
# Activate virtual environment and run
/home/darshan/darshan/library_mobile_app/.venv/bin/python main.py

# OR use shorter command
.venv/bin/python main.py
```

**IMPORTANT:** Always use the virtual environment Python, not the system Python!

**First Run:**
- Database tables are automatically created
- Default admin user is created (admin/admin123)
- Books can be imported from data.json

**Test Accounts:**
- Admin: username=`admin`, password=`admin123`
- Users: Create new accounts via signup

---

## Recent Updates & Changes

### Update 1: Multi-Mode Login System (Jan 4, 2026)
**Changes Made:**
- Added user registration/signup functionality
- Separated user and admin authentication
- Created `users` table in database alongside `admins` table
- Added three-tab interface: User Login | Sign Up | Admin
- Color-coded buttons (Blue for users, Red for admin)

**Database Changes:**
- New table: `users` (username, password_hash, email, phone, created_at, last_login)
- New methods: `create_user()`, `verify_user()`
- Password validation: minimum 6 characters
- Password confirmation in signup

**UI Changes:**
- Dynamic form rendering based on selected mode
- Mode switcher buttons with active state highlighting
- Signup form with optional email and phone fields
- Separate admin login with warning label

### Update 2: Responsive Layout Fix (Jan 4, 2026)
**Problem:** Elements overlapping on desktop preview
**Solution:** Changed from fixed heights to auto-sizing layout

**Changes Made:**
- Removed fixed 400px height on form container
- Changed to `size_hint_y=None` with `minimum_height` binding
- Reduced all spacing from 15-20dp to 12-15dp for mobile
- Reduced button heights from 50dp to 48dp
- Reduced title sizes (H2→H3, H5→H6, H6→Subtitle1)
- Added proper spacers between sections
- Improved ScrollView implementation

**Technical Details:**
- Form container now auto-calculates height based on content
- Better mobile compatibility (360x640 screen)
- No more content cutoff or overlap
- Smooth scrolling for all content

### Update 3: UI Fixes (Jan 4, 2026)
**Problems Fixed:**
1. Emoji icon showing as square box
2. Tab button text hidden when selected (white text on white background)

**Solutions:**
1. Replaced emoji 📚 with text-based logo `[LIBRARY]`
2. Added dynamic `text_color` property to tab buttons
   - Selected: White text on colored background
   - Unselected: Colored text on white background

### Update 4: Functional Login/Signup System (Jan 4, 2026)
**Major Update:** Full authentication and navigation implementation

**Features Added:**
1. **User Signup - Fully Functional**
   - Creates user account in database
   - Stores hashed password (SHA256)
   - Auto-login after successful registration
   - Redirects to User Dashboard

2. **User Login - Fully Functional**
   - Verifies credentials against database
   - Updates last_login timestamp
   - Redirects to User Dashboard

3. **Admin Login - Fully Functional**
   - Separate authentication for admins
   - Verifies against admin table
   - Redirects to Admin Dashboard
   - **Default Credentials: `admin` / `admin123`**

4. **Navigation System**
   - Screen Manager with 3 screens: Login, UserDashboard, AdminDashboard
   - Automatic redirection after authentication
   - Logout functionality returns to login screen

5. **Dashboard Screens Created**
   - **User Dashboard:**
     - Welcome message with username
     - Logout button
     - Placeholder for book browsing (coming soon)
     - Blue/neutral theme
   
   - **Admin Dashboard:**
     - Admin identification in header
     - Logout button
     - Placeholder for book/user management
     - Light red tint background
     - Basic stats display (Total Books: 2393)

**Technical Implementation:**
- `set_user_name(username)` - Pass username to dashboard
- `set_admin_name(admin)` - Pass admin name to dashboard
- `go_to_dashboard(user_type, username)` - Navigate to correct dashboard
- Screen transitions using `manager.current`

**User Flow:**
```
Signup → Auto-login → User Dashboard
Login → Verify → User Dashboard
Admin Login → Verify → Admin Dashboard
Dashboard → Logout → Login Screen
```

### Update 5: Admin Panel with Navigation System (Jan 4, 2026)
**Major Update:** Complete admin panel redesign with hamburger menu navigation

**Created Separate File:** `admin_dashboard.py` for better code organization

**Features Added:**
1. **Mobile-Optimized Hamburger Menu**
   - ✅ Proper 3-line icon using MDIconButton
   - Smooth slide-in/slide-out animation (0.3s)
   - Drawer width: 250dp
   - Overlay with semi-transparent background
   - Click outside drawer to close

2. **Navigation Menu Items:**
   - Dashboard (default)
   - Manage Books
   - Manage Users
   - Admin Authentication
   - System Settings

3. **Header Design (Mobile Optimized):**
   - Height: 56dp (standard mobile header)
   - Blue background (0.2, 0.6, 1, 1)
   - Hamburger icon button (left)
   - Current section title (center)
   - Logout icon button (right)

4. **Dashboard Content (Stacked for Mobile):**
   - Welcome message with admin name
   - Stats cards (vertical stack):
     - Total Books: 2393 (blue card, 90dp height)
     - Total Users: -- (green card, 90dp height)
   - Recent activity card (120dp height)

5. **Navigation Drawer:**
   - Header with "ADMIN PANEL" title
   - Admin name display
   - 5 menu items with icons
   - Clean tap-to-navigate
   - Auto-closes after selection

**Technical Implementation:**
```python
- FloatLayout for overlay support
- Animation() for smooth drawer transitions
- pos_hint for off-screen positioning
- MDIconButton for proper hamburger icon
- Separate sections: dashboard, manage_books, manage_users, admin_auth, settings
```

**File Structure:**
```
admin_dashboard.py - Complete admin panel (mobile optimized)
main.py - Login, UserDashboard, app initialization
database.py - Database operations
```

**Mobile Optimizations:**
- Cards stacked vertically (not horizontal)
- Proper touch targets (48dp minimum)
- Responsive spacing (10-15dp)
- ScrollView for overflow content
- Optimized for 360x640 screen

---

## VS Code Extension Usage: BattleBas.kivy-vscode

### Installation ✓
```
Extension ID: BattleBas.kivy-vscode
```

### Features & How to Use:

#### 1. Syntax Highlighting
- Automatically highlights Kivy/KV file syntax
- Works on `.kv` files (Kivy language files)
- Color codes widget names, properties, and values

#### 2. Code Snippets
Type these shortcuts and press Tab:

**Widget Snippets:**
- `box` → Creates BoxLayout
- `grid` → Creates GridLayout
- `float` → Creates FloatLayout
- `button` → Creates Button widget
- `label` → Creates Label widget
- `text` → Creates TextInput
- `image` → Creates Image widget

**Example:**
Type `button` + Tab:
```python
Button(
    text='',
    size_hint=(None, None),
    size=(100, 50)
)
```

#### 3. Auto-Completion
- Type widget names and get suggestions
- Shows available properties for widgets
- Press Ctrl+Space for suggestions

#### 4. Creating .kv Files (Optional)
You can separate UI from logic using KV language:

**Create:** `login.kv`
```kv
#:kivy 2.0

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        
        MDLabel:
            text: 'Library App'
            font_style: 'H5'
            halign: 'center'
        
        MDTextField:
            id: username
            hint_text: 'Username'
            icon_left: 'account'
```

**Load in Python:**
```python
from kivy.lang import Builder

Builder.load_file('login.kv')
```

### Current Project Structure
We're using **Pure Python approach** (not .kv files) for:
- Better IDE support and autocomplete
- Easier debugging
- More explicit code
- Better for beginners

**If you want to use .kv files later:**
- Extension will provide full syntax highlighting
- Better visual separation of UI and logic
- More compact code

### Extension Settings
No configuration needed - works automatically!

**Optional Settings in VS Code:**
1. Go to Settings (Ctrl+,)
2. Search for "Kivy"
3. Customize (if needed)

---

## Project File Structure
```
library_mobile_app/
├── .venv/                      # Virtual environment
├── data.json                   # Library books data (2393 records)
├── database.py                 # Database management module
├── main.py                     # Main Kivy application
├── library.db                  # SQLite database (auto-created)
├── document.md                 # Project documentation (this file)
├── MOBILE_PREVIEW_GUIDE.md     # Mobile testing guide
└── .gitignore                  # Git ignore file
```

---

## Next Steps
- [ ] Build admin dashboard interface
- [ ] Build user dashboard interface
- [ ] Implement book management (CRUD operations)
- [ ] Add book search and filter functionality
- [ ] Create book detail view
- [ ] Add image caching for thumbnails
- [ ] Implement pagination for large datasets
- [ ] Add book categories/filters
- [ ] User profile management

---

## Admin Dashboard Code Documentation

### File: `admin_dashboard.py`

#### Class: `AdminDashboard(MDScreen)`
Main admin panel screen with hamburger menu navigation system.

**Attributes:**
- `drawer_open` (bool): Tracks whether navigation drawer is currently open or closed
- `current_section` (str): ID of currently displayed section (e.g., 'dashboard', 'manage_books')
- `menu_buttons` (dict): Dictionary storing references to menu item widgets for dynamic updates
- `menu_items` (list): List of tuples defining menu structure (title, icon, section_id)

**Key Components:**
- **Header Bar**: Contains hamburger menu button, section title, and logout button
- **Content Area**: ScrollView with dynamic content based on selected section
- **Navigation Drawer**: 250dp wide sidebar that slides from left
- **Overlay**: Semi-transparent dark background covering right portion when drawer is open

---

### Methods

#### `__init__(**kwargs)`
Initialize admin dashboard screen.
- Sets `drawer_open` to False (drawer starts hidden)
- Sets `current_section` to 'dashboard' (default view)
- Calls `build_ui()` to construct the interface

#### `build_ui()`
Constructs the complete admin dashboard user interface.

**Layout Structure:**
```
FloatLayout (root)
├── BoxLayout (content_container)
│   ├── Header (56dp height)
│   └── ScrollView (content_scroll)
├── BoxLayout (drawer - 250dp width)
│   ├── Drawer Header (100dp height)
│   ├── Menu Items (280dp height)
│   └── Spacer (fills remaining space)
└── Widget (overlay - right side only)
```

**Header Components:**
- Hamburger menu button (MDIconButton with "menu" icon)
- Section title (MDLabel showing current page name)
- Logout button (MDIconButton with "logout" icon)

**Drawer Components:**
- Close button (X icon in top-right of drawer header)
- "ADMIN PANEL" title with admin username
- 5 menu items with icons and text
- Bottom spacer to push content to top

**Menu Items:**
Each menu item is a clickable row containing:
- Material Design icon (left side)
- Text label (right side)
- Background highlight for selected state
- Full-row click detection using ButtonBehavior

#### `toggle_drawer(instance)`
Toggle drawer between open and closed states.
- Called by hamburger menu button
- Calls `open_drawer()` if closed, `close_drawer()` if open

#### `open_drawer()`
Animate drawer sliding in from left side.
- Sets `drawer_open = True`
- Animates drawer position from `(Window.width * -1, 0)` to `(0, 0)` in 0.3 seconds
- Fades in overlay from opacity 0 to 1
- Uses cubic easing for smooth motion

#### `close_drawer()`
Animate drawer sliding out to left (off-screen).
- Sets `drawer_open = False`
- Animates drawer position from `(0, 0)` to `(Window.width * -1, 0)` in 0.3 seconds
- Fades out overlay from opacity 1 to 0
- Uses cubic easing for smooth motion

#### `close_drawer_on_overlay(instance, touch)`
Handle clicks on dark overlay to close drawer.
- Checks if drawer is open and overlay is visible
- Uses `collide_point()` to detect if click is within overlay bounds
- Calls `close_drawer()` if click detected
- Returns True if click was handled, False otherwise

#### `update_menu_selection()`
Update visual state of all menu items to highlight current selection.

**For Selected Item:**
- Background: Light blue tint (rgba: 0.2, 0.6, 1, 0.15)
- Icon color: Blue (0.2, 0.6, 1, 1)
- Text color: Blue (0.2, 0.6, 1, 1)
- Font style: Subtitle1 (bold)

**For Unselected Items:**
- Background: Transparent (rgba: 0, 0, 0, 0)
- Icon color: Gray (0.4, 0.4, 0.4, 1)
- Text color: Dark gray (0.2, 0.2, 0.2, 1)
- Font style: Body1 (normal)

#### `navigate_to(section, title)`
Handle navigation when menu item is clicked.
- Updates `current_section` to new section ID
- Updates header title to display new section name
- Calls `update_menu_selection()` to highlight new selection
- Calls `load_section()` to load content for new section
- Closes drawer automatically

#### `load_section(section)`
Clear current content and load the appropriate section.
- Clears all widgets from `content_scroll`
- Routes to appropriate loader method based on section ID:
  - 'dashboard' → `load_dashboard()`
  - 'manage_books' → `load_manage_books()`
  - 'manage_users' → `load_manage_users()`
  - 'admin_authentication' → `load_admin_auth()`
  - 'system_settings' → `load_settings()`

#### `load_dashboard()`
Display dashboard with statistics and overview.
- Shows welcome message
- Displays total books count from database
- Displays total users count from database
- Shows quick action cards in vertical layout

#### `load_manage_books()`
Display book management interface.
- Shows 5 action cards for book operations:
  - Add New Book
  - Import Books from JSON/CSV
  - Edit Books
  - Delete Books
  - Search Books

#### `load_manage_users()`
Display user management interface.
- Shows 5 action cards for user operations:
  - View All Users
  - User Details
  - Edit Permissions
  - Delete Users
  - Login History

#### `load_admin_auth()`
Display admin authentication management interface.
- Shows 5 action cards for admin operations:
  - Add Admin
  - Change Password
  - Admin Roles
  - Activity Log
  - Security Settings

#### `load_settings()`
Display system settings interface.
- Shows 5 action cards for settings:
  - Database Config
  - App Preferences
  - Security
  - Backup/Restore
  - About

#### `logout(instance)`
Handle logout action.
- Changes screen to 'login' using ScreenManager
- Returns user to login screen

#### Canvas Update Methods
These methods keep background rectangles synchronized with widget size/position:
- `_update_header_rect()`: Updates header background
- `_update_content_rect()`: Updates content area background
- `_update_drawer_rect()`: Updates drawer background
- `_update_drawer_header_rect()`: Updates drawer header background
- `_update_overlay_rect()`: Updates overlay background

---

### Layout Positioning Details

**Kivy Coordinate System:**
- Origin (0, 0) is at bottom-left corner
- Y-axis increases upward
- Widgets in vertical BoxLayout are added top-to-bottom

**Drawer Widget Order:**
Widgets must be added in specific order to appear correctly:
1. `drawer_header` (added first → appears at top)
2. `menu_container` (added second → appears in middle)
3. `bottom_spacer` (added last → fills bottom space)

**Overlay Positioning:**
- Size: `(Window.width - 250dp, Window.height)` - covers only right portion
- Position: `(250dp, 0)` - starts after drawer width
- This creates effect where only content area is darkened, not the drawer itself

---

### Animation Specifications

**Drawer Animation:**
- Duration: 0.3 seconds
- Easing: 'out_cubic' (fast start, smooth end)
- Property: Absolute position (x, y coordinates)
- Open position: (0, 0)
- Closed position: (Window.width * -1, 0)

**Overlay Animation:**
- Duration: 0.3 seconds (synchronized with drawer)
- Property: Opacity
- Open state: opacity = 1
- Closed state: opacity = 0

---

### Color Scheme

**Header:**
- Background: Blue (0.2, 0.6, 1, 1)
- Text: White (1, 1, 1, 1)

**Drawer:**
- Background: Light gray (0.95, 0.95, 0.97, 1)
- Header background: Blue (0.2, 0.6, 1, 1)

**Content Area:**
- Background: Off-white (0.98, 0.98, 0.98, 1)

**Menu Items:**
- Selected background: Light blue tint (0.2, 0.6, 1, 0.15)
- Selected text/icon: Blue (0.2, 0.6, 1, 1)
- Unselected text: Dark gray (0.2, 0.2, 0.2, 1)
- Unselected icon: Medium gray (0.4, 0.4, 0.4, 1)

**Overlay:**
- Semi-transparent black (0, 0, 0, 0.5)

