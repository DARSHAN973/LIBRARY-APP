"""
User Dashboard - Bottom Navigation with 4 Tabs
Home | Browse | Search | Profile
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel, MDIcon
from user_modules.home_tab import load_home_tab
from user_modules.browse_tab import load_browse_tab
from user_modules.search_tab import load_search_tab
from user_modules.profile_tab import load_profile_tab


class UserDashboard(MDScreen):
    def __init__(self, user_id, username, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.username = username
        self.current_tab = 'home'
        
        # Main layout
        main_layout = FloatLayout()
        
        # Top bar
        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(56),
            padding=[dp(5), 0],
            pos_hint={'top': 1}
        )
        
        # Top bar background
        with top_bar.canvas.before:
            Color(0.13, 0.59, 0.95, 1)  # Blue
            top_bar.rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        
        def update_top_bar_bg(instance, value):
            top_bar.rect.size = instance.size
            top_bar.rect.pos = instance.pos
        
        top_bar.bind(size=update_top_bar_bg, pos=update_top_bar_bg)
        
        # Library icon
        library_icon = MDLabel(
            text="📚",
            font_style='H6',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        top_bar.add_widget(library_icon)
        
        # App title
        title = MDLabel(
            text="Library",
            font_style='H6',
            bold=True,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint_x=1,
            pos_hint={'center_y': 0.5}
        )
        top_bar.add_widget(title)
        
        # Logout button
        logout_btn = MDIconButton(
            icon='logout',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            icon_size='24sp',
            pos_hint={'center_y': 0.5}
        )
        logout_btn.bind(on_release=self.logout)
        top_bar.add_widget(logout_btn)
        
        main_layout.add_widget(top_bar)
        
        # Content area with scroll
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={'top': 0.9115},  # Below top bar
            padding=[0, 0, 0, dp(56)]  # Space for bottom nav
        )
        
        # ScrollView for content
        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )
        
        # Content container
        self.content_scroll = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(0),
            spacing=dp(0)
        )
        self.content_scroll.bind(minimum_height=self.content_scroll.setter('height'))
        
        scroll.add_widget(self.content_scroll)
        content_layout.add_widget(scroll)
        main_layout.add_widget(content_layout)
        
        # Bottom Navigation
        bottom_nav = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(56),
            pos_hint={'bottom': 1}
        )
        
        # Bottom nav background
        with bottom_nav.canvas.before:
            Color(1, 1, 1, 1)
            bottom_nav.rect = Rectangle(size=bottom_nav.size, pos=bottom_nav.pos)
            Color(0.9, 0.9, 0.9, 1)
            bottom_nav.line = Rectangle(size=(bottom_nav.width, dp(1)), pos=(bottom_nav.x, bottom_nav.y + bottom_nav.height - dp(1)))
        
        def update_bottom_nav_bg(instance, value):
            bottom_nav.rect.size = instance.size
            bottom_nav.rect.pos = instance.pos
            bottom_nav.line.size = (instance.width, dp(1))
            bottom_nav.line.pos = (instance.x, instance.y + instance.height - dp(1))
        
        bottom_nav.bind(size=update_bottom_nav_bg, pos=update_bottom_nav_bg)
        
        # Nav buttons
        self.nav_buttons = {}
        nav_items = [
            ('home', 'home', 'Home'),
            ('browse', 'book-open-page-variant', 'Browse'),
            ('search', 'magnify', 'Search'),
            ('profile', 'account', 'Profile')
        ]
        
        for tab_id, icon, label in nav_items:
            btn_container = BoxLayout(
                orientation='vertical',
                size_hint_x=0.25
            )
            
            btn = MDIconButton(
                icon=icon,
                theme_text_color='Custom',
                text_color=(0.5, 0.5, 0.5, 1) if tab_id != 'home' else (0.13, 0.59, 0.95, 1),
                icon_size='28sp',
                pos_hint={'center_x': 0.5}
            )
            btn.bind(on_release=lambda x, t=tab_id: self.switch_tab(t))
            
            lbl = MDLabel(
                text=label,
                font_style='Caption',
                halign='center',
                theme_text_color='Custom',
                text_color=(0.5, 0.5, 0.5, 1) if tab_id != 'home' else (0.13, 0.59, 0.95, 1),
                size_hint_y=None,
                height=dp(12)
            )
            
            btn_container.add_widget(btn)
            btn_container.add_widget(lbl)
            bottom_nav.add_widget(btn_container)
            
            self.nav_buttons[tab_id] = {'btn': btn, 'lbl': lbl}
        
        main_layout.add_widget(bottom_nav)
        self.add_widget(main_layout)
        
        # Load home tab by default
        self.load_home()
    
    def switch_tab(self, tab_id):
        """Switch between tabs"""
        if self.current_tab == tab_id:
            return
        
        self.current_tab = tab_id
        
        # Update button colors
        for tid, widgets in self.nav_buttons.items():
            if tid == tab_id:
                widgets['btn'].text_color = (0.13, 0.59, 0.95, 1)
                widgets['lbl'].text_color = (0.13, 0.59, 0.95, 1)
            else:
                widgets['btn'].text_color = (0.5, 0.5, 0.5, 1)
                widgets['lbl'].text_color = (0.5, 0.5, 0.5, 1)
        
        # Load content
        if tab_id == 'home':
            self.load_home()
        elif tab_id == 'browse':
            self.load_browse()
        elif tab_id == 'search':
            self.load_search()
        elif tab_id == 'profile':
            self.load_profile()
    
    def load_home(self):
        """Load home tab"""
        load_home_tab(self.content_scroll, self)
    
    def load_browse(self):
        """Load browse tab"""
        load_browse_tab(self.content_scroll, self)
    
    def load_search(self):
        """Load search tab"""
        load_search_tab(self.content_scroll, self)
    
    def load_profile(self):
        """Load profile tab"""
        load_profile_tab(self.content_scroll, self)
    
    def logout(self, instance):
        """Logout user and return to login screen"""
        import json
        # Clear user session
        with open('data/admin_session.json', 'w') as f:
            json.dump({'logged_in': False}, f)
        
        # Navigate back to login screen
        self.manager.current = 'login'
