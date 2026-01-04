"""
Admin Dashboard Screen - Mobile Optimized
Separate file for better organization
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from dashboard_layout import load_dashboard_content
from manage_books import load_manage_books_content
from manage_users import load_manage_users_content


class AdminDashboard(MDScreen):
    """Admin Dashboard - Mobile optimized with drawer navigation"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'admin_dashboard'
        self.admin_name = ''
        self.current_section = 'dashboard'
        self.drawer_open = False
        self.build_ui()
        
    def set_admin_name(self, admin_name):
        """Set logged-in admin name"""
        self.admin_name = admin_name
        self.admin_label.text = admin_name
        
    def build_ui(self):
        """
        Build mobile-optimized admin dashboard UI
        
        Structure:
        1. Root FloatLayout (allows overlays)
        2. Content Container (header + scrollable content)
        3. Navigation Drawer (slides from left)
        4. Overlay (darkens right side when drawer open)
        """
        # Root layout - FloatLayout allows widgets to overlap
        root = FloatLayout()
        
        # Main content (always visible)
        self.content_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={'x': 0, 'top': 1}  # Align to top
        )
        
        # Header bar
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            padding=(dp(8), 0),
            spacing=dp(10)
        )
        
        with header.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_header_rect, pos=self._update_header_rect)
        
        # Hamburger menu button
        self.menu_btn = MDIconButton(
            icon="menu",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_press=self.toggle_drawer
        )
        header.add_widget(self.menu_btn)
        
        # Section title
        self.section_title = MDLabel(
            text="Dashboard",
            font_style='H6',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint_x=0.6
        )
        header.add_widget(self.section_title)
        
        # Logout button
        logout_btn = MDIconButton(
            icon="logout",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_press=self.logout
        )
        header.add_widget(logout_btn)
        
        self.content_container.add_widget(header)
        
        # Content area with ScrollView
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        
        self.content_scroll = BoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None
        )
        self.content_scroll.bind(minimum_height=self.content_scroll.setter('height'))
        
        with self.content_scroll.canvas.before:
            Color(0.98, 0.98, 0.98, 1)
            self.content_rect = Rectangle(size=self.content_scroll.size, pos=self.content_scroll.pos)
        self.content_scroll.bind(size=self._update_content_rect, pos=self._update_content_rect)
        
        self.load_section('dashboard')
        scroll.add_widget(self.content_scroll)
        self.content_container.add_widget(scroll)
        
        root.add_widget(self.content_container)
        
        # Navigation Drawer (overlay) - Positioned at TOP of screen
        # In Kivy, y=0 is bottom, so we use Window.height to position at top
        self.drawer = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            width=dp(250),
            height=Window.height,  # Full height of screen
            pos=(Window.width * -1, 0),  # Hidden off-screen to the left, starts from bottom
            padding=0,
            spacing=0
        )
        
        with self.drawer.canvas.before:
            Color(0.95, 0.95, 0.97, 1)
            self.drawer_rect = Rectangle(size=self.drawer.size, pos=self.drawer.pos)
        self.drawer.bind(size=self._update_drawer_rect, pos=self._update_drawer_rect)
        
        # Drawer header with close button - ADDED FIRST (will appear at TOP in reverse order)
        drawer_header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=0,
            spacing=0
        )
        
        with drawer_header.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.drawer_header_rect = Rectangle(size=drawer_header.size, pos=drawer_header.pos)
        drawer_header.bind(size=self._update_drawer_header_rect, pos=self._update_drawer_header_rect)
        
        # Close button row
        close_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=(dp(5), 0)
        )
        close_row.add_widget(Label())  # Spacer
        close_btn = MDIconButton(
            icon="close",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_press=lambda x: self.close_drawer()
        )
        close_row.add_widget(close_btn)
        drawer_header.add_widget(close_row)
        
        # Title and admin name
        title_box = BoxLayout(orientation='vertical', padding=(dp(15), 0), spacing=dp(5))
        title_box.add_widget(MDLabel(
            text="ADMIN PANEL",
            font_style='H6',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(25)
        ))
        
        self.admin_label = MDLabel(
            text="Admin",
            font_style='Caption',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(20)
        )
        title_box.add_widget(self.admin_label)
        drawer_header.add_widget(title_box)
        
        # Menu items container
        menu_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(280),  # 5 items x 56dp
            padding=(dp(5), dp(15)),
            spacing=dp(2)
        )
        
        self.menu_items = [
            ("Dashboard", "view-dashboard", "dashboard"),
            ("Manage Books", "book-multiple", "manage_books"),
            ("Manage Users", "account-multiple", "manage_users"),
            ("Manage Users", "account-multiple", "manage_users"),
            ("Admin Auth", "shield-account", "admin_authentication"),
            ("Settings", "cog", "system_settings")
        ]
        
        # Import ButtonBehavior at top of method
        from kivy.uix.behaviors import ButtonBehavior
        
        class ClickableBox(ButtonBehavior, BoxLayout):
            pass
        
        self.menu_buttons = {}
        for item_text, icon, section_id in self.menu_items:
            # Container for each menu item
            item_container = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(50),
                padding=(dp(15), dp(5)),
                spacing=dp(15)
            )
            
            # Add background rectangle (will be updated on selection)
            with item_container.canvas.before:
                item_container.bg_color = Color(0, 0, 0, 0)  # Transparent initially
                item_container.bg_rect = Rectangle(size=item_container.size, pos=item_container.pos)
            item_container.bind(
                size=lambda i, v: setattr(i.bg_rect, 'size', i.size),
                pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos)
            )
            
            # Icon
            icon_btn = MDIconButton(
                icon=icon,
                theme_text_color="Custom",
                text_color=(0.4, 0.4, 0.4, 1),
                size_hint_x=None,
                width=dp(40)
            )
            item_container.add_widget(icon_btn)
            
            # Text label
            text_label = MDLabel(
                text=item_text,
                theme_text_color='Custom',
                text_color=(0.2, 0.2, 0.2, 1),
                font_style='Body1',
                size_hint_x=1
            )
            item_container.add_widget(text_label)
            
            # Make entire container clickable
            clickable_item = ClickableBox(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(50)
            )
            clickable_item.add_widget(item_container)
            clickable_item.bind(on_press=lambda x, s=section_id, t=item_text: self.navigate_to(s, t))
            
            # Store references to update later
            self.menu_buttons[section_id] = {
                'container': item_container,
                'icon': icon_btn,
                'label': text_label
            }
            
            menu_container.add_widget(clickable_item)
        
        # Highlight initial selection
        self.update_menu_selection()
        
        # Add widgets in REVERSE order (last added appears at top)
        # Bottom spacer to take remaining space
        bottom_spacer = Widget(size_hint_y=1)
        
        # Add to drawer: header first (top), then menu, then spacer (bottom)
        self.drawer.add_widget(drawer_header)   # This will be at TOP
        self.drawer.add_widget(menu_container)  # This will be below header
        self.drawer.add_widget(bottom_spacer)   # This will fill the bottom
        
        root.add_widget(self.drawer)
        
        # Overlay (semi-transparent background on right side only)
        self.overlay = Widget(
            size_hint=(None, None),
            size=(Window.width - dp(250), Window.height),
            pos=(dp(250), 0),
            opacity=0
        )
        
        with self.overlay.canvas.before:
            Color(0, 0, 0, 0.5)
            self.overlay_rect = Rectangle(size=self.overlay.size, pos=self.overlay.pos)
        self.overlay.bind(size=self._update_overlay_rect, pos=self._update_overlay_rect)
        self.overlay.bind(on_touch_down=self.close_drawer_on_overlay)
        
        root.add_widget(self.overlay)
        
        self.add_widget(root)
        
    def toggle_drawer(self, instance):
        """Toggle navigation drawer with animation"""
        if self.drawer_open:
            self.close_drawer()
        else:
            self.open_drawer()
            
    def open_drawer(self):
        """
        Animate drawer sliding in from left side of screen
        Also displays semi-transparent overlay on right portion
        
        Animation: 0.3 seconds with cubic easing for smooth motion
        """
        self.drawer_open = True
        
        # Slide drawer in from left edge to position (0, 0)
        anim = Animation(pos=(0, 0), duration=0.3, t='out_cubic')
        anim.start(self.drawer)
        
        # Fade in the dark overlay (only covers right portion)
        anim_overlay = Animation(opacity=1, duration=0.3)
        anim_overlay.start(self.overlay)
        
    def close_drawer(self):
        """
        Animate drawer sliding out to left (off-screen)
        Also hides the overlay
        
        Animation: 0.3 seconds with cubic easing for smooth motion
        """
        self.drawer_open = False
        
        # Slide drawer off-screen to the left
        anim = Animation(pos=(Window.width * -1, 0), duration=0.3, t='out_cubic')
        anim.start(self.drawer)
        
        # Fade out the overlay
        anim_overlay = Animation(opacity=0, duration=0.3)
        anim_overlay.start(self.overlay)
        
    def close_drawer_on_overlay(self, instance, touch):
        """
        Close drawer when user clicks on the dark overlay area
        Provides intuitive UX - click outside drawer to close it
        
        Args:
            instance: The overlay widget
            touch: Touch event data with position
            
        Returns:
            bool: True if touch was handled (drawer closed), False otherwise
        """
        if self.drawer_open and self.overlay.opacity > 0:
            if self.overlay.collide_point(*touch.pos):
                self.close_drawer()
                return True
        return False
    
    def update_menu_selection(self):
        """Update menu items to highlight the currently selected section"""
        for section_id, widgets in self.menu_buttons.items():
            container = widgets['container']
            icon = widgets['icon']
            label = widgets['label']
            
            if section_id == self.current_section:
                # Selected state: light blue background, blue icon and text, bold font
                container.bg_color.rgba = (0.2, 0.6, 1, 0.15)
                icon.text_color = (0.2, 0.6, 1, 1)
                label.text_color = (0.2, 0.6, 1, 1)
                label.font_style = 'Subtitle1'
            else:
                # Unselected state: transparent background, gray icon, dark text
                container.bg_color.rgba = (0, 0, 0, 0)
                icon.text_color = (0.4, 0.4, 0.4, 1)
                label.text_color = (0.2, 0.2, 0.2, 1)
                label.font_style = 'Body1'
    
    def navigate_to(self, section, title):
        """
        Navigate to a different section from menu
        Updates header title, highlights selected menu item, loads content, and closes drawer
        
        Args:
            section (str): Section ID (e.g., 'dashboard', 'manage_books')
            title (str): Display title for header (e.g., 'Dashboard', 'Manage Books')
        """
        self.current_section = section
        self.section_title.text = title
        self.update_menu_selection()
        self.load_section(section)
        self.close_drawer()
        
    def load_section(self, section):
        """
        Load content for the specified section
        Clears current content and renders new section
        
        Args:
            section (str): Section ID to load
        """
        self.content_scroll.clear_widgets()
        
        if section == 'dashboard':
            self.load_dashboard()
        elif section == 'manage_books':
            self.load_manage_books()
        elif section == 'manage_users':
            self.load_manage_users()
        elif section == 'manage_users':
            self.load_manage_users()
        elif section == 'admin_authentication':
            self.load_admin_auth()
        elif section == 'system_settings':
            self.load_settings()
            
    def load_dashboard(self):
        """Load modern dashboard with KPIs, insights, and quick actions"""
        load_dashboard_content(self.content_scroll, self.navigate_to)
        
    def load_manage_books(self):
        """Load manage books - modern table-based interface"""
        load_manage_books_content(self.content_scroll, self)
    
    def load_manage_users(self):
        """Load manage users - card-based interface"""
        load_manage_users_content(self.content_scroll, self)
        
    def load_manage_users(self):
        """Load manage users - full page"""
        container = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))
        
        # Page title
        title = MDLabel(
            text="👥 Manage Users",
            font_style='H5',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(40)
        )
        container.add_widget(title)
        
        # Description
        desc = MDLabel(
            text="Monitor and control user accounts",
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(30)
        )
        container.add_widget(desc)
        
        # Action cards
        actions = [
            ("View All Users", "👤", "See complete user list"),
            ("User Details", "📋", "Check user information and activity"),
            ("Edit Permissions", "🔐", "Modify user access rights"),
            ("Delete Users", "❌", "Remove user accounts"),
            ("Login History", "📊", "View user login records")
        ]
        
        for action_title, icon, action_desc in actions:
            card = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(70),
                padding=dp(10),
                spacing=dp(10)
            )
            
            with card.canvas.before:
                Color(0.9, 0.95, 0.9, 1)
                card.rect = Rectangle(size=card.size, pos=card.pos)
            card.bind(size=lambda i, v: setattr(i.rect, 'size', i.size))
            card.bind(pos=lambda i, v: setattr(i.rect, 'pos', i.pos))
            
            card.add_widget(MDLabel(
                text=icon,
                font_style='H4',
                size_hint_x=0.2
            ))
            
            text_box = BoxLayout(orientation='vertical', spacing=dp(2))
            text_box.add_widget(MDLabel(
                text=action_title,
                font_style='Subtitle1',
                theme_text_color='Primary',
                size_hint_y=None,
                height=dp(25)
            ))
            text_box.add_widget(MDLabel(
                text=action_desc,
                font_style='Caption',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(20)
            ))
            card.add_widget(text_box)
            
            container.add_widget(card)
        
        self.content_scroll.add_widget(container)
        
    def load_admin_auth(self):
        """Load admin auth - full page"""
        container = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))
        
        # Page title
        title = MDLabel(
            text="🛡️ Admin Authentication",
            font_style='H5',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(40)
        )
        container.add_widget(title)
        
        # Description
        desc = MDLabel(
            text="Manage admin accounts and security",
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(30)
        )
        container.add_widget(desc)
        
        # Action cards
        actions = [
            ("Add Admin", "➕", "Create new admin account"),
            ("Change Password", "🔑", "Update admin password"),
            ("Admin Roles", "👑", "Assign admin permissions"),
            ("Activity Log", "📝", "View admin actions history"),
            ("Security Settings", "🔒", "Configure security options")
        ]
        
        for action_title, icon, action_desc in actions:
            card = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(70),
                padding=dp(10),
                spacing=dp(10)
            )
            
            with card.canvas.before:
                Color(0.95, 0.9, 0.9, 1)
                card.rect = Rectangle(size=card.size, pos=card.pos)
            card.bind(size=lambda i, v: setattr(i.rect, 'size', i.size))
            card.bind(pos=lambda i, v: setattr(i.rect, 'pos', i.pos))
            
            card.add_widget(MDLabel(
                text=icon,
                font_style='H4',
                size_hint_x=0.2
            ))
            
            text_box = BoxLayout(orientation='vertical', spacing=dp(2))
            text_box.add_widget(MDLabel(
                text=action_title,
                font_style='Subtitle1',
                theme_text_color='Primary',
                size_hint_y=None,
                height=dp(25)
            ))
            text_box.add_widget(MDLabel(
                text=action_desc,
                font_style='Caption',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(20)
            ))
            card.add_widget(text_box)
            
            container.add_widget(card)
        
        self.content_scroll.add_widget(container)
        
    def load_settings(self):
        """Load settings - full page"""
        container = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))
        
        # Page title
        title = MDLabel(
            text="⚙️ System Settings",
            font_style='H5',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(40)
        )
        container.add_widget(title)
        
        # Description
        desc = MDLabel(
            text="Configure application preferences",
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(30)
        )
        container.add_widget(desc)
        
        # Action cards
        actions = [
            ("Database Config", "💾", "Database connection settings"),
            ("App Preferences", "🎨", "Customize app appearance"),
            ("Security", "🔐", "Security and privacy options"),
            ("Backup/Restore", "💿", "Data backup and recovery"),
            ("About", "ℹ️", "App version and information")
        ]
        
        for action_title, icon, action_desc in actions:
            card = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(70),
                padding=dp(10),
                spacing=dp(10)
            )
            
            with card.canvas.before:
                Color(0.9, 0.9, 0.95, 1)
                card.rect = Rectangle(size=card.size, pos=card.pos)
            card.bind(size=lambda i, v: setattr(i.rect, 'size', i.size))
            card.bind(pos=lambda i, v: setattr(i.rect, 'pos', i.pos))
            
            card.add_widget(MDLabel(
                text=icon,
                font_style='H4',
                size_hint_x=0.2
            ))
            
            text_box = BoxLayout(orientation='vertical', spacing=dp(2))
            text_box.add_widget(MDLabel(
                text=action_title,
                font_style='Subtitle1',
                theme_text_color='Primary',
                size_hint_y=None,
                height=dp(25)
            ))
            text_box.add_widget(MDLabel(
                text=action_desc,
                font_style='Caption',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(20)
            ))
            card.add_widget(text_box)
            
            container.add_widget(card)
        
        self.content_scroll.add_widget(container)
        
    def _update_header_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size
        
    def _update_content_rect(self, instance, value):
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size
        
    def _update_drawer_rect(self, instance, value):
        self.drawer_rect.pos = instance.pos
        self.drawer_rect.size = instance.size
        
    def _update_drawer_header_rect(self, instance, value):
        self.drawer_header_rect.pos = instance.pos
        self.drawer_header_rect.size = instance.size
        
    def _update_overlay_rect(self, instance, value):
        self.overlay_rect.pos = instance.pos
        self.overlay_rect.size = instance.size
        
    def logout(self, instance):
        """Logout and return to login"""
        self.manager.current = 'login'
        print(f"✓ Admin {self.admin_name} logged out")
