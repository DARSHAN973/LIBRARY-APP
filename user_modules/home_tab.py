"""
Home Tab - Discovery & Engagement
Welcome + Subjects + Recently Added + Continue Reading
MODERN DESIGN WITH ANIMATIONS
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
import sqlite3


def load_home_tab(content_scroll, parent_instance): 
    """Load home tab content"""
    content_scroll.clear_widgets()
    
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(20),
        padding=[dp(15), dp(15), dp(15), 0]  # Left, Top, Right, Bottom=0
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # ==================== HERO WELCOME CARD ====================
    welcome_card = FloatLayout(
        size_hint_y=None,
        height=dp(140)
    )
    
    # Modern gradient background
    with welcome_card.canvas.before:
        # Gradient with two rounded rectangles
        Color(0.13, 0.59, 0.95, 1)  # Primary blue
        welcome_card.bg1 = RoundedRectangle(
            size=welcome_card.size,
            pos=welcome_card.pos,
            radius=[dp(20)]
        )
        Color(0.10, 0.50, 0.85, 0.5)  # Darker blue overlay
        welcome_card.bg2 = RoundedRectangle(
            size=(welcome_card.width * 0.6, welcome_card.height * 0.8),
            pos=(welcome_card.width * 0.4, welcome_card.y + welcome_card.height * 0.1),
            radius=[dp(20)]
        )
    
    def update_welcome_bg(instance, value):
        welcome_card.bg1.size = instance.size
        welcome_card.bg1.pos = instance.pos
        welcome_card.bg2.size = (instance.width * 0.6, instance.height * 0.8)
        welcome_card.bg2.pos = (instance.width * 0.4, instance.y + instance.height * 0.1)
    
    welcome_card.bind(size=update_welcome_bg, pos=update_welcome_bg)
    
    # Content box
    content_box = BoxLayout(
        orientation='vertical',
        padding=dp(20),
        spacing=dp(8),
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    )
    
    # Greeting with icon
    greeting_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(10)
    )
    
    greeting_icon = MDIcon(
        icon='hand-wave-outline',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        font_size='32sp',
        size_hint=(None, None),
        size=(dp(40), dp(40))
    )
    greeting_box.add_widget(greeting_icon)
    
    greeting_label = MDLabel(
        text=f"Hi, {parent_instance.username}!",
        font_style='H5',
        bold=True,
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        size_hint_x=1
    )
    greeting_box.add_widget(greeting_label)
    
    content_box.add_widget(greeting_box)
    
    subtitle = MDLabel(
        text="Discover your next great read",
        font_style='Subtitle1',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        size_hint_y=None,
        height=dp(25)
    )
    content_box.add_widget(subtitle)
    
    # Stats row
    stats_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(20)
    )
    
    # Get user stats
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reading_history WHERE user_id = ?", (parent_instance.user_id,))
    books_read = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM watchlist WHERE user_id = ?", (parent_instance.user_id,))
    saved_books = cursor.fetchone()[0]
    conn.close()
    
    # Books read stat
    stat1 = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint_x=0.5)
    stat1.add_widget(MDIcon(
        icon='book-check-outline',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        font_size='20sp',
        size_hint=(None, None),
        size=(dp(24), dp(24)),
        pos_hint={'center_y': 0.5}
    ))
    stat1.add_widget(MDLabel(
        text=f"{books_read} read",
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        size_hint_x=1,
        pos_hint={'center_y': 0.5}
    ))
    stats_box.add_widget(stat1)
    
    # Saved books stat
    stat2 = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint_x=0.5)
    stat2.add_widget(MDIcon(
        icon='heart',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        font_size='20sp',
        size_hint=(None, None),
        size=(dp(24), dp(24)),
        pos_hint={'center_y': 0.5}
    ))
    stat2.add_widget(MDLabel(
        text=f"{saved_books} saved",
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        size_hint_x=1
    ))
    stats_box.add_widget(stat2)
    
    content_box.add_widget(stats_box)
    welcome_card.add_widget(content_box)
    
    main_container.add_widget(welcome_card)
    
    # Animate welcome card entrance
    welcome_card.opacity = 0
    anim = Animation(opacity=1, duration=0.5, t='out_cubic')
    anim.start(welcome_card)
    
    # ==================== SUBJECTS SECTION ====================
    # Section header with icon and decorative line
    subjects_header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(12),
        padding=[0, dp(5), 0, dp(5)]
    )
    
    # Icon background circle
    icon_container = FloatLayout(
        size_hint=(None, None),
        size=(dp(36), dp(36))
    )
    
    with icon_container.canvas.before:
        Color(0.13, 0.59, 0.95, 0.15)
        icon_container.circle = RoundedRectangle(
            size=(dp(36), dp(36)),
            pos=icon_container.pos,
            radius=[dp(18)]
        )
    
    icon_container.bind(
        pos=lambda inst, val: setattr(inst.circle, 'pos', val)
    )
    
    icon_container.add_widget(MDIcon(
        icon='shape-outline',
        theme_text_color='Primary',
        font_size='22sp',
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    ))
    
    subjects_header_box.add_widget(icon_container)
    
    subjects_header_box.add_widget(MDLabel(
        text="Explore by Subject",
        font_style='H6',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    ))
    main_container.add_widget(subjects_header_box)
    
    # Get subjects from database
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, COUNT(*) as count 
        FROM books 
        WHERE subject IS NOT NULL AND subject != ''
        GROUP BY subject 
        ORDER BY count DESC 
        LIMIT 10
    """)
    subjects = cursor.fetchall()
    conn.close()
    
    # Color palette for subject cards
    subject_colors = [
        (0.61, 0.35, 0.71, 1),  # Purple
        (0.91, 0.30, 0.55, 1),  # Pink
        (0.26, 0.63, 0.69, 1),  # Teal
        (0.95, 0.61, 0.22, 1),  # Orange
        (0.30, 0.69, 0.31, 1),  # Green
        (0.26, 0.52, 0.96, 1),  # Blue
    ]
    
    # Icon mapping for common subjects
    subject_icons = {
        'computer': 'laptop',
        'science': 'atom',
        'biology': 'dna',
        'physics': 'atom-variant',
        'chemistry': 'flask',
        'mathematics': 'calculator',
        'math': 'chart-line',
        'history': 'book-clock',
        'literature': 'book-open-page-variant',
        'engineering': 'cog',
        'business': 'briefcase',
        'art': 'palette',
        'music': 'music',
        'philosophy': 'head-lightbulb'
    }
    
    # Subject cards horizontal scroll
    subject_scroll = ScrollView(
        size_hint_y=None,
        height=dp(130),
        do_scroll_y=False,
        bar_width=0
    )
    
    subject_container = BoxLayout(
        orientation='horizontal',
        size_hint_x=None,
        spacing=dp(15),
        padding=[0, dp(10)]
    )
    subject_container.bind(minimum_width=subject_container.setter('width'))
    
    for idx, (subject, count) in enumerate(subjects):
        # Create card with colored background
        subject_card = FloatLayout(
            size_hint=(None, 1),
            width=dp(130)
        )
        
        # Get color for this card
        color = subject_colors[idx % len(subject_colors)]
        
        # Find matching icon
        icon_name = 'book-variant'
        for key, icon in subject_icons.items():
            if key.lower() in subject.lower():
                icon_name = icon
                break
        
        # Colored background with shadow
        with subject_card.canvas.before:
            # Shadow
            Color(0, 0, 0, 0.1)
            subject_card.shadow = RoundedRectangle(
                size=subject_card.size,
                pos=(subject_card.x + dp(3), subject_card.y - dp(3)),
                radius=[dp(15)]
            )
            # Main background
            Color(*color)
            subject_card.bg = RoundedRectangle(
                size=subject_card.size,
                pos=subject_card.pos,
                radius=[dp(15)]
            )
        
        def update_subject_bg(instance, value, shadow_rect, bg_rect):
            shadow_rect.size = instance.size
            shadow_rect.pos = (instance.x + dp(3), instance.y - dp(3))
            bg_rect.size = instance.size
            bg_rect.pos = instance.pos
        
        subject_card.bind(
            size=lambda inst, val, s=subject_card.shadow, b=subject_card.bg: update_subject_bg(inst, val, s, b),
            pos=lambda inst, val, s=subject_card.shadow, b=subject_card.bg: update_subject_bg(inst, val, s, b)
        )
        
        # Content
        content = BoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Icon
        content.add_widget(MDIcon(
            icon=icon_name,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            font_size='32sp',
            halign='center',
            size_hint_y=None,
            height=dp(40)
        ))
        
        # Subject name
        subject_label = MDLabel(
            text=subject[:18] + ('...' if len(subject) > 18 else ''),
            font_style='Body2',
            halign='center',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40)
        )
        subject_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
        content.add_widget(subject_label)
        
        # Count
        content.add_widget(MDLabel(
            text=f"{count} books",
            font_style='Caption',
            halign='center',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(15)
        ))
        
        subject_card.add_widget(content)
        
        # Add click handler
        def on_subject_click(instance, touch, subj=subject):
            if instance.collide_point(*touch.pos):
                show_subject_books(parent_instance, subj)
        
        subject_card.bind(on_touch_down=on_subject_click)
        
        # Animate entrance with stagger
        subject_card.opacity = 0
        subject_card.scale_value = 0.8
        anim = Animation(
            opacity=1,
            duration=0.4,
            t='out_back'
        ) + Animation(duration=0.1 + (idx * 0.05))
        anim.start(subject_card)
        
        subject_container.add_widget(subject_card)
    
    subject_scroll.add_widget(subject_container)
    main_container.add_widget(subject_scroll)
    
    # ==================== RECENTLY ADDED SECTION ====================
    # Section header with icon and decorative background
    recent_header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(12),
        padding=[0, dp(5), 0, dp(5)]
    )
    
    # Icon background circle
    recent_icon_container = FloatLayout(
        size_hint=(None, None),
        size=(dp(36), dp(36))
    )
    
    with recent_icon_container.canvas.before:
        Color(0.13, 0.59, 0.95, 0.15)
        recent_icon_container.circle = RoundedRectangle(
            size=(dp(36), dp(36)),
            pos=recent_icon_container.pos,
            radius=[dp(18)]
        )
    
    recent_icon_container.bind(
        pos=lambda inst, val: setattr(inst.circle, 'pos', val)
    )
    
    recent_icon_container.add_widget(MDIcon(
        icon='clock-outline',
        theme_text_color='Primary',
        font_size='22sp',
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    ))
    
    recent_header_box.add_widget(recent_icon_container)
    
    recent_header_box.add_widget(MDLabel(
        text="Recently Added",
        font_style='H6',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    ))
    main_container.add_widget(recent_header_box)
    
    # Get recent books with more details
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, year_of_publication, subject 
        FROM books 
        ORDER BY id DESC 
        LIMIT 6
    """)
    recent_books = cursor.fetchall()
    conn.close()
    
    # Books grid (2 columns)
    books_grid = GridLayout(
        cols=2,
        size_hint_y=None,
        spacing=dp(15),
        padding=[0, dp(10)]
    )
    books_grid.bind(minimum_height=books_grid.setter('height'))
    
    # Gradient colors for book cards
    book_gradients = [
        [(0.13, 0.59, 0.95, 1), (0.10, 0.50, 0.85, 0.8)],  # Blue
        [(0.61, 0.35, 0.71, 1), (0.51, 0.25, 0.61, 0.8)],  # Purple
        [(0.30, 0.69, 0.31, 1), (0.20, 0.59, 0.21, 0.8)],  # Green
        [(0.95, 0.61, 0.22, 1), (0.85, 0.51, 0.12, 0.8)],  # Orange
        [(0.91, 0.30, 0.55, 1), (0.81, 0.20, 0.45, 0.8)],  # Pink
        [(0.26, 0.63, 0.69, 1), (0.16, 0.53, 0.59, 0.8)],  # Teal
    ]
    
    for idx, (book_id, title, year, subject) in enumerate(recent_books):
        # Create elevated card
        book_card = FloatLayout(
            size_hint_y=None,
            height=dp(140)
        )
        
        # Get gradient colors
        gradient = book_gradients[idx % len(book_gradients)]
        
        # Card background with solid color and shadow
        with book_card.canvas.before:
            # Shadow
            Color(0, 0, 0, 0.12)
            book_card.shadow = RoundedRectangle(
                size=book_card.size,
                pos=(book_card.x + dp(2), book_card.y - dp(4)),
                radius=[dp(16)]
            )
            # Main background (solid color)
            Color(*gradient[0])
            book_card.bg = RoundedRectangle(
                size=book_card.size,
                pos=book_card.pos,
                radius=[dp(16)]
            )
        
        def update_book_bg(instance, value, shadow, bg):
            shadow.size = instance.size
            shadow.pos = (instance.x + dp(2), instance.y - dp(4))
            bg.size = instance.size
            bg.pos = instance.pos
        
        book_card.bind(
            size=lambda inst, val, s=book_card.shadow, b=book_card.bg: 
                update_book_bg(inst, val, s, b),
            pos=lambda inst, val, s=book_card.shadow, b=book_card.bg: 
                update_book_bg(inst, val, s, b)
        )
        
        # Content
        content = BoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Book icon
        content.add_widget(MDIcon(
            icon='book-open-variant',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            font_size='32sp',
            halign='center',
            size_hint_y=None,
            height=dp(40)
        ))
        
        # Title
        content.add_widget(MDLabel(
            text=title[:35] + ('...' if len(title) > 35 else ''),
            font_style='Subtitle2',
            bold=True,
            halign='center',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(50)
        ))
        
        # Details row
        details = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20),
            spacing=dp(5)
        )
        
        if year:
            details.add_widget(MDLabel(
                text=str(year),
                font_style='Caption',
                halign='center',
                theme_text_color='Custom',
                text_color=(1, 1, 1, 0.9),
                size_hint_x=0.5
            ))
        
        if subject:
            subject_short = subject[:12] + ('...' if len(subject) > 12 else '')
            details.add_widget(MDLabel(
                text=f"• {subject_short}",
                font_style='Caption',
                halign='center',
                theme_text_color='Custom',
                text_color=(1, 1, 1, 0.9),
                size_hint_x=0.5
            ))
        
        content.add_widget(details)
        book_card.add_widget(content)
        
        # Add click handler
        def on_book_click(instance, touch, bid=book_id):
            if instance.collide_point(*touch.pos):
                show_book_details(parent_instance, bid)
        
        book_card.bind(on_touch_down=on_book_click)
        
        # Animate entrance with stagger
        book_card.opacity = 0
        anim = Animation(
            opacity=1,
            duration=0.5,
            t='out_cubic'
        )
        # Delay based on position
        anim.start_delay = 0.3 + (idx * 0.08)
        anim.start(book_card)
        
        books_grid.add_widget(book_card)
    
    main_container.add_widget(books_grid)
    
    # Add bottom spacer to prevent content hiding behind bottom nav
    bottom_spacer = BoxLayout(
        size_hint_y=None,
        height=dp(80)  # Extra padding to clear bottom nav (56dp nav + 24dp buffer)
    )
    main_container.add_widget(bottom_spacer)
    
    content_scroll.add_widget(main_container)


def show_subject_books(parent_instance, subject):
    """Show all books of a specific subject"""
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.list import MDList, TwoLineListItem
    
    # Get books for this subject
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, year_of_publication 
        FROM books 
        WHERE subject = ? 
        ORDER BY title
        LIMIT 50
    """, (subject,))
    books = cursor.fetchall()
    conn.close()
    
    # Create list of books
    books_list = MDList()
    
    for book_id, title, year in books:
        item = TwoLineListItem(
            text=title[:50] + ('...' if len(title) > 50 else ''),
            secondary_text=f"Year: {year or 'N/A'}",
            on_release=lambda x, bid=book_id: [dialog.dismiss(), show_book_details(parent_instance, bid)]
        )
        books_list.add_widget(item)
    
    if not books:
        books_list.add_widget(TwoLineListItem(
            text="No books found",
            secondary_text="This subject has no books yet"
        ))
    
    # Show dialog
    dialog = MDDialog(
        title=f"{subject}",
        type="custom",
        content_cls=books_list,
        size_hint=(0.9, 0.8),
        buttons=[
            MDFlatButton(
                text="CLOSE",
                on_release=lambda x: dialog.dismiss()
            )
        ]
    )
    dialog.open()


