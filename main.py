"""
Library Mobile App - Main Application
Multi-option Login: User Login, User Signup, Admin Login
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from database import Database
from admin_modules.admin_dashboard import AdminDashboard
from admin_modules.admin_auth import save_session
from user_modules.user_dashboard import UserDashboard

# Set window size for testing (comment out for mobile deployment)
Window.size = (360, 640)


class LoginScreen(MDScreen):
    """Main Login Screen with User/Admin options"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self.db = Database()
        self.current_mode = 'user_login'  # user_login, user_signup, admin_login
        
        # Main scrollable layout
        scroll = ScrollView()
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None)
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
        
        # Set background color
        with self.main_layout.canvas.before:
            Color(0.95, 0.95, 0.97, 1)  # Light gray background
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Build the UI
        self.build_ui()
        
        scroll.add_widget(self.main_layout)
        self.add_widget(scroll)
        
    def _update_rect(self, instance, value):
        """Update background rectangle"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def build_ui(self):
        """Build the login interface"""
        self.main_layout.clear_widgets()
        
        # Spacer
        self.main_layout.add_widget(Label(size_hint_y=None, height=dp(20)))
        
        # Logo/Title section - Modern Design
        title_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(140), spacing=dp(8))
        
        # Icon container with background
        icon_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(70),
            padding=dp(10)
        )
        
        icon_label = MDIcon(
            icon='book-open-variant',
            theme_text_color='Custom',
            text_color=(0.13, 0.59, 0.95, 1),
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            pos_hint={'center_x': 0.5}
        )
        icon_container.add_widget(icon_label)
        title_box.add_widget(icon_container)
        
        # App name with modern styling
        app_name = MDLabel(
            text="📚 Digital Library",
            font_style='H4',
            halign='center',
            bold=True,
            theme_text_color='Custom',
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=dp(40)
        )
        title_box.add_widget(app_name)
        
        # Subtitle
        subtitle = MDLabel(
            text="Your Knowledge Gateway",
            font_style='Body2',
            halign='center',
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(25)
        )
        title_box.add_widget(subtitle)
        
        self.main_layout.add_widget(title_box)
        
        self.main_layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        
        # Mode selection buttons - Modern tabs
        mode_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(8))
        
        self.user_login_btn = MDRaisedButton(
            text="User Login",
            size_hint=(0.33, None),
            height=dp(50),
            md_bg_color=(0.13, 0.59, 0.95, 1) if self.current_mode == 'user_login' else (0.95, 0.95, 0.95, 1),
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1) if self.current_mode == 'user_login' else (0.3, 0.3, 0.3, 1),
            elevation=3 if self.current_mode == 'user_login' else 0
        )
        self.user_login_btn.bind(on_press=lambda x: self.switch_mode('user_login'))
        
        self.user_signup_btn = MDRaisedButton(
            text="Sign Up",
            size_hint=(0.33, None),
            height=dp(50),
            md_bg_color=(0.13, 0.59, 0.95, 1) if self.current_mode == 'user_signup' else (0.95, 0.95, 0.95, 1),
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1) if self.current_mode == 'user_signup' else (0.3, 0.3, 0.3, 1),
            elevation=3 if self.current_mode == 'user_signup' else 0
        )
        self.user_signup_btn.bind(on_press=lambda x: self.switch_mode('user_signup'))
        
        self.admin_login_btn = MDRaisedButton(
            text="Admin",
            size_hint=(0.34, None),
            height=dp(50),
            md_bg_color=(0.96, 0.26, 0.21, 1) if self.current_mode == 'admin_login' else (0.95, 0.95, 0.95, 1),
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1) if self.current_mode == 'admin_login' else (0.3, 0.3, 0.3, 1),
            elevation=3 if self.current_mode == 'admin_login' else 0
        )
        self.admin_login_btn.bind(on_press=lambda x: self.switch_mode('admin_login'))
        
        mode_box.add_widget(self.user_login_btn)
        mode_box.add_widget(self.user_signup_btn)
        mode_box.add_widget(self.admin_login_btn)
        
        self.main_layout.add_widget(mode_box)
        
        self.main_layout.add_widget(Label(size_hint_y=None, height=dp(20)))
        
        # Form container - auto height
        self.form_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(12))
        self.form_container.bind(minimum_height=self.form_container.setter('height'))
        
        if self.current_mode == 'user_login':
            self.build_user_login_form()
        elif self.current_mode == 'user_signup':
            self.build_user_signup_form()
        else:
            self.build_admin_login_form()
            
        self.main_layout.add_widget(self.form_container)
        
        # Bottom spacer
        self.main_layout.add_widget(Label(size_hint_y=None, height=dp(30)))
        
    def switch_mode(self, mode):
        """Switch between user login, signup, and admin login"""
        self.current_mode = mode
        self.build_ui()
        
    def build_user_login_form(self):
        """Build user login form"""
        self.form_container.clear_widgets()
        
        # Form card container
        form_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(15)
        )
        form_card.bind(minimum_height=form_card.setter('height'))
        
        with form_card.canvas.before:
            Color(1, 1, 1, 1)
            form_card.bg = RoundedRectangle(
                size=form_card.size,
                pos=form_card.pos,
                radius=[dp(16)]
            )
        
        form_card.bind(
            size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
            pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
        )
        
        subtitle = MDLabel(
            text="Welcome Back! 👋",
            font_style='H6',
            halign='center',
            bold=True,
            theme_text_color='Custom',
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=dp(35)
        )
        form_card.add_widget(subtitle)
        
        self.username_field = MDTextField(
            hint_text="👤 Username",
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.username_field)
        
        self.password_field = MDTextField(
            hint_text="🔒 Password",
            password=True,
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.password_field)
        
        login_btn = MDRaisedButton(
            text="LOGIN",
            size_hint=(1, None),
            height=dp(52),
            md_bg_color=(0.13, 0.59, 0.95, 1),
            elevation=3
        )
        login_btn.bind(on_press=self.user_login)
        form_card.add_widget(login_btn)
        
        self.error_label = MDLabel(
            text="",
            halign='center',
            theme_text_color='Error',
            size_hint_y=None,
            height=dp(30)
        )
        form_card.add_widget(self.error_label)
        
        self.form_container.add_widget(form_card)
        
    def build_user_signup_form(self):
        """Build user signup form"""
        self.form_container.clear_widgets()
        
        # Form card container
        form_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(15)
        )
        form_card.bind(minimum_height=form_card.setter('height'))
        
        with form_card.canvas.before:
            Color(1, 1, 1, 1)
            form_card.bg = RoundedRectangle(
                size=form_card.size,
                pos=form_card.pos,
                radius=[dp(16)]
            )
        
        form_card.bind(
            size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
            pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
        )
        
        subtitle = MDLabel(
            text="Create Your Account 🎉",
            font_style='H6',
            halign='center',
            bold=True,
            theme_text_color='Custom',
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=dp(35)
        )
        form_card.add_widget(subtitle)
        
        self.signup_username_field = MDTextField(
            hint_text="👤 Username",
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.signup_username_field)
        
        self.signup_email_field = MDTextField(
            hint_text="📧 Email (optional)",
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.signup_email_field)
        
        self.signup_phone_field = MDTextField(
            hint_text="📱 Phone (optional)",
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.signup_phone_field)
        
        self.signup_password_field = MDTextField(
            hint_text="🔒 Password",
            password=True,
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.signup_password_field)
        
        self.signup_confirm_password_field = MDTextField(
            hint_text="🔐 Confirm Password",
            password=True,
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.signup_confirm_password_field)
        
        signup_btn = MDRaisedButton(
            text="SIGN UP",
            size_hint=(1, None),
            height=dp(52),
            md_bg_color=(0.13, 0.59, 0.95, 1),
            elevation=3
        )
        signup_btn.bind(on_press=self.user_signup)
        form_card.add_widget(signup_btn)
        
        self.error_label = MDLabel(
            text="",
            halign='center',
            theme_text_color='Error',
            size_hint_y=None,
            height=dp(30)
        )
        form_card.add_widget(self.error_label)
        
        self.form_container.add_widget(form_card)
        
    def build_admin_login_form(self):
        """Build admin login form"""
        self.form_container.clear_widgets()
        
        # Form card container
        form_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(15)
        )
        form_card.bind(minimum_height=form_card.setter('height'))
        
        with form_card.canvas.before:
            Color(1, 1, 1, 1)
            form_card.bg = RoundedRectangle(
                size=form_card.size,
                pos=form_card.pos,
                radius=[dp(16)]
            )
        
        form_card.bind(
            size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
            pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
        )
        
        subtitle = MDLabel(
            text="Admin Access 🔒",
            font_style='H6',
            halign='center',
            bold=True,
            theme_text_color='Custom',
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=dp(35)
        )
        form_card.add_widget(subtitle)
        
        info_label = MDLabel(
            text="⚠️ Authorized Personnel Only",
            font_style='Caption',
            halign='center',
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(25)
        )
        form_card.add_widget(info_label)
        
        self.admin_username_field = MDTextField(
            hint_text="🛡️ Admin ID",
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.admin_username_field)
        
        self.admin_password_field = MDTextField(
            hint_text="🔒 Admin Password",
            password=True,
            size_hint_y=None,
            height=dp(56),
            mode="rectangle"
        )
        form_card.add_widget(self.admin_password_field)
        
        admin_login_btn = MDRaisedButton(
            text="ADMIN LOGIN",
            size_hint=(1, None),
            height=dp(52),
            md_bg_color=(0.96, 0.26, 0.21, 1),
            elevation=3
        )
        admin_login_btn.bind(on_press=self.admin_login)
        form_card.add_widget(admin_login_btn)
        
        self.error_label = MDLabel(
            text="",
            halign='center',
            theme_text_color='Error',
            size_hint_y=None,
            height=dp(30)
        )
        form_card.add_widget(self.error_label)
        
        self.form_container.add_widget(form_card)
        
    def user_login(self, instance):
        """Handle user login"""
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Verify user and get user ID
        conn = self.db.connect()
        cursor = conn.cursor()
        password_hash = self.db.hash_password(password)
        cursor.execute(
            'SELECT id, username FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user_id, username = result
            self.show_success_dialog(username, "User", user_id)
        else:
            self.show_error("Invalid username or password")
            
    def user_signup(self, instance):
        """Handle user signup"""
        username = self.signup_username_field.text.strip()
        email = self.signup_email_field.text.strip()
        phone = self.signup_phone_field.text.strip()
        password = self.signup_password_field.text.strip()
        confirm_password = self.signup_confirm_password_field.text.strip()
        
        if not username or not password:
            self.show_error("Username and password are required")
            return
            
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return
            
        if len(password) < 6:
            self.show_error("Password must be at least 6 characters")
            return
        
        # Create user and get ID
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            password_hash = self.db.hash_password(password)
            cursor.execute(
                'INSERT INTO users (username, password_hash, email, phone) VALUES (?, ?, ?, ?)',
                (username, password_hash, email or None, phone or None)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            # Auto-login after successful signup
            dialog = MDDialog(
                title="Success!",
                text=f"Account created successfully! Welcome, {username}!",
                buttons=[
                    MDFlatButton(
                        text="Continue",
                        on_release=lambda x: (dialog.dismiss(), self.go_to_dashboard('User', username, user_id))
                    )
                ]
            )
            dialog.open()
        except Exception as e:
            conn.close()
            self.show_error("Username already exists")
            
    def admin_login(self, instance):
        """Handle admin login"""
        username = self.admin_username_field.text.strip()
        password = self.admin_password_field.text.strip()
        
        if not username or not password:
            self.show_error("Please enter both admin ID and password")
            return
            
        if self.db.verify_admin(username, password):
            # Save session
            save_session(1, username)
            self.show_success_dialog(username, "Admin")
        else:
            self.show_error("Invalid admin credentials")
            
    def show_error(self, message):
        """Display error message"""
        self.error_label.text = message
        
    def show_success_dialog(self, username, user_type, user_id=None):
        """Show attractive success modal on successful login"""
        from kivy.uix.modalview import ModalView
        
        modal = ModalView(
            size_hint=(0.85, None),
            height=dp(320),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.6),
            auto_dismiss=False
        )
        
        modal_content = BoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(20)
        )
        
        with modal_content.canvas.before:
            Color(1, 1, 1, 1)
            modal_content.bg = RoundedRectangle(
                size=modal_content.size,
                pos=modal_content.pos,
                radius=[dp(20)]
            )
        
        modal_content.bind(
            size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
            pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
        )
        
        # Success Icon
        icon_box = BoxLayout(
            size_hint_y=None,
            height=dp(80)
        )
        icon_box.add_widget(BoxLayout())  # Spacer
        
        success_icon = MDLabel(
            text="✓",
            font_style='H1',
            halign='center',
            theme_text_color='Custom',
            text_color=(0.3, 0.8, 0.3, 1),
            size_hint=(None, None),
            size=(dp(80), dp(80))
        )
        icon_box.add_widget(success_icon)
        icon_box.add_widget(BoxLayout())  # Spacer
        modal_content.add_widget(icon_box)
        
        # Success Title
        title = MDLabel(
            text="Login Successful!",
            font_style='H5',
            bold=True,
            halign='center',
            theme_text_color='Custom',
            text_color=(0.13, 0.59, 0.95, 1),
            size_hint_y=None,
            height=dp(40)
        )
        modal_content.add_widget(title)
        
        # Welcome Message
        welcome_msg = MDLabel(
            text=f"Welcome back, {username}! 🎉",
            font_style='Body1',
            halign='center',
            theme_text_color='Custom',
            text_color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(30)
        )
        modal_content.add_widget(welcome_msg)
        
        # Subtext
        subtext = MDLabel(
            text=f"Logging in as {user_type}...",
            font_style='Caption',
            halign='center',
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(25)
        )
        modal_content.add_widget(subtext)
        
        # Continue Button
        continue_btn = MDRaisedButton(
            text="CONTINUE",
            size_hint=(1, None),
            height=dp(52),
            md_bg_color=(0.13, 0.59, 0.95, 1),
            elevation=3,
            on_release=lambda x: (modal.dismiss(), self.go_to_dashboard(user_type, username, user_id))
        )
        modal_content.add_widget(continue_btn)
        
        modal.add_widget(modal_content)
        modal.open()
        
    def go_to_dashboard(self, user_type, username, user_id=None):
        """Navigate to appropriate dashboard"""
        print(f"✓ Navigating to {user_type} dashboard for {username}...")
        
        if user_type == 'Admin':
            self.manager.get_screen('admin_dashboard').set_admin_name(username)
            self.manager.current = 'admin_dashboard'
        else:
            # Navigate to user dashboard
            if 'user_dashboard' not in [screen.name for screen in self.manager.screens]:
                user_dash = UserDashboard(user_id=user_id, username=username, name='user_dashboard')
                self.manager.add_widget(user_dash)
            else:
                # Update existing dashboard
                user_dash = self.manager.get_screen('user_dashboard')
                user_dash.user_id = user_id
                user_dash.username = username
                user_dash.load_home()
            
            self.manager.current = 'user_dashboard'

class LibraryApp(MDApp):
    """Main Application Class"""
    
    def build(self):
        """Build the application"""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        
        # Screen Manager
        sm = ScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(AdminDashboard())
        
        return sm
        
    def on_start(self):
        """Initialize database on app start"""
        print("🚀 Library Mobile App Started")
        db = Database()
        db.create_tables()
        # Create default admin if not exists
        db.create_admin('admin', 'admin123', 'admin@library.com')


if __name__ == '__main__':
    LibraryApp().run()
