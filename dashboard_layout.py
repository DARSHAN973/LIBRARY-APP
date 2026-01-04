"""
Dashboard Layout Components - Modern SaaS Style
Separate file for dashboard UI components and data loading
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datetime import datetime
import database as db_module


def create_kpi_card(icon, value, subtitle, color):
    """
    Create a modern KPI card with rounded corners effect
    
    Args:
        icon: Emoji or icon text
        value: Main number to display
        subtitle: Description text
        color: RGBA tuple for background color
    """
    card = BoxLayout(
        orientation='vertical',
        size_hint=(0.5, None),
        height=dp(90),
        padding=dp(10),
        spacing=dp(5)
    )
    
    # Background with color
    with card.canvas.before:
        Color(*color)
        card.color_rect = Rectangle(size=card.size, pos=card.pos)
    card.bind(
        size=lambda i, v: setattr(i.color_rect, 'size', i.size),
        pos=lambda i, v: setattr(i.color_rect, 'pos', i.pos)
    )
    
    # Icon
    card.add_widget(MDLabel(
        text=icon,
        font_style='H5',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        size_hint_y=None,
        height=dp(25),
        halign='center'
    ))
    
    # Value
    card.add_widget(MDLabel(
        text=value,
        font_style='H4',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        size_hint_y=None,
        height=dp(35),
        halign='center'
    ))
    
    # Subtitle
    card.add_widget(MDLabel(
        text=subtitle,
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        size_hint_y=None,
        height=dp(20),
        halign='center'
    ))
    
    return card


def create_progress_row(subject, count, percentage):
    """Create a progress bar row for subject statistics"""
    row = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(28),
        spacing=dp(10),
        padding=(dp(5), 0)
    )
    
    # Subject name
    row.add_widget(MDLabel(
        text=subject,
        font_style='Body2',
        size_hint_x=0.35
    ))
    
    # Progress bar container
    progress_container = BoxLayout(
        orientation='horizontal',
        size_hint_x=0.45,
        size_hint_y=None,
        height=dp(15)
    )
    
    with progress_container.canvas.before:
        Color(0.9, 0.9, 0.9, 1)
        progress_container.bg = Rectangle(size=progress_container.size, pos=progress_container.pos)
    progress_container.bind(
        size=lambda i, v: setattr(i.bg, 'size', i.size),
        pos=lambda i, v: setattr(i.bg, 'pos', i.pos)
    )
    
    # Filled progress bar
    progress_bar = Widget(size_hint=(percentage, 1))
    
    with progress_bar.canvas.before:
        Color(0.2, 0.6, 1, 1)
        progress_bar.bar = Rectangle(size=progress_bar.size, pos=progress_bar.pos)
    progress_bar.bind(
        size=lambda i, v: setattr(i.bar, 'size', i.size),
        pos=lambda i, v: setattr(i.bar, 'pos', i.pos)
    )
    
    progress_container.add_widget(progress_bar)
    row.add_widget(progress_container)
    
    # Count
    row.add_widget(MDLabel(
        text=str(count),
        font_style='Body2',
        theme_text_color='Secondary',
        size_hint_x=0.2,
        halign='right'
    ))
    
    return row


def create_recent_book_row(title, subject, date):
    """Create a row for recently added book"""
    row = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(25),
        spacing=dp(8),
        padding=(dp(5), 0)
    )
    
    row.add_widget(MDLabel(
        text=title,
        font_style='Body2',
        size_hint_x=0.5
    ))
    
    row.add_widget(MDLabel(
        text=subject,
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_x=0.25
    ))
    
    row.add_widget(MDLabel(
        text=date,
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_x=0.25,
        halign='right'
    ))
    
    return row


def create_action_button(text, callback):
    """Create a quick action button"""
    btn = MDRaisedButton(
        text=text,
        size_hint_y=None,
        height=dp(50),
        md_bg_color=(0.2, 0.6, 1, 1),
        on_press=callback
    )
    return btn


def load_dashboard_content(content_scroll, navigate_callback):
    """
    Load complete dashboard with all sections
    
    Args:
        content_scroll: The scrollable content area to add widgets to
        navigate_callback: Function to call for navigation (section, title)
    """
    # Get database statistics
    db = db_module.Database()
    db.connect()
    
    db.cursor.execute("SELECT COUNT(*) FROM books")
    result = db.cursor.fetchone()
    total_books = result[0] if result else 0
    
    db.cursor.execute("SELECT COUNT(*) FROM users")
    result = db.cursor.fetchone()
    total_users = result[0] if result else 0
    
    db.close()
    
    # Main container
    container = BoxLayout(
        orientation='vertical',
        spacing=dp(15),
        size_hint_y=None,
        padding=dp(10)
    )
    container.bind(minimum_height=container.setter('height'))
    
    # === TOP SECTION - KPI CARDS ===
    kpi_title = MDLabel(
        text="📊 Key Performance Indicators",
        font_style='H6',
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(35)
    )
    container.add_widget(kpi_title)
    
    # KPI Row 1
    kpi_row1 = BoxLayout(
        orientation='horizontal',
        spacing=dp(10),
        size_hint_y=None,
        height=dp(90)
    )
    
    kpi_row1.add_widget(create_kpi_card(
        "📚",
        str(total_books),
        "Books available in library",
        (0.2, 0.6, 1, 1)  # Blue
    ))
    
    kpi_row1.add_widget(create_kpi_card(
        "👤",
        str(total_users),
        "Currently active users",
        (0.4, 0.8, 0.4, 1)  # Green
    ))
    
    container.add_widget(kpi_row1)
    
    # KPI Row 2
    kpi_row2 = BoxLayout(
        orientation='horizontal',
        spacing=dp(10),
        size_hint_y=None,
        height=dp(90)
    )
    
    kpi_row2.add_widget(create_kpi_card(
        "🌐",
        "3",
        "English, Hindi, Marathi",
        (1, 0.6, 0.2, 1)  # Orange
    ))
    
    kpi_row2.add_widget(create_kpi_card(
        "📘",
        "18",
        "Unique publishers",
        (0.8, 0.4, 0.8, 1)  # Purple
    ))
    
    container.add_widget(kpi_row2)
    
    # === MIDDLE SECTION - INSIGHTS ===
    insights_title = MDLabel(
        text="📈 Library Insights",
        font_style='H6',
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(40)
    )
    container.add_widget(insights_title)
    
    # Books by Subject Panel
    subject_panel = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(220),
        padding=dp(15),
        spacing=dp(8)
    )
    
    with subject_panel.canvas.before:
        Color(1, 1, 1, 1)
        subject_panel.rect = Rectangle(size=subject_panel.size, pos=subject_panel.pos)
    subject_panel.bind(
        size=lambda i, v: setattr(i.rect, 'size', i.size),
        pos=lambda i, v: setattr(i.rect, 'pos', i.pos)
    )
    
    subject_panel.add_widget(MDLabel(
        text="📊 Books by Subject (Top 5)",
        font_style='Subtitle1',
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(30)
    ))
    
    # Sample data - replace with real database queries later
    subjects_data = [
        ("Computer Science", 320, 0.64),
        ("Biology", 210, 0.42),
        ("Commerce", 180, 0.36),
        ("Mathematics", 140, 0.28),
        ("Others", 395, 0.79)
    ]
    
    for subject, count, percentage in subjects_data:
        subject_panel.add_widget(create_progress_row(subject, count, percentage))
    
    container.add_widget(subject_panel)
    
    # Recently Added Books Panel
    recent_panel = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(195),
        padding=dp(15),
        spacing=dp(6)
    )
    
    with recent_panel.canvas.before:
        Color(1, 1, 1, 1)
        recent_panel.rect = Rectangle(size=recent_panel.size, pos=recent_panel.pos)
    recent_panel.bind(
        size=lambda i, v: setattr(i.rect, 'size', i.size),
        pos=lambda i, v: setattr(i.rect, 'pos', i.pos)
    )
    
    recent_panel.add_widget(MDLabel(
        text="🕒 Recently Added Books",
        font_style='Subtitle1',
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(30)
    ))
    
    # Sample recent books
    recent_books = [
        ("Python Programming", "Computer Sci", "Today"),
        ("Human Biology", "Biology", "Yesterday"),
        ("Financial Accounting", "Commerce", "2 days ago"),
        ("Calculus Basics", "Mathematics", "3 days ago"),
        ("Data Structures", "Computer Sci", "4 days ago")
    ]
    
    for title, subject, date in recent_books:
        recent_panel.add_widget(create_recent_book_row(title, subject, date))
    
    container.add_widget(recent_panel)
    
    # === BOTTOM SECTION - QUICK ACTIONS ===
    actions_title = MDLabel(
        text="⚡ Quick Actions",
        font_style='H6',
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(40)
    )
    container.add_widget(actions_title)
    
    actions_container = BoxLayout(
        orientation='vertical',
        spacing=dp(10),
        size_hint_y=None,
        height=dp(170)
    )
    
    actions_container.add_widget(create_action_button(
        "➕ Add New Book",
        lambda x: navigate_callback('manage_books', 'Manage Books')
    ))
    
    actions_container.add_widget(create_action_button(
        "👥 Manage Users",
        lambda x: navigate_callback('manage_users', 'Manage Users')
    ))
    
    actions_container.add_widget(create_action_button(
        "⚙️ System Settings",
        lambda x: navigate_callback('system_settings', 'Settings')
    ))
    
    container.add_widget(actions_container)
    
    # === FOOTER - SYSTEM STATUS ===
    footer = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(55),
        padding=dp(10),
        spacing=dp(3)
    )
    
    with footer.canvas.before:
        Color(0.95, 0.95, 0.95, 1)
        footer.rect = Rectangle(size=footer.size, pos=footer.pos)
    footer.bind(
        size=lambda i, v: setattr(i.rect, 'size', i.size),
        pos=lambda i, v: setattr(i.rect, 'pos', i.pos)
    )
    
    footer.add_widget(MDLabel(
        text="Database: ✅ Connected  •  Storage: Local (SQLite)",
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_y=None,
        height=dp(20)
    ))
    
    current_time = datetime.now().strftime("%I:%M %p")
    footer.add_widget(MDLabel(
        text=f"Last Updated: Today, {current_time}",
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_y=None,
        height=dp(20)
    ))
    
    container.add_widget(footer)
    
    # Add to scroll view
    content_scroll.add_widget(container)
