"""
example_ai_dashboard_integration.py
Shows how to add the AI Chat button to the user dashboard.

This is a reference snippet. Copy/adapt this into your user_modules/user_dashboard.py
"""

# Add these imports at the top of user_modules/user_dashboard.py
from ai_chatbot import show_ai_chat
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

# Then in your UserDashboard class, modify the navigation/button area like this:

def build_navigation_bar(self):
    """Build the bottom navigation with AI chat button."""
    nav_box = MDBoxLayout(
        orientation="horizontal",
        spacing=dp(8),
        padding=dp(8),
        size_hint_y=0.12
    )
    
    # Existing navigation buttons
    home_btn = MDRaisedButton(
        text="🏠 Home",
        on_press=lambda x: self.switch_tab("home"),
        size_hint_x=0.2
    )
    nav_box.add_widget(home_btn)
    
    browse_btn = MDRaisedButton(
        text="📖 Browse",
        on_press=lambda x: self.switch_tab("browse"),
        size_hint_x=0.2
    )
    nav_box.add_widget(browse_btn)
    
    search_btn = MDRaisedButton(
        text="🔍 Search",
        on_press=lambda x: self.switch_tab("search"),
        size_hint_x=0.2
    )
    nav_box.add_widget(search_btn)
    
    profile_btn = MDRaisedButton(
        text="👤 Profile",
        on_press=lambda x: self.switch_tab("profile"),
        size_hint_x=0.2
    )
    nav_box.add_widget(profile_btn)
    
    # NEW: AI Chat button
    ai_chat_btn = MDRaisedButton(
        text="🤖 AI",
        on_press=self.open_ai_chat,
        size_hint_x=0.2,
        md_bg_color=(0.2, 0.6, 0.9, 1)  # Blue color
    )
    nav_box.add_widget(ai_chat_btn)
    
    return nav_box

def open_ai_chat(self, instance):
    """Open the AI chat assistant."""
    # Pass current user_id to the chat
    show_ai_chat(user_id=self.user_id)

# ─────────────────────────────────────────────────────────────────────────

# MINIMAL EXAMPLE: Add this to existing user_dashboard.py

# In the build() or __init__ method where you build the UI:

# Get the AI module
try:
    from ai_chatbot import show_ai_chat

    # Example placeholder; replace with actual logged-in user id from your screen state.
    current_user_id = 1
    
    # Add AI button to your navigation
    ai_btn = MDRaisedButton(
        text="🤖 AI Chat",
        on_press=lambda x: show_ai_chat(user_id=current_user_id),
        size_hint_y=None,
        height=dp(50),
        md_bg_color=(0.2, 0.6, 0.9, 1)
    )
    
    # Add it to your navigation box or button container
    # nav_container.add_widget(ai_btn)
    
except ImportError:
    print("AI chatbot module not available")
