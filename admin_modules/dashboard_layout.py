"""
Dashboard Layout Components - Premium Modern Design
Advanced analytics dashboard with beautiful UI and real-time data
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from datetime import datetime, timedelta
import database as db_module


def create_gradient_card(icon_name, value, subtitle, trend, color_start, color_end):
    """
    Create a stunning gradient KPI card with trend indicator
    
    Args:
        icon_name: Material Design icon name (e.g., 'book', 'account', 'download')
        value: Main metric value
        subtitle: Description
        trend: Percentage change (e.g., "+12%")
        color_start: Start color RGBA
        color_end: End color RGBA
    """
    card_container = BoxLayout(
        orientation='vertical',
        size_hint=(0.48, None),
        height=dp(120),
        padding=dp(2)
    )
    
    card = BoxLayout(
        orientation='vertical',
        padding=dp(15),
        spacing=dp(5)
    )
    
    # Gradient background effect (simulated with two layers)
    with card.canvas.before:
        Color(*color_start)
        card.bg_rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(15)])
        Color(*color_end)
        card.gradient_rect = RoundedRectangle(
            size=(card.size[0], card.size[1] * 0.5),
            pos=(card.pos[0], card.pos[1] + card.size[1] * 0.5),
            radius=[dp(15), dp(15), 0, 0]
        )
    
    def update_card_graphics(instance, value):
        card.bg_rect.size = instance.size
        card.bg_rect.pos = instance.pos
        card.gradient_rect.size = (instance.size[0], instance.size[1] * 0.5)
        card.gradient_rect.pos = (instance.pos[0], instance.pos[1] + instance.size[1] * 0.5)
    
    card.bind(size=update_card_graphics, pos=update_card_graphics)
    
    # Top row: Icon and trend
    top_row = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(30)
    )
    
    # Material Design Icon
    icon = MDIcon(
        icon=icon_name,
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        font_size='32sp',
        size_hint_x=0.6,
        halign='left'
    )
    top_row.add_widget(icon)
    
    # Trend indicator
    trend_color = (0.2, 1, 0.4, 1) if '+' in trend else (1, 0.3, 0.3, 1)
    trend_label = MDLabel(
        text=trend,
        font_style='Caption',
        theme_text_color='Custom',
        text_color=trend_color,
        size_hint_x=0.4,
        halign='right',
        bold=True
    )
    top_row.add_widget(trend_label)
    card.add_widget(top_row)
    
    # Main value
    card.add_widget(MDLabel(
        text=str(value),
        font_style='H3',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        size_hint_y=None,
        height=dp(45),
        halign='left',
        bold=True
    ))
    
    # Subtitle
    card.add_widget(MDLabel(
        text=subtitle,
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.85),
        size_hint_y=None,
        height=dp(20),
        halign='left'
    ))
    
    card_container.add_widget(card)
    return card_container


def create_subject_card(subject, count, color):
    """Create simple subject card for mobile"""
    card = BoxLayout(
        orientation='vertical',
        size_hint=(0.5, None),
        height=dp(80),
        padding=dp(12)
    )
    
    with card.canvas.before:
        Color(*color)
        card.bg_rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(10)])
    
    card.bind(
        size=lambda i, v: setattr(i.bg_rect, 'size', i.size),
        pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos)
    )
    
    # Count
    card.add_widget(MDLabel(
        text=str(count),
        font_style='H4',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        bold=True,
        halign='center',
        size_hint_y=None,
        height=dp(40)
    ))
    
    # Subject name
    card.add_widget(MDLabel(
        text=subject[:15] + '...' if len(subject) > 15 else subject,
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        halign='center',
        size_hint_y=None,
        height=dp(20)
    ))
    
    return card


def create_stat_row(label, value, max_value, color):
    """Create beautiful stat row with animated progress bar"""
    container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(50),
        spacing=dp(5)
    )
    
    # Label and value
    label_row = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(20)
    )
    
    label_row.add_widget(MDLabel(
        text=label,
        font_style='Body2',
        size_hint_x=0.7,
        theme_text_color='Secondary'
    ))
    
    label_row.add_widget(MDLabel(
        text=f"{value}/{max_value}",
        font_style='Caption',
        size_hint_x=0.3,
        halign='right',
        theme_text_color='Secondary',
        bold=True
    ))
    
    container.add_widget(label_row)
    
    # Progress bar
    progress_bg = BoxLayout(
        size_hint_y=None,
        height=dp(8)
    )
    
    with progress_bg.canvas.before:
        Color(0.9, 0.9, 0.9, 1)
        progress_bg.bg_rect = RoundedRectangle(
            size=progress_bg.size,
            pos=progress_bg.pos,
            radius=[dp(4)]
        )
    
    progress_bg.bind(
        size=lambda i, v: setattr(i.bg_rect, 'size', i.size),
        pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos)
    )
    
    # Progress fill
    percentage = min((value / max_value * 100) if max_value > 0 else 0, 100)
    progress_fill = Widget(size_hint=(percentage/100, 1))
    
    with progress_fill.canvas.before:
        Color(*color)
        progress_fill.fill_rect = RoundedRectangle(
            size=progress_fill.size,
            pos=progress_fill.pos,
            radius=[dp(4)]
        )
    
    progress_fill.bind(
        size=lambda i, v: setattr(i.fill_rect, 'size', i.size),
        pos=lambda i, v: setattr(i.fill_rect, 'pos', i.pos)
    )
    
    progress_bg.add_widget(progress_fill)
    container.add_widget(progress_bg)
    
    return container


def create_mini_stat_card(title, value, icon_name, bg_color):
    """Create mini statistics card with Material Design icon - mobile optimized"""
    card = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(70),
        padding=dp(15),
        spacing=dp(15)
    )
    
    with card.canvas.before:
        Color(*bg_color)
        card.bg_rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(12)])
    
    card.bind(
        size=lambda i, v: setattr(i.bg_rect, 'size', i.size),
        pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos)
    )
    
    # Material Design Icon - Centered vertically
    icon = MDIcon(
        icon=icon_name,
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        font_size='42sp',
        halign='center',
        valign='middle',
        size_hint_x=None,
        width=dp(50),
        pos_hint={'center_y': 0.5}
    )
    card.add_widget(icon)
    
    # Text
    text_box = BoxLayout(orientation='vertical', size_hint_x=1, spacing=dp(2))
    text_box.add_widget(MDLabel(
        text=str(value),
        font_style='H4',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        bold=True,
        size_hint_y=None,
        height=dp(32)
    ))
    text_box.add_widget(MDLabel(
        text=title,
        font_style='Body2',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        size_hint_y=None,
        height=dp(20)
    ))
    
    card.add_widget(text_box)
    return card


def create_trending_book_card(rank, title, author, views, rating):
    """Create trending book card - clean mobile design"""
    card = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(75),
        padding=dp(12),
        spacing=dp(10)
    )
    
    with card.canvas.before:
        Color(1, 1, 1, 1)
        card.bg_rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(12)])
    
    card.bind(
        size=lambda i, v: setattr(i.bg_rect, 'size', i.size),
        pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos)
    )
    
    # Rank number
    rank_label = MDLabel(
        text=str(rank),
        font_style='H5',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        bold=True,
        halign='center',
        size_hint_x=None,
        width=dp(30)
    )
    card.add_widget(rank_label)
    
    # Book info
    info_box = BoxLayout(
        orientation='vertical',
        spacing=dp(3),
        size_hint_x=1
    )
    
    # Title
    info_box.add_widget(MDLabel(
        text=title[:28] + "..." if len(title) > 28 else title,
        font_style='Body2',
        bold=True,
        theme_text_color='Primary'
    ))
    
    # Author
    if author:
        info_box.add_widget(MDLabel(
            text=author[:30] + "..." if len(author) > 30 else author,
            font_style='Caption',
            theme_text_color='Secondary'
        ))
    
    # Stats
    stats_box = BoxLayout(
        orientation='horizontal',
        spacing=dp(10),
        size_hint_y=None,
        height=dp(18)
    )
    
    # Rating with star
    rating_container = BoxLayout(
        orientation='horizontal',
        size_hint_x=None,
        width=dp(50),
        spacing=dp(2)
    )
    star_icon = MDIcon(
        icon='star',
        theme_text_color='Custom',
        text_color=(1, 0.76, 0.03, 1),
        font_size='14sp',
        size_hint_x=None,
        width=dp(14)
    )
    rating_container.add_widget(star_icon)
    rating_container.add_widget(MDLabel(
        text=f"{rating:.1f}",
        font_style='Caption',
        bold=True,
        theme_text_color='Primary'
    ))
    stats_box.add_widget(rating_container)
    
    # Views
    views_container = BoxLayout(
        orientation='horizontal',
        spacing=dp(2),
        size_hint_x=1
    )
    eye_icon = MDIcon(
        icon='eye',
        theme_text_color='Secondary',
        font_size='14sp',
        size_hint_x=None,
        width=dp(14)
    )
    views_container.add_widget(eye_icon)
    views_container.add_widget(MDLabel(
        text=f"{views}",
        font_style='Caption',
        theme_text_color='Secondary'
    ))
    stats_box.add_widget(views_container)
    
    info_box.add_widget(stats_box)
    card.add_widget(info_box)
    
    return card


def load_dashboard_content(content_scroll, navigate_callback):
    """
    Load the modern premium dashboard with real-time analytics
    
    Args:
        content_scroll: ScrollView to load content into
        navigate_callback: Function to handle navigation
    """
    # Clear existing content
    content_scroll.clear_widgets()
    
    # Main container
    main_container = BoxLayout(
        orientation='vertical',
        spacing=dp(15),
        padding=dp(15),
        size_hint_y=None
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # Connect to database
    db = db_module.Database()
    db.connect()
    
    try:
        # ==================== HEADER ====================
        header_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        header_icon = MDIcon(
            icon='chart-line',
            theme_text_color='Primary',
            font_size='32sp',
            size_hint_x=None,
            width=dp(40)
        )
        header_box.add_widget(header_icon)
        
        header_label = MDLabel(
            text="Analytics Dashboard",
            font_style='H4',
            bold=True,
            theme_text_color='Primary',
            size_hint_x=1
        )
        header_box.add_widget(header_label)
        main_container.add_widget(header_box)
        
        # Last updated
        last_updated = MDLabel(
            text=f"Last updated: {datetime.now().strftime('%I:%M %p, %b %d')}",
            font_style='Caption',
            size_hint_y=None,
            height=dp(20),
            theme_text_color='Secondary'
        )
        main_container.add_widget(last_updated)
        
        # ==================== TOP KPI CARDS ====================
        # Fetch real-time statistics
        cursor = db.cursor
        
        # Total books
        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]
        
        # Total views
        cursor.execute("SELECT SUM(views) FROM books")
        total_views = cursor.fetchone()[0] or 0
        
        # Active users (logged in last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE last_login >= datetime('now', '-7 days')
        """)
        active_users = cursor.fetchone()[0]
        
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # KPI Grid
        kpi_grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(250)
        )
        
        # Calculate total books trend (compare with last week)
        cursor.execute("""
            SELECT COUNT(*) FROM books 
            WHERE created_at >= datetime('now', '-14 days') 
            AND created_at < datetime('now', '-7 days')
        """)
        last_week_books = cursor.fetchone()[0]
        cursor.execute("""
            SELECT COUNT(*) FROM books 
            WHERE created_at >= datetime('now', '-7 days')
        """)
        this_week_books = cursor.fetchone()[0]
        books_trend = "+0%"
        if last_week_books > 0:
            pct = int(((this_week_books - last_week_books) / last_week_books) * 100)
            books_trend = f"+{pct}%" if pct > 0 else f"{pct}%"
        elif this_week_books > 0:
            books_trend = "+100%"
        
        # Calculate active users trend
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE last_login >= datetime('now', '-14 days') 
            AND last_login < datetime('now', '-7 days')
        """)
        last_week_active = cursor.fetchone()[0]
        active_trend = "+0%"
        if last_week_active > 0:
            pct = int(((active_users - last_week_active) / last_week_active) * 100)
            active_trend = f"+{pct}%" if pct > 0 else f"{pct}%"
        elif active_users > 0:
            active_trend = "+100%"
        
        # Calculate total users trend
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE created_at >= datetime('now', '-7 days')
        """)
        new_users_week = cursor.fetchone()[0]
        users_trend = f"+{new_users_week}" if new_users_week > 0 else "0"
        
        # Card 1: Total Books
        kpi_grid.add_widget(create_gradient_card(
            "book-multiple", total_books, "Total Books", books_trend,
            (0.13, 0.59, 0.95, 1), (0.25, 0.32, 0.71, 1)  # Blue gradient
        ))
        
        # Card 2: Total Views
        kpi_grid.add_widget(create_gradient_card(
            "eye", total_views, "Total Views", "+0%",
            (0.30, 0.69, 0.31, 1), (0.10, 0.49, 0.20, 1)  # Green gradient
        ))
        
        # Card 3: Active Users
        kpi_grid.add_widget(create_gradient_card(
            "account-group", active_users, "Active Users (7d)", active_trend,
            (0.61, 0.15, 0.69, 1), (0.38, 0.09, 0.44, 1)  # Purple gradient
        ))
        
        # Card 4: Total Users
        kpi_grid.add_widget(create_gradient_card(
            "account-multiple", total_users, "Total Members", users_trend,
            (1, 0.60, 0, 1), (0.90, 0.40, 0, 1)  # Orange gradient
        ))
        
        main_container.add_widget(kpi_grid)
        
        # ==================== QUICK STATS ====================
        cursor.execute("SELECT COUNT(*) FROM reading_sessions WHERE date(start_time) = date('now')")
        active_readers = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(views) FROM books")
        total_views = cursor.fetchone()[0] or 0
        
        stats_header_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(8)
        )
        
        stats_icon = MDIcon(
            icon='information',
            theme_text_color='Primary',
            font_size='24sp',
            size_hint_x=None,
            width=dp(30)
        )
        stats_header_box.add_widget(stats_icon)
        
        stats_label = MDLabel(
            text="Quick Stats",
            font_style='H6',
            bold=True,
            theme_text_color='Primary',
            size_hint_x=1
        )
        stats_header_box.add_widget(stats_label)
        main_container.add_widget(stats_header_box)
        
        # Vertical layout for mobile - one stat per row
        quick_stats = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None
        )
        quick_stats.bind(minimum_height=quick_stats.setter('height'))
        
        quick_stats.add_widget(create_mini_stat_card(
            "Total Views", total_views, "eye", (0.00, 0.74, 0.83, 1)
        ))
        quick_stats.add_widget(create_mini_stat_card(
            "Reading Now", active_readers, "book-open-variant", (0.61, 0.15, 0.69, 1)
        ))
        quick_stats.add_widget(create_mini_stat_card(
            "Total Views", total_views, "eye", (0.96, 0.26, 0.21, 1)
        ))
        
        main_container.add_widget(quick_stats)
        
        # ==================== BOOKS BY SUBJECT ====================
        subject_header_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(8)
        )
        
        subject_icon = MDIcon(
            icon='bookshelf',
            theme_text_color='Primary',
            font_size='24sp',
            size_hint_x=None,
            width=dp(30)
        )
        subject_header_box.add_widget(subject_icon)
        
        subject_label = MDLabel(
            text="Books by Subject",
            font_style='H6',
            bold=True,
            theme_text_color='Primary',
            size_hint_x=1
        )
        subject_header_box.add_widget(subject_label)
        main_container.add_widget(subject_header_box)
        
        # Get all subjects - only valid English ones
        cursor.execute("""
            SELECT subject, COUNT(*) as count 
            FROM books 
            WHERE subject IS NOT NULL 
            AND subject != '' 
            AND TRIM(subject) != '' 
            AND LENGTH(subject) > 2
            AND subject GLOB '*[A-Za-z]*'
            GROUP BY subject 
            ORDER BY count DESC 
            LIMIT 8
        """)
        subjects = cursor.fetchall()
        
        # Filter out subjects with non-ASCII characters
        subjects = [(s, c) for s, c in subjects if all(ord(char) < 128 for char in s)]
        
        # If we have subjects, show them
        if not subjects:
            # No subjects found, skip this section
            pass
        else:
            # Grid layout - 2 columns for mobile
            subject_grid = GridLayout(
                cols=2,
                spacing=dp(8),
                size_hint_y=None
            )
            subject_grid.bind(minimum_height=subject_grid.setter('height'))
            
            colors = [
                (0.13, 0.59, 0.95, 1),  # Blue
                (0.30, 0.69, 0.31, 1),  # Green
                (0.61, 0.15, 0.69, 1),  # Purple
                (1, 0.60, 0, 1),         # Orange
            ]
            
            for idx, (subject, count) in enumerate(subjects):
                color = colors[idx % len(colors)]
                subject_grid.add_widget(create_subject_card(subject, count, color))
            
            main_container.add_widget(subject_grid)
        
        # ==================== TRENDING BOOKS ====================
        trending_header_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            spacing=dp(8)
        )
        
        trending_icon = MDIcon(
            icon='fire',
            theme_text_color='Custom',
            text_color=(1, 0.34, 0, 1),
            font_size='24sp',
            size_hint_x=None,
            width=dp(30)
        )
        trending_header_box.add_widget(trending_icon)
        
        trending_label = MDLabel(
            text="Trending Books",
            font_style='H6',
            bold=True,
            theme_text_color='Primary',
            size_hint_x=1
        )
        trending_header_box.add_widget(trending_label)
        main_container.add_widget(trending_header_box)
        
        # Get most viewed books
        cursor.execute("""
            SELECT title, author, views, rating
            FROM books 
            WHERE views > 0
            ORDER BY views DESC 
            LIMIT 5
        """)
        trending_books = cursor.fetchall()
        
        trending_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8)
        )
        trending_container.bind(minimum_height=trending_container.setter('height'))
        
        for idx, book in enumerate(trending_books, 1):
            title, author, views, rating = book
            trending_container.add_widget(
                create_trending_book_card(idx, title, author, views, rating)
            )
        
        main_container.add_widget(trending_container)
        
        # ==================== QUICK ACTIONS ====================
        actions_header_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            spacing=dp(8)
        )
        
        actions_icon = MDIcon(
            icon='flash',
            theme_text_color='Primary',
            font_size='24sp',
            size_hint_x=None,
            width=dp(30)
        )
        actions_header_box.add_widget(actions_icon)
        
        actions_header = MDLabel(
            text="Quick Actions",
            font_style='H6',
            bold=True,
            theme_text_color='Primary',
            size_hint_x=1
        )
        actions_header_box.add_widget(actions_header)
        main_container.add_widget(actions_header_box)
        
        actions_grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        # Action buttons with icons
        btn_add_book = MDRaisedButton(
            text="Add Book",
            icon="book-plus",
            size_hint_x=0.5,
            md_bg_color=(0.13, 0.59, 0.95, 1),
            on_release=lambda x: navigate_callback("Manage Books")
        )
        actions_grid.add_widget(btn_add_book)
        
        btn_manage_users = MDRaisedButton(
            text="Users",
            icon="account-group",
            size_hint_x=0.5,
            md_bg_color=(0.30, 0.69, 0.31, 1),
            on_release=lambda x: navigate_callback("Manage Users")
        )
        actions_grid.add_widget(btn_manage_users)
        
        main_container.add_widget(actions_grid)
        
        # ==================== FOOTER ====================
        footer = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=(dp(10), dp(15)),
            spacing=dp(8)
        )
        
        with footer.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            footer.bg_rect = RoundedRectangle(
                size=footer.size,
                pos=footer.pos,
                radius=[dp(8)]
            )
        
        footer.bind(
            size=lambda i, v: setattr(i.bg_rect, 'size', i.size),
            pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos)
        )
        
        # Status icon
        status_icon = MDIcon(
            icon='check-circle',
            theme_text_color='Custom',
            text_color=(0.30, 0.69, 0.31, 1),
            font_size='18sp',
            size_hint_x=None,
            width=dp(20)
        )
        footer.add_widget(status_icon)
        
        footer.add_widget(MDLabel(
            text="System Active",
            font_style='Caption',
            size_hint_x=0.4,
            theme_text_color='Secondary'
        ))
        
        # Database icon
        db_icon = MDIcon(
            icon='database',
            theme_text_color='Secondary',
            font_size='18sp',
            size_hint_x=None,
            width=dp(20)
        )
        footer.add_widget(db_icon)
        
        footer.add_widget(MDLabel(
            text=f"SQLite • {total_books} records",
            font_style='Caption',
            size_hint_x=0.6,
            halign='right',
            theme_text_color='Secondary'
        ))
        
        main_container.add_widget(footer)
        
        # Add spacing at bottom
        main_container.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        error_label = MDLabel(
            text=f"⚠️ Error loading dashboard: {str(e)}",
            theme_text_color='Error',
            size_hint_y=None,
            height=dp(40)
        )
        main_container.add_widget(error_label)
    
    finally:
        db.close()
    
    # Add to scroll view
    content_scroll.add_widget(main_container)
