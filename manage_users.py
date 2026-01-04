"""
Manage Users Module - Mobile-Optimized User Management
Clean, efficient user management for admin dashboard
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from datetime import datetime
import sqlite3


def create_user_card(user_data, view_callback, toggle_status_callback, delete_callback):
    """
    Create a clean mobile-optimized card for a user
    
    Args:
        user_data: tuple (id, username, email, is_active, created_at, last_login)
    """
    user_id, username, email, is_active, created_at, last_login = user_data
    
    card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(110),
        padding=dp(14),
        spacing=dp(10)
    )
    
    # Card background
    with card.canvas.before:
        Color(1, 1, 1, 1)
        card.bg_rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(10)])
        Color(0.85, 0.85, 0.85, 1)
        card.border = Line(rounded_rectangle=(card.x, card.y, card.width, card.height, dp(10)), width=1)
    
    def update_card(instance, value):
        card.bg_rect.size = instance.size
        card.bg_rect.pos = instance.pos
        card.border.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, dp(10))
    
    card.bind(size=update_card, pos=update_card)
    
    # Top row: Username + Status Badge
    top_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), spacing=dp(10))
    
    # User icon
    user_icon = MDIcon(
        icon='account',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='24sp',
        size_hint_x=None,
        width=dp(30)
    )
    top_row.add_widget(user_icon)
    
    # Username
    username_label = MDLabel(
        text=str(username),
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    )
    top_row.add_widget(username_label)
    
    # Status Badge
    status_box = BoxLayout(
        orientation='horizontal',
        size_hint_x=None,
        width=dp(80),
        spacing=dp(4),
        padding=[dp(6), dp(4)]
    )
    
    # Status badge background
    status_color = (0.30, 0.69, 0.31, 0.2) if is_active else (0.96, 0.26, 0.21, 0.2)
    with status_box.canvas.before:
        Color(*status_color)
        status_box.bg = RoundedRectangle(size=status_box.size, pos=status_box.pos, radius=[dp(12)])
    
    def update_status_bg(instance, value):
        status_box.bg.size = instance.size
        status_box.bg.pos = instance.pos
    
    status_box.bind(size=update_status_bg, pos=update_status_bg)
    
    # Status icon
    status_icon = MDIcon(
        icon='check-circle' if is_active else 'close-circle',
        theme_text_color='Custom',
        text_color=(0.30, 0.69, 0.31, 1) if is_active else (0.96, 0.26, 0.21, 1),
        font_size='16sp',
        size_hint_x=None,
        width=dp(20)
    )
    status_box.add_widget(status_icon)
    
    # Status text
    status_label = MDLabel(
        text='Active' if is_active else 'Inactive',
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(0.30, 0.69, 0.31, 1) if is_active else (0.96, 0.26, 0.21, 1),
        size_hint_x=1
    )
    status_box.add_widget(status_label)
    top_row.add_widget(status_box)
    
    card.add_widget(top_row)
    
    # Email / User ID row
    email_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20), spacing=dp(4))
    
    email_icon = MDIcon(
        icon='email',
        theme_text_color='Secondary',
        font_size='14sp',
        size_hint_x=None,
        width=dp(18)
    )
    email_row.add_widget(email_icon)
    
    email_label = MDLabel(
        text=str(email) if email else f'User #{user_id}',
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_x=1
    )
    email_row.add_widget(email_label)
    card.add_widget(email_row)
    
    # Action buttons
    actions_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(32),
        spacing=dp(6)
    )
    
    # View button
    view_btn = MDIconButton(
        icon='eye',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        on_release=lambda x: view_callback(user_id)
    )
    actions_box.add_widget(view_btn)
    
    # Activate/Deactivate button
    toggle_btn = MDIconButton(
        icon='lock-open' if not is_active else 'lock',
        theme_text_color='Custom',
        text_color=(0.30, 0.69, 0.31, 1) if not is_active else (0.96, 0.50, 0.09, 1),
        on_release=lambda x: toggle_status_callback(user_id, is_active)
    )
    actions_box.add_widget(toggle_btn)
    
    # Delete button
    delete_btn = MDIconButton(
        icon='delete',
        theme_text_color='Custom',
        text_color=(0.96, 0.26, 0.21, 1),
        on_release=lambda x: delete_callback(user_id)
    )
    actions_box.add_widget(delete_btn)
    
    card.add_widget(actions_box)
    return card


def load_manage_users_content(content_scroll, parent_instance):
    """
    Main function to load Manage Users interface
    
    Args:
        content_scroll: ScrollView to add content to
        parent_instance: AdminDashboard instance for callbacks
    """
    
    # Main container
    main_container = BoxLayout(
        orientation='vertical',
        spacing=dp(12),
        size_hint_y=None,
        padding=dp(10)
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # State variables
    state = {
        'search_text': ''
    }
    
    # ==================== HEADER ====================
    header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(10)
    )
    
    header_icon = MDIcon(
        icon='account-multiple',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='28sp',
        size_hint_x=None,
        width=dp(35)
    )
    header_box.add_widget(header_icon)
    
    header = MDLabel(
        text="Manage Users",
        font_style='H5',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    )
    header_box.add_widget(header)
    
    # Refresh button
    refresh_btn = MDIconButton(
        icon='refresh',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        on_release=lambda x: load_users(users_container, state, search_field, parent_instance)
    )
    header_box.add_widget(refresh_btn)
    
    main_container.add_widget(header_box)
    
    # ==================== SEARCH BAR ====================
    search_field = MDTextField(
        hint_text="Search users (name / email / ID)",
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    main_container.add_widget(search_field)
    
    # ==================== USERS CONTAINER ====================
    users_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(15)
    )
    users_container.bind(minimum_height=users_container.setter('height'))
    main_container.add_widget(users_container)
    
    # ==================== FOOTER ====================
    footer_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(65),
        padding=dp(15),
        spacing=dp(4)
    )
    
    # Footer background
    with footer_container.canvas.before:
        Color(0.96, 0.96, 0.96, 1)
        footer_container.bg_rect = RoundedRectangle(
            size=footer_container.size,
            pos=footer_container.pos,
            radius=[dp(8)]
        )
    
    def update_footer_bg(instance, value):
        footer_container.bg_rect.size = instance.size
        footer_container.bg_rect.pos = instance.pos
    
    footer_container.bind(size=update_footer_bg, pos=update_footer_bg)
    
    # Footer title
    footer_title = MDLabel(
        text="Library Management System (Admin)",
        font_style='Caption',
        bold=True,
        theme_text_color='Primary',
        halign='center',
        size_hint_y=None,
        height=dp(18)
    )
    footer_container.add_widget(footer_title)
    
    # Footer info
    today = datetime.now().strftime("%B %d, %Y")
    footer_info = MDLabel(
        text=f"DB: SQLite • Last updated: {today}",
        font_style='Caption',
        theme_text_color='Secondary',
        halign='center',
        size_hint_y=None,
        height=dp(16)
    )
    footer_container.add_widget(footer_info)
    
    main_container.add_widget(footer_container)
    
    # Wire up search
    def on_search(instance):
        state['search_text'] = search_field.text
        load_users(users_container, state, search_field, parent_instance)
    
    search_field.bind(on_text_validate=on_search)
    
    # Initial load
    content_scroll.add_widget(main_container)
    Clock.schedule_once(lambda dt: load_users(users_container, state, search_field, parent_instance), 0.1)


def load_users(users_container, state, search_field, parent_instance):
    """Load users with search filter"""
    
    # Clear and show loading indicator
    users_container.clear_widgets()
    
    loading_box = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(120),
        padding=dp(20)
    )
    
    spinner = MDSpinner(
        size_hint=(None, None),
        size=(dp(46), dp(46)),
        pos_hint={'center_x': 0.5},
        active=True
    )
    
    loading_label = MDLabel(
        text="Loading users...",
        font_style='Body1',
        theme_text_color='Secondary',
        halign='center',
        size_hint_y=None,
        height=dp(30)
    )
    
    loading_box.add_widget(spinner)
    loading_box.add_widget(loading_label)
    users_container.add_widget(loading_box)
    
    # Build query
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    query = """
        SELECT id, username, email, is_active, created_at, last_login
        FROM users
        WHERE 1=1
    """
    params = []
    
    # Search filter
    if search_field.text.strip():
        search_term = f"%{search_field.text.strip()}%"
        query += " AND (username LIKE ? OR email LIKE ? OR CAST(id AS TEXT) LIKE ?)"
        params.extend([search_term, search_term, search_term])
    
    query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    users = cursor.fetchall()
    conn.close()
    
    # Clear loading and add users
    users_container.clear_widgets()
    
    if users:
        for user in users:
            card = create_user_card(
                user,
                lambda user_id: show_user_details(user_id, parent_instance),
                lambda user_id, current_status: show_toggle_status_confirmation(user_id, current_status, parent_instance, lambda: load_users(users_container, state, search_field, parent_instance)),
                lambda user_id: show_delete_confirmation(user_id, parent_instance, lambda: load_users(users_container, state, search_field, parent_instance))
            )
            users_container.add_widget(card)
    else:
        # No results
        no_results = MDLabel(
            text="No users found\nTry adjusting your search",
            font_style='Body1',
            theme_text_color='Secondary',
            halign='center',
            size_hint_y=None,
            height=dp(100)
        )
        users_container.add_widget(no_results)


def show_user_details(user_id, parent_instance):
    """Show user details in a modal (read-only)"""
    
    # Get user data
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, email, is_active, created_at, last_login
        FROM users WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return
    
    username, email, is_active, created_at, last_login = user
    
    # Create details container
    details = BoxLayout(
        orientation='vertical',
        spacing=dp(12),
        padding=dp(15),
        size_hint_y=None
    )
    details.bind(minimum_height=details.setter('height'))
    
    # Add details
    def add_detail(label, value, icon_name=None):
        row = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(45), spacing=dp(4))
        
        # Label row with optional icon
        label_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(18), spacing=dp(4))
        
        if icon_name:
            icon = MDIcon(
                icon=icon_name,
                theme_text_color='Secondary',
                font_size='14sp',
                size_hint_x=None,
                width=dp(18)
            )
            label_row.add_widget(icon)
        
        label_row.add_widget(MDLabel(
            text=label,
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(18)
        ))
        row.add_widget(label_row)
        
        row.add_widget(MDLabel(
            text=str(value) if value else 'N/A',
            font_style='Body2',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(25)
        ))
        details.add_widget(row)
    
    add_detail("Username", username, "account")
    add_detail("Email / User ID", email if email else f'User #{user_id}', "email")
    
    # Status with color
    status_text = "✅ Active" if is_active else "❌ Inactive"
    add_detail("Account Status", status_text, "shield-account")
    
    # Format dates
    if created_at:
        try:
            date_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%B %d, %Y at %I:%M %p')
            add_detail("Registered Date", formatted_date, "calendar")
        except:
            add_detail("Registered Date", created_at, "calendar")
    
    if last_login:
        try:
            date_obj = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%B %d, %Y at %I:%M %p')
            add_detail("Last Login", formatted_date, "login")
        except:
            add_detail("Last Login", last_login, "login")
    else:
        add_detail("Last Login", "Never logged in", "login")
    
    # Scroll view for details
    scroll = ScrollView(size_hint=(1, None), height=dp(350))
    scroll.add_widget(details)
    
    # Dialog
    dialog = MDDialog(
        title="User Details",
        type="custom",
        content_cls=scroll,
        buttons=[
            MDFlatButton(
                text="CLOSE",
                on_release=lambda x: dialog.dismiss()
            ),
        ],
    )
    dialog.open()


def show_toggle_status_confirmation(user_id, current_status, parent_instance, refresh_callback):
    """Show confirmation dialog for activate/deactivate"""
    
    # Get username
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return
    
    username = user[0]
    action = "deactivate" if current_status else "activate"
    new_status = 0 if current_status else 1
    
    def confirm_toggle(dialog):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (new_status, user_id))
            conn.commit()
            conn.close()
            
            dialog.dismiss()
            
            # Success message
            success_dialog = MDDialog(
                title="Success",
                text=f"User '{username}' has been {action}d successfully!",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: success_dialog.dismiss())]
            )
            success_dialog.open()
            
            # Refresh list
            if refresh_callback:
                refresh_callback()
        
        except Exception as e:
            error_dialog = MDDialog(
                title="Database Error",
                text=f"Failed to {action} user: {str(e)}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
            )
            error_dialog.open()
    
    # Confirmation dialog
    dialog = MDDialog(
        title="Confirm Action",
        text=f"Are you sure you want to {action} this user?\n\nUsername: {username}",
        buttons=[
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: dialog.dismiss()
            ),
            MDRaisedButton(
                text=action.upper(),
                md_bg_color=(0.30, 0.69, 0.31, 1) if not current_status else (0.96, 0.50, 0.09, 1),
                on_release=lambda x: confirm_toggle(dialog)
            ),
        ],
    )
    dialog.open()


def show_delete_confirmation(user_id, parent_instance, refresh_callback):
    """Show delete confirmation dialog"""
    
    # Get username
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return
    
    username = user[0]
    
    def confirm_delete(dialog):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            
            dialog.dismiss()
            
            # Success message
            success_dialog = MDDialog(
                title="Success",
                text=f"User '{username}' deleted successfully!",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: success_dialog.dismiss())]
            )
            success_dialog.open()
            
            # Refresh list
            if refresh_callback:
                refresh_callback()
        
        except Exception as e:
            error_dialog = MDDialog(
                title="Database Error",
                text=f"Failed to delete user: {str(e)}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
            )
            error_dialog.open()
    
    # Confirmation dialog
    dialog = MDDialog(
        title="Confirm Delete",
        text=f"Are you sure you want to delete this user?\n\nUsername: {username}\n\n⚠️ This action cannot be undone.",
        buttons=[
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: dialog.dismiss()
            ),
            MDRaisedButton(
                text="DELETE",
                md_bg_color=(0.96, 0.26, 0.21, 1),
                on_release=lambda x: confirm_delete(dialog)
            ),
        ],
    )
    dialog.open()
