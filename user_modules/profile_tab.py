"""
Profile Tab - User Control Center
User Info + Reading History + Watchlist + Reviews + Logout
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
import sqlite3


def load_profile_tab(content_scroll, parent_instance):
    """Load profile tab content"""
    content_scroll.clear_widgets()
    
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(15),
        padding=dp(15)
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # Header
    header = MDLabel(
        text="My Profile",
        font_style='H5',
        bold=True,
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(40)
    )
    main_container.add_widget(header)
    
    # Get user info
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, phone FROM users WHERE id = ?", (parent_instance.user_id,))
    user = cursor.fetchone()
    
    # Get stats
    cursor.execute("SELECT COUNT(*) FROM reading_history WHERE user_id = ?", (parent_instance.user_id,))
    books_read = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM watchlist WHERE user_id = ?", (parent_instance.user_id,))
    watchlist_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM book_reviews WHERE user_id = ?", (parent_instance.user_id,))
    reviews_count = cursor.fetchone()[0]
    
    conn.close()
    
    # ==================== USER INFO CARD ====================
    user_card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(100),
        padding=dp(15),
        spacing=dp(8)
    )
    
    with user_card.canvas.before:
        Color(1, 1, 1, 1)
        user_card.bg = RoundedRectangle(
            size=user_card.size,
            pos=user_card.pos,
            radius=[dp(12)]
        )
        Color(0.13, 0.59, 0.95, 0.1)
        user_card.highlight = RoundedRectangle(
            size=user_card.size,
            pos=user_card.pos,
            radius=[dp(12)]
        )
    
    def update_user_bg(instance, value):
        user_card.bg.size = instance.size
        user_card.bg.pos = instance.pos
        user_card.highlight.size = instance.size
        user_card.highlight.pos = instance.pos
    
    user_card.bind(size=update_user_bg, pos=update_user_bg)
    
    user_card.add_widget(MDLabel(
        text=f"👤 {user[0] if user else 'User'}",
        font_style='H6',
        bold=True,
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(30)
    ))
    
    if user and user[1]:
        user_card.add_widget(MDLabel(
            text=f"📧 {user[1]}",
            font_style='Body2',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(20)
        ))
    
    user_card.add_widget(MDLabel(
        text="✅ Active",
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(0.30, 0.69, 0.31, 1),
        size_hint_y=None,
        height=dp(18)
    ))
    
    main_container.add_widget(user_card)
    
    # ==================== READING HISTORY CARD ====================
    history_card = create_stat_card("📚 Books Read", books_read, "View All")
    main_container.add_widget(history_card)
    
    # ==================== WATCHLIST CARD ====================
    watchlist_card = create_stat_card("⭐ Saved Books", watchlist_count, "View Watchlist")
    main_container.add_widget(watchlist_card)
    
    # ==================== REVIEWS CARD ====================
    reviews_card = create_stat_card("✍️ My Reviews", reviews_count, "View All")
    main_container.add_widget(reviews_card)
    
    # ==================== LOGOUT CARD ====================
    logout_card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(80),
        padding=dp(15),
        spacing=dp(10)
    )
    
    with logout_card.canvas.before:
        Color(1, 1, 1, 1)
        logout_card.bg = RoundedRectangle(
            size=logout_card.size,
            pos=logout_card.pos,
            radius=[dp(12)]
        )
    
    logout_card.bind(
        size=lambda inst, val, bg=logout_card: setattr(bg.bg, 'size', inst.size),
        pos=lambda inst, val, bg=logout_card: setattr(bg.bg, 'pos', inst.pos)
    )
    
    logout_card.add_widget(MDLabel(
        text="🚪 Logout",
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(25)
    ))
    
    def show_logout_dialog(instance):
        """Show logout confirmation"""
        dialog = MDDialog(
            title="Confirm Logout",
            text="Are you sure you want to logout?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="LOGOUT",
                    md_bg_color=(0.96, 0.26, 0.21, 1),
                    on_release=lambda x: perform_logout(dialog, parent_instance)
                )
            ]
        )
        dialog.open()
    
    def perform_logout(dialog, parent):
        """Perform logout"""
        dialog.dismiss()
        # Navigate back to login screen
        parent.manager.current = 'login'
    
    logout_btn = MDRaisedButton(
        text="LOGOUT",
        size_hint_y=None,
        height=dp(40),
        md_bg_color=(0.96, 0.26, 0.21, 1),
        on_release=show_logout_dialog
    )
    logout_card.add_widget(logout_btn)
    
    main_container.add_widget(logout_card)
    content_scroll.add_widget(main_container)


def create_stat_card(title, count, button_text):
    """Create a stat card (reusable)"""
    card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(100),
        padding=dp(15),
        spacing=dp(10)
    )
    
    with card.canvas.before:
        Color(1, 1, 1, 1)
        card.bg = RoundedRectangle(
            size=card.size,
            pos=card.pos,
            radius=[dp(12)]
        )
    
    card.bind(
        size=lambda inst, val, bg=card: setattr(bg.bg, 'size', inst.size),
        pos=lambda inst, val, bg=card: setattr(bg.bg, 'pos', inst.pos)
    )
    
    card.add_widget(MDLabel(
        text=title,
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(25)
    ))
    
    card.add_widget(MDLabel(
        text=f"Total: {count} {'book' if count == 1 else 'books' if 'Books' in title else 'review' if count == 1 else 'reviews'}",
        font_style='Body2',
        theme_text_color='Secondary',
        size_hint_y=None,
        height=dp(20)
    ))
    
    view_btn = MDFlatButton(
        text=button_text,
        size_hint_y=None,
        height=dp(36)
    )
    card.add_widget(view_btn)
    
    return card