def show_book_details(parent_instance, book_id):
    """Show book details and open PDF in app"""
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.card import MDCard
    
    # Get book details
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, author, year_of_publication, subject, pdf_link 
        FROM books 
        WHERE id = ?
    """, (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if not book:
        return
    
    title, author, year, subject, pdf_link = book
    
    # Create content card
    content = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(250),
        padding=dp(20),
        spacing=dp(15)
    )
    
    # Book icon and title
    header = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(60),
        spacing=dp(15)
    )
    
    header.add_widget(MDIcon(
        icon='book-open-variant',
        theme_text_color='Primary',
        font_size='48sp',
        size_hint=(None, None),
        size=(dp(60), dp(60))
    ))
    
    header.add_widget(MDLabel(
        text=title[:40] + ('...' if len(title) > 40 else ''),
        font_style='H6',
        bold=True,
        theme_text_color='Primary'
    ))
    
    content.add_widget(header)
    
    # Details
    if author:
        content.add_widget(MDLabel(
            text=f"Author: {author}",
            font_style='Body1',
            size_hint_y=None,
            height=dp(30)
        ))
    
    if year:
        content.add_widget(MDLabel(
            text=f"Year: {year}",
            font_style='Body1',
            size_hint_y=None,
            height=dp(30)
        ))
    
    if subject:
        content.add_widget(MDLabel(
            text=f"Subject: {subject}",
            font_style='Body1',
            size_hint_y=None,
            height=dp(30)
        ))
    
    # Buttons
    buttons = []
    
    if pdf_link:
        buttons.append(
            MDRaisedButton(
                text="READ NOW",
                on_release=lambda x: [dialog.dismiss(), open_pdf_in_app(parent_instance, pdf_link, title)]
            )
        )
        buttons.append(
            MDFlatButton(
                text="ADD TO WATCHLIST",
                on_release=lambda x: [add_to_watchlist(parent_instance.user_id, book_id), dialog.dismiss()]
            )
        )
    
    buttons.append(
        MDFlatButton(
            text="CLOSE",
            on_release=lambda x: dialog.dismiss()
        )
    )
    
    # Show dialog
    dialog = MDDialog(
        title="Book Details",
        type="custom",
        content_cls=content,
        size_hint=(0.9, None),
        buttons=buttons
    )
    dialog.open()


def open_pdf_in_app(parent_instance, pdf_link, title):
    """Open PDF in app using a webview or local viewer"""
    from kivymd.uix.dialog import MDDialog
    
    # For now, we'll show a simple message
    # In production, you'd integrate a PDF viewer library
    content = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(150),
        padding=dp(20),
        spacing=dp(15)
    )
    
    content.add_widget(MDLabel(
        text=f"Opening: {title[:50]}...",
        font_style='Subtitle1',
        bold=True,
        size_hint_y=None,
        height=dp(40)
    ))
    
    content.add_widget(MDLabel(
        text="PDF viewer integration coming soon!\\nFor now, the PDF will open in your default browser.",
        font_style='Body2',
        halign='center',
        size_hint_y=None,
        height=dp(60)
    ))
    
    def open_in_browser(instance):
        import webbrowser
        webbrowser.open(pdf_link)
        dialog.dismiss()
    
    dialog = MDDialog(
        title="PDF Viewer",
        type="custom",
        content_cls=content,
        buttons=[
            MDRaisedButton(
                text="OPEN IN BROWSER",
                on_release=open_in_browser
            ),
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: dialog.dismiss()
            )
        ]
    )
    dialog.open()


def add_to_watchlist(user_id, book_id):
    """Add book to user's watchlist"""
    from kivymd.toast import toast
    
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Check if already in watchlist
    cursor.execute("SELECT id FROM watchlist WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    if cursor.fetchone():
        toast("Already in watchlist!")
        conn.close()
        return
    
    # Add to watchlist
    cursor.execute("INSERT INTO watchlist (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
    conn.commit()
    conn.close()
    
    toast("Added to watchlist!")
