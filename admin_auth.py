"""
Admin Authentication Module - Login, Logout, and Session Management
Clean admin authentication for library management system
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
import sqlite3
import bcrypt
import json
import os


# Session file path
SESSION_FILE = 'admin_session.json'


def save_session(admin_id, username):
    """Save admin session to file"""
    session_data = {
        'admin_id': admin_id,
        'username': username,
        'logged_in': True
    }
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_data, f)


def clear_session():
    """Clear admin session"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


def get_session():
    """Get current admin session"""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None


def is_logged_in():
    """Check if admin is logged in"""
    session = get_session()
    return session and session.get('logged_in', False)


def load_admin_auth_content(content_scroll, parent_instance):
    """Load the Admin Authentication screen"""
    # Clear existing content
    content_scroll.clear_widgets()
    
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(20),
        padding=dp(15)
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # ==================== HEADER ====================
    header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(50),
        spacing=dp(10)
    )
    
    header_icon = MDIcon(
        icon='shield-account',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='32sp',
        size_hint_x=None,
        width=dp(40)
    )
    header_box.add_widget(header_icon)
    
    title_box = BoxLayout(orientation='vertical', size_hint_x=1, spacing=dp(2))
    
    header = MDLabel(
        text="Admin Authentication",
        font_style='H5',
        bold=True,
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(30)
    )
    title_box.add_widget(header)
    
    subtitle = MDLabel(
        text="Manage your admin account",
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_y=None,
        height=dp(18)
    )
    title_box.add_widget(subtitle)
    
    header_box.add_widget(title_box)
    main_container.add_widget(header_box)
    
    # ==================== SESSION INFO CARD ====================
    session = get_session()
    if session and session.get('logged_in'):
        # Account Info Card
        account_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(20),
            spacing=dp(10)
        )
        
        with account_card.canvas.before:
            Color(1, 1, 1, 1)
            account_card.bg = RoundedRectangle(
                size=account_card.size,
                pos=account_card.pos,
                radius=[dp(12)]
            )
            Color(0.13, 0.59, 0.95, 0.1)
            account_card.highlight = RoundedRectangle(
                size=account_card.size,
                pos=account_card.pos,
                radius=[dp(12)]
            )
        
        def update_account_bg(instance, value):
            account_card.bg.size = instance.size
            account_card.bg.pos = instance.pos
            account_card.highlight.size = instance.size
            account_card.highlight.pos = instance.pos
        
        account_card.bind(size=update_account_bg, pos=update_account_bg)
        
        # Card header
        card_header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(8)
        )
        
        card_icon = MDIcon(
            icon='account-check',
            theme_text_color='Custom',
            text_color=(0.30, 0.69, 0.31, 1),
            font_size='24sp',
            size_hint_x=None,
            width=dp(30)
        )
        card_header.add_widget(card_icon)
        
        card_header.add_widget(MDLabel(
            text="Active Session",
            font_style='Subtitle1',
            bold=True,
            theme_text_color='Primary',
            size_hint_x=1
        ))
        
        account_card.add_widget(card_header)
        
        # Account details
        details_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(10)
        )
        
        details_row.add_widget(MDIcon(
            icon='account',
            theme_text_color='Secondary',
            font_size='18sp',
            size_hint_x=None,
            width=dp(25)
        ))
        
        details_row.add_widget(MDLabel(
            text=f"Admin: {session.get('username', 'admin')}",
            font_style='Body1',
            theme_text_color='Primary',
            size_hint_x=1
        ))
        
        account_card.add_widget(details_row)
        
        # Status indicator
        status_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(25),
            spacing=dp(10)
        )
        
        status_row.add_widget(MDIcon(
            icon='check-circle',
            theme_text_color='Custom',
            text_color=(0.30, 0.69, 0.31, 1),
            font_size='16sp',
            size_hint_x=None,
            width=dp(25)
        ))
        
        status_row.add_widget(MDLabel(
            text="Logged in",
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_x=1
        ))
        
        account_card.add_widget(status_row)
        
        main_container.add_widget(account_card)
        
        # ==================== ACTION BUTTONS ====================
        actions_label = MDLabel(
            text="Account Actions",
            font_style='Subtitle1',
            bold=True,
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(35)
        )
        main_container.add_widget(actions_label)
        
        # Define function before using it
        def show_change_password(instance):
            change_pass_dialog = create_change_password_dialog(parent_instance)
            change_pass_dialog.open()
        
        change_pass_btn = MDRaisedButton(
            text="CHANGE PASSWORD",
            pos_hint={'center_x': 0.5},
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            md_bg_color=(0.13, 0.59, 0.95, 1),
            on_release=show_change_password
        )
        change_pass_btn_container = BoxLayout(
            size_hint_y=None,
            height=dp(50)
        )
        change_pass_btn_container.add_widget(Widget())
        change_pass_btn_container.add_widget(change_pass_btn)
        change_pass_btn_container.add_widget(Widget())
        main_container.add_widget(change_pass_btn_container)
        
        # Logout button
        def show_logout_confirmation(instance):
            logout_dialog = MDDialog(
                title="Confirm Logout",
                text="Are you sure you want to logout?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: logout_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="LOGOUT",
                        md_bg_color=(0.96, 0.26, 0.21, 1),
                        on_release=lambda x: perform_logout(logout_dialog)
                    )
                ]
            )
            logout_dialog.open()
        
        def perform_logout(dialog):
            clear_session()
            dialog.dismiss()
            
            # Show success and reload
            success_dialog = MDDialog(
                title="Logged Out",
                text="You have been logged out successfully.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: (success_dialog.dismiss(), parent_instance.load_admin_auth())
                    )
                ]
            )
            success_dialog.open()
        
        logout_btn = MDRaisedButton(
            text="LOGOUT",
            pos_hint={'center_x': 0.5},
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            md_bg_color=(0.96, 0.26, 0.21, 1),
            on_release=show_logout_confirmation
        )
        logout_btn_container = BoxLayout(
            size_hint_y=None,
            height=dp(50)
        )
        logout_btn_container.add_widget(Widget())
        logout_btn_container.add_widget(logout_btn)
        logout_btn_container.add_widget(Widget())
        main_container.add_widget(logout_btn_container)
    else:
        # Not logged in - show message
        not_logged_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Card background
        with not_logged_box.canvas.before:
            Color(1, 0.95, 0.95, 1)
            not_logged_box.bg = RoundedRectangle(
                size=not_logged_box.size,
                pos=not_logged_box.pos,
                radius=[dp(12)]
            )
        
        def update_not_logged_bg(instance, value):
            not_logged_box.bg.size = instance.size
            not_logged_box.bg.pos = instance.pos
        
        not_logged_box.bind(size=update_not_logged_bg, pos=update_not_logged_bg)
        
        # Warning icon
        warning_icon = MDIcon(
            icon='alert-circle-outline',
            theme_text_color='Custom',
            text_color=(0.96, 0.26, 0.21, 1),
            font_size='48sp',
            halign='center',
            size_hint_y=None,
            height=dp(60)
        )
        not_logged_box.add_widget(warning_icon)
        
        not_logged_box.add_widget(MDLabel(
            text="No Active Session",
            font_style='H6',
            bold=True,
            theme_text_color='Custom',
            text_color=(0.96, 0.26, 0.21, 1),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        ))
        
        not_logged_box.add_widget(MDLabel(
            text="Please login to access admin features",
            font_style='Body2',
            theme_text_color='Secondary',
            halign='center',
            size_hint_y=None,
            height=dp(25)
        ))
        
        main_container.add_widget(not_logged_box)
    
    # ==================== SECURITY INFO FOOTER ====================
    main_container.add_widget(Widget(size_hint_y=None, height=dp(15)))
    
    security_footer = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(90),
        padding=dp(15),
        spacing=dp(8)
    )
    
    with security_footer.canvas.before:
        Color(0.97, 0.97, 0.97, 1)
        security_footer.bg = RoundedRectangle(
            size=security_footer.size,
            pos=security_footer.pos,
            radius=[dp(8)]
        )
    
    def update_security_bg(instance, value):
        security_footer.bg.size = instance.size
        security_footer.bg.pos = instance.pos
    
    security_footer.bind(size=update_security_bg, pos=update_security_bg)
    
    # Security header
    sec_header = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(25),
        spacing=dp(8)
    )
    
    sec_header.add_widget(MDIcon(
        icon='shield-lock',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='20sp',
        size_hint_x=None,
        width=dp(25)
    ))
    
    sec_header.add_widget(MDLabel(
        text="Security",
        font_style='Subtitle2',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    ))
    
    security_footer.add_widget(sec_header)
    
    security_footer.add_widget(MDLabel(
        text="🔒 Passwords encrypted with bcrypt",
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_y=None,
        height=dp(18)
    ))
    
    security_footer.add_widget(MDLabel(
        text="🔐 Secure session management",
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_y=None,
        height=dp(18)
    ))
    
    main_container.add_widget(security_footer)
    
    content_scroll.add_widget(main_container)


