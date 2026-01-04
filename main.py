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
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from database import Database
from admin_dashboard import AdminDashboard

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
        self.main_layout.add_widget(Label(size_hint_y=None, height=dp(30)))
        
        # Logo/Title section
        title_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), spacing=dp(5))
        
        icon_label = MDLabel(
            text="[LIBRARY]",
            font_style='H4',
            halign='center',
            size_hint_y=None,
            height=dp(50),
            bold=True
        )
        title_box.add_widget(icon_label)
        
        title = MDLabel(
            text="Mobile Book Collection",
            font_style='Caption',
            halign='center',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(40)
        )
        title_box.add_widget(title)
        
        self.main_layout.add_widget(title_box)
        
        self.main_layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        
        # Mode selection buttons
        mode_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(5))
        
        self.user_login_btn = MDRectangleFlatButton(
            text="User Login",
            size_hint=(0.33, 1),
            md_bg_color=(0.2, 0.6, 1, 1) if self.current_mode == 'user_login' else (1, 1, 1, 1),
            text_color=(1, 1, 1, 1) if self.current_mode == 'user_login' else (0.2, 0.6, 1, 1)
        )
        self.user_login_btn.bind(on_press=lambda x: self.switch_mode('user_login'))
        
        self.user_signup_btn = MDRectangleFlatButton(
            text="Sign Up",
            size_hint=(0.33, 1),
            md_bg_color=(0.2, 0.6, 1, 1) if self.current_mode == 'user_signup' else (1, 1, 1, 1),
            text_color=(1, 1, 1, 1) if self.current_mode == 'user_signup' else (0.2, 0.6, 1, 1)
        )
        self.user_signup_btn.bind(on_press=lambda x: self.switch_mode('user_signup'))
        
        self.admin_login_btn = MDRectangleFlatButton(
            text="Admin",
            size_hint=(0.34, 1),
            md_bg_color=(0.8, 0.3, 0.3, 1) if self.current_mode == 'admin_login' else (1, 1, 1, 1),
            text_color=(1, 1, 1, 1) if self.current_mode == 'admin_login' else (0.8, 0.3, 0.3, 1)
        )
        self.admin_login_btn.bind(on_press=lambda x: self.switch_mode('admin_login'))
        
        mode_box.add_widget(self.user_login_btn)
        mode_box.add_widget(self.user_signup_btn)
        mode_box.add_widget(self.admin_login_btn)
        
        self.main_layout.add_widget(mode_box)
        
        self.main_layout.add_widget(Label(size_hint_y=None, height=dp(15)))
        
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
        
        subtitle = MDLabel(
            text="User Login",
            font_style='Subtitle1',
            halign='center',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(35)
        )
        self.form_container.add_widget(subtitle)
        
        self.username_field = MDTextField(
            hint_text="Username",
            icon_left="account",
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.username_field)
        
        self.password_field = MDTextField(
            hint_text="Password",
            icon_left="lock",
            password=True,
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.password_field)
        
        login_btn = MDRaisedButton(
            text="LOGIN",
            size_hint=(1, None),
            height=dp(48),
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        login_btn.bind(on_press=self.user_login)
        self.form_container.add_widget(login_btn)
        
        self.error_label = MDLabel(
            text="",
            halign='center',
            theme_text_color='Error',
            size_hint_y=None,
            height=dp(30)
        )
        self.form_container.add_widget(self.error_label)
        
    def build_user_signup_form(self):
        """Build user signup form"""
        self.form_container.clear_widgets()
        
        subtitle = MDLabel(
            text="Create New Account",
            font_style='Subtitle1',
            halign='center',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(35)
        )
        self.form_container.add_widget(subtitle)
        
        self.signup_username_field = MDTextField(
            hint_text="Username",
            icon_left="account",
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.signup_username_field)
        
        self.signup_email_field = MDTextField(
            hint_text="Email (optional)",
            icon_left="email",
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.signup_email_field)
        
        self.signup_phone_field = MDTextField(
            hint_text="Phone (optional)",
            icon_left="phone",
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.signup_phone_field)
        
        self.signup_password_field = MDTextField(
            hint_text="Password",
            icon_left="lock",
            password=True,
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.signup_password_field)
        
        self.signup_confirm_password_field = MDTextField(
            hint_text="Confirm Password",
            icon_left="lock-check",
            password=True,
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.signup_confirm_password_field)
        
        signup_btn = MDRaisedButton(
            text="SIGN UP",
            size_hint=(1, None),
            height=dp(48),
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        signup_btn.bind(on_press=self.user_signup)
        self.form_container.add_widget(signup_btn)
        
        self.error_label = MDLabel(
            text="",
            halign='center',
            theme_text_color='Error',
            size_hint_y=None,
            height=dp(30)
        )
        self.form_container.add_widget(self.error_label)
        
    def build_admin_login_form(self):
        """Build admin login form"""
        self.form_container.clear_widgets()
        
        subtitle = MDLabel(
            text="Admin Login",
            font_style='Subtitle1',
            halign='center',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(35)
        )
        self.form_container.add_widget(subtitle)
        
        info_label = MDLabel(
            text="⚠️ Admin Access Only",
            font_style='Caption',
            halign='center',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(25)
        )
        self.form_container.add_widget(info_label)
        
        self.admin_username_field = MDTextField(
            hint_text="Admin ID",
            icon_left="shield-account",
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.admin_username_field)
        
        self.admin_password_field = MDTextField(
            hint_text="Admin Password",
            icon_left="lock",
            password=True,
            size_hint_y=None,
            height=dp(48),
            mode="rectangle"
        )
        self.form_container.add_widget(self.admin_password_field)
        
        admin_login_btn = MDRaisedButton(
            text="ADMIN LOGIN",
            size_hint=(1, None),
            height=dp(48),
            md_bg_color=(0.8, 0.3, 0.3, 1)
        )
        admin_login_btn.bind(on_press=self.admin_login)
        self.form_container.add_widget(admin_login_btn)
        
        self.error_label = MDLabel(
            text="",
            halign='center',
            theme_text_color='Error',
            size_hint_y=None,
            height=dp(30)
        )
        self.form_container.add_widget(self.error_label)
        
    def user_login(self, instance):
        """Handle user login"""
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
            
        if self.db.verify_user(username, password):
            self.show_success_dialog(username, "User")
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
            
        if self.db.create_user(username, password, email or None, phone or None):
            # Auto-login after successful signup
            dialog = MDDialog(
                title="Success!",
                text=f"Account created successfully! Welcome, {username}!",
                buttons=[
                    MDFlatButton(
                        text="Continue",
                        on_release=lambda x: (dialog.dismiss(), self.go_to_dashboard('User', username))
                    )
                ]
            )
            dialog.open()
        else:
            self.show_error("Username already exists")
            
    def admin_login(self, instance):
        """Handle admin login"""
        username = self.admin_username_field.text.strip()
        password = self.admin_password_field.text.strip()
        
        if not username or not password:
            self.show_error("Please enter both admin ID and password")
            return
            
        if self.db.verify_admin(username, password):
            self.show_success_dialog(username, "Admin")
        else:
            self.show_error("Invalid admin credentials")
            
    def show_error(self, message):
        """Display error message"""
        self.error_label.text = message
        
    def show_success_dialog(self, username, user_type):
        """Show success dialog on successful login"""
        dialog = MDDialog(
            title=f"{user_type} Login Successful!",
            text=f"Welcome back, {username}!",
            buttons=[
                MDFlatButton(
                    text="Continue",
                    on_release=lambda x: (dialog.dismiss(), self.go_to_dashboard(user_type, username))
                )
            ]
        )
        dialog.open()
        
    def go_to_dashboard(self, user_type, username):
        """Navigate to appropriate dashboard"""
        print(f"✓ Navigating to {user_type} dashboard for {username}...")
        
        if user_type == 'Admin':
            self.manager.get_screen('admin_dashboard').set_admin_name(username)
            self.manager.current = 'admin_dashboard'
        else:
            # Load user dashboard - coming soon
            print(f"✓ User login not yet implemented. Please use admin account.")
            self.error_label.text = "User dashboard coming soon. Please use admin account."

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
