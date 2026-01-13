"""
Profile Tab - User Control Center
User Info + Reading History + Watchlist + Logout
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
import sqlite3


def load_profile_tab(content_scroll, parent_instance):
    """Modern Profile Tab with Enhanced UI"""
    content_scroll.clear_widgets()
    
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(18),
        padding=[dp(20), dp(15), dp(20), dp(70)]
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # ========== HEADER SECTION ==========
    header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(50),
        spacing=dp(10)
    )
    
    profile_icon = MDLabel(
        text="👤",
        font_style='H5',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        size_hint=(None, None),
        size=(dp(36), dp(36)),
        pos_hint={'center_y': 0.5}
    )
    header_box.add_widget(profile_icon)
    
    header = MDLabel(
        text="My Profile",
        font_style='H4',
        bold=True,
        theme_text_color='Custom',
        text_color=(0.1, 0.1, 0.1, 1),
        size_hint_x=1,
        pos_hint={'center_y': 0.5}
    )
    header_box.add_widget(header)
    main_container.add_widget(header_box)
    
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
    
    conn.close()
    
    # ==================== USER INFO CARD ====================
    user_card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(100),
        padding=dp(15),
        spacing=dp(6)
    )
    
    with user_card.canvas.before:
        # Gradient-like background
        Color(0.13, 0.59, 0.95, 1)
        user_card.bg = RoundedRectangle(
            size=user_card.size,
            pos=user_card.pos,
            radius=[dp(16)]
        )
    
    user_card.bind(
        size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
        pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
    )
    
    # User icon and name
    user_header = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(32),
        spacing=dp(8)
    )
    
    user_avatar = MDLabel(
        text="👤",
        font_style='H6',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        size_hint=(None, None),
        size=(dp(32), dp(32)),
        pos_hint={'center_y': 0.5}
    )
    user_header.add_widget(user_avatar)
    
    user_name_box = BoxLayout(
        orientation='vertical',
        size_hint_x=1,
        spacing=dp(2)
    )
    
    user_name_box.add_widget(MDLabel(
        text=user[0] if user else 'User',
        font_style='H6',
        bold=True,
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        size_hint_y=None,
        height=dp(24)
    ))
    
    user_name_box.add_widget(MDLabel(
        text="✨ Active Reader",
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        size_hint_y=None,
        height=dp(16)
    ))
    
    user_header.add_widget(user_name_box)
    user_card.add_widget(user_header)
    
    # Email
    if user and user[1]:
        email_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20),
            spacing=dp(6)
        )
        
        email_icon = MDLabel(
            text="📧",
            font_style='Caption',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 0.9),
            size_hint=(None, None),
            size=(dp(18), dp(18)),
            pos_hint={'center_y': 0.5}
        )
        email_box.add_widget(email_icon)
        
        email_box.add_widget(MDLabel(
            text=user[1],
            font_style='Body2',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 0.95),
            size_hint_x=1,
            pos_hint={'center_y': 0.5}
        ))
        user_card.add_widget(email_box)
    
    # Phone
    if user and user[2]:
        phone_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20),
            spacing=dp(6)
        )
        
        phone_icon = MDLabel(
            text="📱",
            font_style='Caption',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 0.9),
            size_hint=(None, None),
            size=(dp(18), dp(18)),
            pos_hint={'center_y': 0.5}
        )
        phone_box.add_widget(phone_icon)
        
        phone_box.add_widget(MDLabel(
            text=user[2],
            font_style='Body2',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 0.95),
            size_hint_x=1,
            pos_hint={'center_y': 0.5}
        ))
        user_card.add_widget(phone_box)
    
    main_container.add_widget(user_card)
    
    # ==================== STATS SECTION HEADER ====================
    stats_header = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(8),
        padding=[dp(5), dp(10), 0, 0]
    )
    
    stats_icon = MDLabel(
        text="📊",
        font_style='H5',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        size_hint=(None, None),
        size=(dp(26), dp(26)),
        pos_hint={'center_y': 0.5}
    )
    stats_header.add_widget(stats_icon)
    
    stats_label = MDLabel(
        text="My Activity",
        font_style='H6',
        bold=True,
        theme_text_color='Custom',
        text_color=(0.2, 0.2, 0.2, 1),
        size_hint_x=1,
        pos_hint={'center_y': 0.5}
    )
    stats_header.add_widget(stats_label)
    main_container.add_widget(stats_header)
    
    # ==================== STATS GRID ====================
    stats_grid = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(120),
        spacing=dp(15)
    )
    
    # Books Read Card
    books_read_card = create_stat_card_modern(
        icon='book-check',
        title='Books Read',
        count=books_read,
        color=(0.30, 0.69, 0.31, 1)
    )
    stats_grid.add_widget(books_read_card)
    
    # Saved Books Card
    saved_books_card = create_stat_card_modern(
        icon='bookmark',
        title='Saved Books',
        count=watchlist_count,
        color=(0.96, 0.61, 0.07, 1)
    )
    stats_grid.add_widget(saved_books_card)
    
    main_container.add_widget(stats_grid)
    
    # ==================== READING HISTORY SECTION ====================
    def show_reading_history(instance):
        """Show reading history in modal view"""
        from kivy.uix.modalview import ModalView
        from kivy.uix.scrollview import ScrollView
        
        modal = ModalView(
            size_hint=(0.9, 0.85),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.6)
        )
        
        modal_content = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        with modal_content.canvas.before:
            Color(0.96, 0.96, 0.98, 1)
            modal_content.bg = RoundedRectangle(
                size=modal_content.size,
                pos=modal_content.pos,
                radius=[dp(16)]
            )
        
        modal_content.bind(
            size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
            pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
        )
        
        # Header
        header_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        header_icon = MDLabel(
            text="📚",
            font_style='H5',
            theme_text_color='Custom',
            text_color=(0.13, 0.59, 0.95, 1),
            size_hint=(None, None),
            size=(dp(32), dp(32)),
            pos_hint={'center_y': 0.5}
        )
        header_box.add_widget(header_icon)
        
        header_label = MDLabel(
            text='Reading History',
            font_style='H5',
            bold=True,
            theme_text_color='Custom',
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_x=1,
            pos_hint={'center_y': 0.5}
        )
        header_box.add_widget(header_label)
        
        close_btn = MDIconButton(
            icon='close',
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1),
            on_release=lambda x: modal.dismiss()
        )
        header_box.add_widget(close_btn)
        modal_content.add_widget(header_box)
        
        # Scroll view for books
        scroll = ScrollView(size_hint=(1, 1))
        books_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10),
            padding=dp(5)
        )
        books_container.bind(minimum_height=books_container.setter('height'))
        
        # Get reading history
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.title, b.author, b.subject, rh.opened_at
            FROM reading_history rh
            JOIN books b ON rh.book_id = b.id
            WHERE rh.user_id = ?
            ORDER BY rh.opened_at DESC
            LIMIT 20
        """, (parent_instance.user_id,))
        history_books = cursor.fetchall()
        conn.close()
        
        if history_books:
            for title, author, subject, opened_at in history_books:
                book_card = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(90),
                    padding=dp(15),
                    spacing=dp(6)
                )
                
                with book_card.canvas.before:
                    Color(1, 1, 1, 1)
                    book_card.bg = RoundedRectangle(
                        size=book_card.size,
                        pos=book_card.pos,
                        radius=[dp(12)]
                    )
                
                book_card.bind(
                    size=lambda inst, val, bg=book_card: setattr(bg.bg, 'size', inst.size),
                    pos=lambda inst, val, bg=book_card: setattr(bg.bg, 'pos', inst.pos)
                )
                
                book_card.add_widget(MDLabel(
                    text=title[:60] + '...' if len(title) > 60 else title,
                    font_style='Subtitle1',
                    bold=True,
                    theme_text_color='Custom',
                    text_color=(0.15, 0.15, 0.15, 1),
                    size_hint_y=None,
                    height=dp(24)
                ))
                
                if author:
                    book_card.add_widget(MDLabel(
                        text=f"by {author[:40]}" + ('...' if len(author) > 40 else ''),
                        font_style='Body2',
                        theme_text_color='Custom',
                        text_color=(0.4, 0.4, 0.4, 1),
                        size_hint_y=None,
                        height=dp(20)
                    ))
                
                meta_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(20),
                    spacing=dp(10)
                )
                
                if subject:
                    meta_box.add_widget(MDLabel(
                        text=f"📚 {subject[:20]}" + ('...' if len(subject) > 20 else ''),
                        font_style='Caption',
                        theme_text_color='Custom',
                        text_color=(0.5, 0.5, 0.5, 1)
                    ))
                
                if opened_at:
                    meta_box.add_widget(MDLabel(
                        text=f"📅 {opened_at}",
                        font_style='Caption',
                        theme_text_color='Custom',
                        text_color=(0.5, 0.5, 0.5, 1)
                    ))
                
                book_card.add_widget(meta_box)
                books_container.add_widget(book_card)
        else:
            books_container.add_widget(MDLabel(
                text="No reading history yet",
                font_style='Body1',
                halign='center',
                theme_text_color='Custom',
                text_color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(40)
            ))
        
        scroll.add_widget(books_container)
        modal_content.add_widget(scroll)
        modal.add_widget(modal_content)
        modal.open()
    
    history_section = create_action_card(
        icon='history',
        title='Reading History',
        subtitle=f'{books_read} books completed',
        button_text='View All',
        icon_color=(0.13, 0.59, 0.95, 1),
        on_button_click=show_reading_history
    )
    main_container.add_widget(history_section)
    
    # ==================== WATCHLIST SECTION ====================
    def show_watchlist(instance):
        """Show watchlist in modal view"""
        from kivy.uix.modalview import ModalView
        from kivy.uix.scrollview import ScrollView
        
        modal = ModalView(
            size_hint=(0.9, 0.85),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.6)
        )
        
        modal_content = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        with modal_content.canvas.before:
            Color(0.96, 0.96, 0.98, 1)
            modal_content.bg = RoundedRectangle(
                size=modal_content.size,
                pos=modal_content.pos,
                radius=[dp(16)]
            )
        
        modal_content.bind(
            size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
            pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
        )
        
        # Header
        header_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        header_icon = MDLabel(
            text="🔖",
            font_style='H5',
            theme_text_color='Custom',
            text_color=(0.96, 0.61, 0.07, 1),
            size_hint=(None, None),
            size=(dp(32), dp(32)),
            pos_hint={'center_y': 0.5}
        )
        header_box.add_widget(header_icon)
        
        header_label = MDLabel(
            text='My Watchlist',
            font_style='H5',
            bold=True,
            theme_text_color='Custom',
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_x=1,
            pos_hint={'center_y': 0.5}
        )
        header_box.add_widget(header_label)
        
        close_btn = MDIconButton(
            icon='close',
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1),
            on_release=lambda x: modal.dismiss()
        )
        header_box.add_widget(close_btn)
        modal_content.add_widget(header_box)
        
        # Scroll view for books
        scroll = ScrollView(size_hint=(1, 1))
        books_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10),
            padding=dp(5)
        )
        books_container.bind(minimum_height=books_container.setter('height'))
        
        # Get watchlist
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.title, b.author, b.subject, w.added_at
            FROM watchlist w
            JOIN books b ON w.book_id = b.id
            WHERE w.user_id = ?
            ORDER BY w.added_at DESC
            LIMIT 20
        """, (parent_instance.user_id,))
        watchlist_books = cursor.fetchall()
        conn.close()
        
        if watchlist_books:
            for title, author, subject, added_at in watchlist_books:
                book_card = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(90),
                    padding=dp(15),
                    spacing=dp(6)
                )
                
                with book_card.canvas.before:
                    Color(1, 1, 1, 1)
                    book_card.bg = RoundedRectangle(
                        size=book_card.size,
                        pos=book_card.pos,
                        radius=[dp(12)]
                    )
                
                book_card.bind(
                    size=lambda inst, val, bg=book_card: setattr(bg.bg, 'size', inst.size),
                    pos=lambda inst, val, bg=book_card: setattr(bg.bg, 'pos', inst.pos)
                )
                
                book_card.add_widget(MDLabel(
                    text=title[:60] + '...' if len(title) > 60 else title,
                    font_style='Subtitle1',
                    bold=True,
                    theme_text_color='Custom',
                    text_color=(0.15, 0.15, 0.15, 1),
                    size_hint_y=None,
                    height=dp(24)
                ))
                
                if author:
                    book_card.add_widget(MDLabel(
                        text=f"by {author[:40]}" + ('...' if len(author) > 40 else ''),
                        font_style='Body2',
                        theme_text_color='Custom',
                        text_color=(0.4, 0.4, 0.4, 1),
                        size_hint_y=None,
                        height=dp(20)
                    ))
                
                meta_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(20),
                    spacing=dp(10)
                )
                
                if subject:
                    meta_box.add_widget(MDLabel(
                        text=f"📚 {subject[:20]}" + ('...' if len(subject) > 20 else ''),
                        font_style='Caption',
                        theme_text_color='Custom',
                        text_color=(0.5, 0.5, 0.5, 1)
                    ))
                
                if added_at:
                    meta_box.add_widget(MDLabel(
                        text=f"⭐ Added {added_at}",
                        font_style='Caption',
                        theme_text_color='Custom',
                        text_color=(0.5, 0.5, 0.5, 1)
                    ))
                
                book_card.add_widget(meta_box)
                books_container.add_widget(book_card)
        else:
            books_container.add_widget(MDLabel(
                text="No books in watchlist yet",
                font_style='Body1',
                halign='center',
                theme_text_color='Custom',
                text_color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(40)
            ))
        
        scroll.add_widget(books_container)
        modal_content.add_widget(scroll)
        modal.add_widget(modal_content)
        modal.open()
    
    watchlist_section = create_action_card(
        icon='bookmark-multiple',
        title='My Watchlist',
        subtitle=f'{watchlist_count} books saved',
        button_text='View Watchlist',
        icon_color=(0.96, 0.61, 0.07, 1),
        on_button_click=show_watchlist
    )
    main_container.add_widget(watchlist_section)
    
    # ==================== LOGOUT SECTION ====================
    logout_section = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(105),
        padding=dp(18),
        spacing=dp(12)
    )
    
    with logout_section.canvas.before:
        Color(1, 1, 1, 1)
        logout_section.bg = RoundedRectangle(
            size=logout_section.size,
            pos=logout_section.pos,
            radius=[dp(14)]
        )
        Color(0.96, 0.26, 0.21, 0.1)
        logout_section.border = Line(
            rounded_rectangle=(
                logout_section.x, logout_section.y,
                logout_section.width, logout_section.height,
                dp(14)
            ),
            width=2
        )
    
    logout_section.bind(
        size=lambda inst, val: [
            setattr(inst.bg, 'size', inst.size),
            setattr(inst.border, 'rounded_rectangle', (
                inst.x, inst.y, inst.width, inst.height, dp(14)
            ))
        ],
        pos=lambda inst, val: [
            setattr(inst.bg, 'pos', inst.pos),
            setattr(inst.border, 'rounded_rectangle', (
                inst.x, inst.y, inst.width, inst.height, dp(14)
            ))
        ]
    )
    
    logout_header = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(30),
        spacing=dp(10)
    )
    
    logout_icon = MDLabel(
        text="🚪",
        font_style='H6',
        theme_text_color='Custom',
        text_color=(0.96, 0.26, 0.21, 1),
        size_hint=(None, None),
        size=(dp(26), dp(26)),
        pos_hint={'center_y': 0.5}
    )
    logout_header.add_widget(logout_icon)
    
    logout_label = MDLabel(
        text="Logout",
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Custom',
        text_color=(0.2, 0.2, 0.2, 1),
        size_hint_x=1,
        pos_hint={'center_y': 0.5}
    )
    logout_header.add_widget(logout_label)
    logout_section.add_widget(logout_header)
    
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
        height=dp(42),
        md_bg_color=(0.96, 0.26, 0.21, 1),
        elevation=2,
        on_release=show_logout_dialog
    )
    logout_section.add_widget(logout_btn)
    
    main_container.add_widget(logout_section)
    content_scroll.add_widget(main_container)


def create_stat_card_modern(icon, title, count, color):
    """Create modern stat card with icon"""
    card = BoxLayout(
        orientation='vertical',
        size_hint_x=0.5,
        size_hint_y=None,
        height=dp(120),
        padding=dp(16),
        spacing=dp(10)
    )
    
    with card.canvas.before:
        Color(1, 1, 1, 1)
        card.bg = RoundedRectangle(
            size=card.size,
            pos=card.pos,
            radius=[dp(14)]
        )
        Color(*color, 0.08)
        card.accent = RoundedRectangle(
            size=card.size,
            pos=card.pos,
            radius=[dp(14)]
        )
    
    card.bind(
        size=lambda inst, val, bg=card: [
            setattr(bg.bg, 'size', inst.size),
            setattr(bg.accent, 'size', inst.size)
        ],
        pos=lambda inst, val, bg=card: [
            setattr(bg.bg, 'pos', inst.pos),
            setattr(bg.accent, 'pos', inst.pos)
        ]
    )
    
    # Icon - map to emoji
    icon_map = {
        'book-check': '✓️',
        'bookmark': '🔖'
    }
    icon_emoji = icon_map.get(icon, '📚')
    
    icon_widget = MDLabel(
        text=icon_emoji,
        font_style='H5',
        theme_text_color='Custom',
        text_color=color,
        size_hint=(None, None),
        size=(dp(36), dp(36))
    )
    card.add_widget(icon_widget)
    
    # Count
    count_label = MDLabel(
        text=str(count),
        font_style='H4',
        bold=True,
        theme_text_color='Custom',
        text_color=(0.1, 0.1, 0.1, 1),
        size_hint_y=None,
        height=dp(40)
    )
    card.add_widget(count_label)
    
    # Title
    title_label = MDLabel(
        text=title,
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(0.5, 0.5, 0.5, 1),
        size_hint_y=None,
        height=dp(18)
    )
    card.add_widget(title_label)
    
    return card


def create_action_card(icon, title, subtitle, button_text, icon_color, on_button_click=None):
    """Create action card with icon and button"""
    card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(125),
        padding=dp(18),
        spacing=dp(10)
    )
    
    with card.canvas.before:
        Color(1, 1, 1, 1)
        card.bg = RoundedRectangle(
            size=card.size,
            pos=card.pos,
            radius=[dp(14)]
        )
    
    card.bind(
        size=lambda inst, val, bg=card: setattr(bg.bg, 'size', inst.size),
        pos=lambda inst, val, bg=card: setattr(bg.bg, 'pos', inst.pos)
    )
    
    # Header with icon
    icon_map = {
        'history': '📚',
        'bookmark-multiple': '🔖'
    }
    icon_emoji = icon_map.get(icon, '📚')
    
    header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(28),
        spacing=dp(10)
    )
    
    icon_widget = MDLabel(
        text=icon_emoji,
        font_style='H6',
        theme_text_color='Custom',
        text_color=icon_color,
        size_hint=(None, None),
        size=(dp(28), dp(28)),
        pos_hint={'center_y': 0.5}
    )
    header_box.add_widget(icon_widget)
    
    title_label = MDLabel(
        text=title,
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Custom',
        text_color=(0.15, 0.15, 0.15, 1),
        size_hint_x=1,
        pos_hint={'center_y': 0.5}
    )
    header_box.add_widget(title_label)
    card.add_widget(header_box)
    
    # Subtitle
    subtitle_label = MDLabel(
        text=subtitle,
        font_style='Body2',
        theme_text_color='Custom',
        text_color=(0.5, 0.5, 0.5, 1),
        size_hint_y=None,
        height=dp(22)
    )
    card.add_widget(subtitle_label)
    
    # Button
    view_btn = MDRaisedButton(
        text=button_text,
        size_hint=(1, None),
        height=dp(40),
        md_bg_color=icon_color,
        elevation=0
    )
    
    if on_button_click:
        view_btn.bind(on_release=on_button_click)
    
    card.add_widget(view_btn)
    
    return card