def create_change_password_dialog(parent_instance):
    """Create change password dialog"""
    content = BoxLayout(
        orientation='vertical',
        spacing=dp(12),
        padding=dp(15),
        size_hint_y=None,
        height=dp(280)
    )
    
    # Title
    title_label = MDLabel(
        text="Change Admin Password",
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(30)
    )
    content.add_widget(title_label)
    
    current_pass = MDTextField(
        hint_text="Current Password",
        password=True,
        mode="rectangle",
        size_hint_y=None,
        height=dp(55)
    )
    content.add_widget(current_pass)
    
    new_pass = MDTextField(
        hint_text="New Password (min 6 characters)",
        password=True,
        mode="rectangle",
        size_hint_y=None,
        height=dp(55)
    )
    content.add_widget(new_pass)
    
    confirm_pass = MDTextField(
        hint_text="Confirm New Password",
        password=True,
        mode="rectangle",
        size_hint_y=None,
        height=dp(55)
    )
    content.add_widget(confirm_pass)
    
    error_label = MDLabel(
        text="",
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(0.96, 0.26, 0.21, 1),
        halign='center',
        size_hint_y=None,
        height=dp(20)
    )
    content.add_widget(error_label)
    
    dialog = MDDialog(
        title="",
        type="custom",
        content_cls=content,
        size_hint=(0.9, None),
        height=dp(450),
        buttons=[]
    )
    
    def change_password(instance):
        # Validation
        if not current_pass.text or not new_pass.text or not confirm_pass.text:
            error_label.text = "⚠️ All fields are required"
            error_label.height = dp(25)
            return
        
        if new_pass.text != confirm_pass.text:
            error_label.text = "⚠️ New passwords don't match"
            error_label.height = dp(25)
            return
        
        if len(new_pass.text) < 6:
            error_label.text = "⚠️ Password must be at least 6 characters"
            error_label.height = dp(25)
            return
        
        # Verify current password
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE id = 1")
        admin = cursor.fetchone()
        
        if not admin or not bcrypt.checkpw(current_pass.text.encode('utf-8'), admin[0]):
            error_label.text = "⚠️ Current password is incorrect"
            error_label.height = dp(25)
            conn.close()
            return
        
        # Update password
        new_hash = bcrypt.hashpw(new_pass.text.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = 1", (new_hash,))
        conn.commit()
        conn.close()
        
        dialog.dismiss()
        
        # Show success
        success_dialog = MDDialog(
            title="Password Changed",
            text="Your password has been changed successfully!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: success_dialog.dismiss()
                )
            ]
        )
        success_dialog.open()
    
    # Dialog buttons - prominent and clearly visible
    dialog.buttons = [
        MDFlatButton(
            text="CANCEL",
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1),
            on_release=lambda x: dialog.dismiss()
        ),
        MDRaisedButton(
            text="SAVE PASSWORD",
            md_bg_color=(0.13, 0.59, 0.95, 1),
            on_release=change_password
        )
    ]
    
    return dialog
