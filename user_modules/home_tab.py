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


def load_book_list_page(parent_instance, page_title, books):
    """Dynamic page to display list of books with back button - Modern & Stylish"""
    from kivy.uix.widget import Widget
    from kivy.animation import Animation
    
    # Clear current content
    parent_instance.content_scroll.clear_widgets()
    
    # Main container
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(12),
        padding=[dp(12), dp(5), dp(12), 0]
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # ==================== STYLISH HEADER ====================
    # Header background card
    header_card = FloatLayout(
        size_hint_y=None,
        height=dp(110)
    )
    
    with header_card.canvas.before:
        # Gradient-like header with modern blue
        Color(0.13, 0.59, 0.95, 1)
        header_card.bg = RoundedRectangle(
            size=header_card.size,
            pos=header_card.pos,
            radius=[dp(16), dp(16), dp(16), dp(16)]
        )
    
    header_card.bind(
        size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
        pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
    )
    
    # Header content container
    header_content = BoxLayout(
        orientation='vertical',
        padding=[dp(15), dp(12), dp(15), dp(12)],
        spacing=dp(8)
    )
    
    # Top row: Back button + Count badge
    top_row = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(10)
    )
    
    # Back button with circular bg
    back_container = FloatLayout(
        size_hint=(None, 1),
        width=dp(40)
    )
    
    back_circle = BoxLayout(
        size_hint=(None, None),
        size=(dp(40), dp(40)),
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    )
    
    with back_circle.canvas.before:
        Color(1, 1, 1, 0.2)
        back_circle.bg = RoundedRectangle(
            size=(dp(40), dp(40)),
            pos=back_circle.pos,
            radius=[dp(20)]
        )
    
    back_circle.bind(
        pos=lambda inst, val: setattr(inst.bg, 'pos', val)
    )
    
    back_btn = MDIconButton(
        icon='arrow-left',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        pos_hint={'center_x': 0.5, 'center_y': 0.5},
        on_release=lambda x: load_home_tab(parent_instance.content_scroll, parent_instance)
    )
    back_circle.add_widget(back_btn)
    back_container.add_widget(back_circle)
    top_row.add_widget(back_container)
    
    # Spacer
    top_row.add_widget(BoxLayout(size_hint_x=1))
    
    # Book count badge
    count_badge = BoxLayout(
        size_hint=(None, None),
        size=(dp(60), dp(32)),
        padding=[dp(10), 0, dp(10), 0]
    )
    
    with count_badge.canvas.before:
        Color(1, 1, 1, 0.25)
        count_badge.bg = RoundedRectangle(
            size=(dp(60), dp(32)),
            pos=count_badge.pos,
            radius=[dp(16)]
        )
    
    count_badge.bind(
        pos=lambda inst, val: setattr(inst.bg, 'pos', val),
        size=lambda inst, val: setattr(inst.bg, 'size', val)
    )
    
    count_badge.add_widget(MDLabel(
        text=str(len(books)),
        font_style='Subtitle2',
        bold=True,
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        halign='center'
    ))
    
    top_row.add_widget(count_badge)
    header_content.add_widget(top_row)
    
    # Title section with icon
    title_row = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(50),
        spacing=dp(12)
    )
    
    # Subject icon
    title_row.add_widget(MDIcon(
        icon='bookshelf',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.9),
        font_size='28sp',
        size_hint=(None, None),
        size=(dp(32), dp(32)),
        pos_hint={'center_y': 0.5}
    ))
    
    # Title with proper wrapping
    title_text = page_title if len(page_title) <= 30 else page_title[:27] + '...'
    title_box = BoxLayout(
        orientation='vertical',
        size_hint_x=1,
        spacing=dp(2)
    )
    
    title_box.add_widget(MDLabel(
        text=title_text,
        font_style='H6',
        bold=True,
        theme_text_color='Custom',
        text_color=(1, 1, 1, 1),
        size_hint_y=None,
        height=dp(30)
    ))
    
    title_box.add_widget(MDLabel(
        text=f"{len(books)} book{'s' if len(books) != 1 else ''} available",
        font_style='Caption',
        theme_text_color='Custom',
        text_color=(1, 1, 1, 0.8),
        size_hint_y=None,
        height=dp(18)
    ))
    
    title_row.add_widget(title_box)
    header_content.add_widget(title_row)
    header_card.add_widget(header_content)
    main_container.add_widget(header_card)
    
    # Small spacing after header
    main_container.add_widget(BoxLayout(size_hint_y=None, height=dp(5)))
    
    # ==================== BOOKS LIST ====================
    if not books:
        # Empty state
        empty_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(250),
            spacing=dp(15),
            padding=dp(30)
        )
        
        empty_container.add_widget(MDIcon(
            icon='book-off-outline',
            theme_text_color='Custom',
            text_color=(0.6, 0.6, 0.6, 0.4),
            font_size='72sp',
            halign='center',
            size_hint_y=None,
            height=dp(90)
        ))
        
        empty_container.add_widget(MDLabel(
            text="No Books Found",
            font_style='H6',
            bold=True,
            halign='center',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(40)
        ))
        
        empty_container.add_widget(MDLabel(
            text="This category doesn't have any books yet.\\nCheck back later!",
            font_style='Body2',
            halign='center',
            theme_text_color='Hint',
            size_hint_y=None,
            height=dp(50)
        ))
        
        main_container.add_widget(empty_container)
    else:
        # Books list container
        for idx, book_data in enumerate(books):
            book_id = book_data[0]
            title = book_data[1]
            author = book_data[2] if len(book_data) > 2 else None
            year = book_data[3] if len(book_data) > 3 else None
            subject = book_data[4] if len(book_data) > 4 else None
            
            # Create modern book card
            book_card = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(110),
                padding=[dp(12), dp(12), dp(12), dp(12)],
                spacing=dp(12)
            )
            
            # Card background with shadow
            with book_card.canvas.before:
                # Subtle shadow
                Color(0, 0, 0, 0.05)
                book_card.shadow = RoundedRectangle(
                    size=book_card.size,
                    pos=(book_card.x + dp(2), book_card.y - dp(2)),
                    radius=[dp(14)]
                )
                # White background
                Color(1, 1, 1, 1)
                book_card.bg = RoundedRectangle(
                    size=book_card.size,
                    pos=book_card.pos,
                    radius=[dp(14)]
                )
            
            def update_card_bg(inst, val, shadow, bg):
                shadow.size = inst.size
                shadow.pos = (inst.x + dp(2), inst.y - dp(2))
                bg.size = inst.size
                bg.pos = inst.pos
            
            book_card.bind(
                size=lambda inst, val, s=book_card.shadow, b=book_card.bg: update_card_bg(inst, val, s, b),
                pos=lambda inst, val, s=book_card.shadow, b=book_card.bg: update_card_bg(inst, val, s, b)
            )
            
            # Book icon - FIXED AND CENTERED
            icon_container = BoxLayout(
                orientation='vertical',
                size_hint=(None, 1),
                width=dp(70),
                padding=[0, dp(10), 0, dp(10)]
            )
            
            icon_bg_wrapper = BoxLayout(
                size_hint_y=None,
                height=dp(70)
            )
            
            icon_bg = FloatLayout(
                size_hint=(1, 1)
            )
            
            with icon_bg.canvas.before:
                Color(0.13, 0.59, 0.95, 0.12)
                icon_bg.rect = RoundedRectangle(
                    size=(dp(70), dp(70)),
                    pos=icon_bg.pos,
                    radius=[dp(14)]
                )
            
            def update_icon_bg(inst, val):
                inst.rect.size = inst.size
                inst.rect.pos = inst.pos
            
            icon_bg.bind(size=update_icon_bg, pos=update_icon_bg)
            
            # Icon centered inside
            icon_bg.add_widget(MDIcon(
                icon='book-open-page-variant',
                theme_text_color='Primary',
                font_size='36sp',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            ))
            
            icon_bg_wrapper.add_widget(icon_bg)
            icon_container.add_widget(icon_bg_wrapper)
            book_card.add_widget(icon_container)
            
            # Book details - PROPERLY ARRANGED
            details_container = BoxLayout(
                orientation='vertical',
                spacing=dp(6),
                size_hint_x=1,
                padding=[0, dp(5), 0, dp(5)]
            )
            
            # Title - NO OVERLAP
            title_text = title if len(title) <= 40 else title[:37] + '...'
            title_label = MDLabel(
                text=title_text,
                font_style='Subtitle1',
                bold=True,
                theme_text_color='Primary',
                size_hint_y=None,
                height=dp(24),
                markup=False
            )
            details_container.add_widget(title_label)
            
            # Author row
            if author:
                author_text = author if len(author) <= 32 else author[:29] + '...'
                author_row = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(20),
                    spacing=dp(6)
                )
                author_row.add_widget(MDIcon(
                    icon='account-outline',
                    theme_text_color='Secondary',
                    font_size='16sp',
                    size_hint=(None, 1),
                    width=dp(16)
                ))
                author_row.add_widget(MDLabel(
                    text=author_text,
                    font_style='Caption',
                    theme_text_color='Secondary',
                    size_hint_x=1,
                    markup=False
                ))
                details_container.add_widget(author_row)
            
            # Meta info row (Year + Subject)
            meta_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(20),
                spacing=dp(8)
            )
            
            if year:
                year_chip = BoxLayout(
                    size_hint=(None, None),
                    size=(dp(60), dp(20)),
                    padding=[dp(6), 0, dp(6), 0]
                )
                
                with year_chip.canvas.before:
                    Color(0.13, 0.59, 0.95, 0.1)
                    year_chip.chip_bg = RoundedRectangle(
                        size=(dp(60), dp(20)),
                        pos=year_chip.pos,
                        radius=[dp(10)]
                    )
                
                year_chip.bind(
                    pos=lambda inst, val: setattr(inst.chip_bg, 'pos', val)
                )
                
                year_chip.add_widget(MDLabel(
                    text=str(year),
                    font_style='Caption',
                    theme_text_color='Primary',
                    halign='center'
                ))
                meta_row.add_widget(year_chip)
            
            if subject:
                subject_text = subject if len(subject) <= 18 else subject[:15] + '...'
                meta_row.add_widget(MDLabel(
                    text=f"• {subject_text}",
                    font_style='Caption',
                    theme_text_color='Hint',
                    size_hint_x=1,
                    markup=False
                ))
            
            details_container.add_widget(meta_row)
            book_card.add_widget(details_container)
            
            # Chevron - PROPERLY ALIGNED
            chevron_container = BoxLayout(
                orientation='vertical',
                size_hint=(None, 1),
                width=dp(30)
            )
            chevron_container.add_widget(MDIcon(
                icon='chevron-right',
                theme_text_color='Hint',
                font_size='28sp',
                pos_hint={'center_y': 0.5}
            ))
            book_card.add_widget(chevron_container)
            
            # Add click handler
            def on_card_click(instance, touch, bid=book_id):
                if instance.collide_point(*touch.pos):
                    show_book_details(parent_instance, bid)
            
            book_card.bind(on_touch_down=on_card_click)
            
            # Animate card entrance
            book_card.opacity = 0
            anim = Animation(opacity=1, duration=0.3, t='out_cubic')
            anim.start_delay = idx * 0.03  # Stagger effect
            anim.start(book_card)
            
            main_container.add_widget(book_card)
    
    # Bottom spacer
    bottom_spacer = BoxLayout(
        size_hint_y=None,
        height=dp(80)
    )
    main_container.add_widget(bottom_spacer)
    
    parent_instance.content_scroll.add_widget(main_container)


def show_subject_books(parent_instance, subject):
    """Show all books of a specific subject in a dedicated page"""
    # Get books for this subject
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, author, year_of_publication, subject 
        FROM books 
        WHERE subject = ? 
        ORDER BY title
    """, (subject,))
    books = cursor.fetchall()
    conn.close()
    
    # Load the dynamic book list page
    load_book_list_page(parent_instance, subject, books)


def show_book_details(parent_instance, book_id):
    """Show book details in a well-styled dialog"""
    from kivymd.uix.dialog import MDDialog
    
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
    
    # Create content with proper text limits
    content = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(300),
        padding=dp(20),
        spacing=dp(12)
    )
    
    # Book icon with colored background
    icon_box = FloatLayout(
        size_hint_y=None,
        height=dp(80)
    )
    
    icon_bg = BoxLayout(
        size_hint=(None, None),
        size=(dp(80), dp(80)),
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    )
    
    with icon_bg.canvas.before:
        Color(0.13, 0.59, 0.95, 0.15)
        icon_bg.bg = RoundedRectangle(
            size=(dp(80), dp(80)),
            pos=icon_bg.pos,
            radius=[dp(40)]
        )
    
    icon_bg.bind(
        pos=lambda inst, val: setattr(inst.bg, 'pos', val)
    )
    
    icon_bg.add_widget(MDIcon(
        icon='book-open-variant',
        theme_text_color='Primary',
        font_size='48sp',
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    ))
    
    icon_box.add_widget(icon_bg)
    content.add_widget(icon_box)
    
    # Title with text limit
    title_text = title if len(title) <= 50 else title[:47] + '...'
    title_label = MDLabel(
        text=title_text,
        font_style='H6',
        bold=True,
        halign='center',
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(60)
    )
    title_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
    content.add_widget(title_label)
    
    # Details container
    details_box = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(90),
        spacing=dp(8),
        padding=[dp(10), 0, dp(10), 0]
    )
    
    # Author with text limit
    if author:
        author_text = author if len(author) <= 40 else author[:37] + '...'
        author_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(25),
            spacing=dp(10)
        )
        author_row.add_widget(MDIcon(
            icon='account',
            theme_text_color='Secondary',
            font_size='20sp',
            size_hint=(None, None),
            size=(dp(24), dp(24))
        ))
        author_row.add_widget(MDLabel(
            text=author_text,
            font_style='Body2',
            theme_text_color='Secondary',
            size_hint_x=1
        ))
        details_box.add_widget(author_row)
    
    # Year
    if year:
        year_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(25),
            spacing=dp(10)
        )
        year_row.add_widget(MDIcon(
            icon='calendar',
            theme_text_color='Secondary',
            font_size='20sp',
            size_hint=(None, None),
            size=(dp(24), dp(24))
        ))
        year_row.add_widget(MDLabel(
            text=str(year),
            font_style='Body2',
            theme_text_color='Secondary',
            size_hint_x=1
        ))
        details_box.add_widget(year_row)
    
    # Subject with text limit
    if subject:
        subject_text = subject if len(subject) <= 35 else subject[:32] + '...'
        subject_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(25),
            spacing=dp(10)
        )
        subject_row.add_widget(MDIcon(
            icon='tag',
            theme_text_color='Secondary',
            font_size='20sp',
            size_hint=(None, None),
            size=(dp(24), dp(24))
        ))
        subject_row.add_widget(MDLabel(
            text=subject_text,
            font_style='Body2',
            theme_text_color='Secondary',
            size_hint_x=1
        ))
        details_box.add_widget(subject_row)
    
    content.add_widget(details_box)
    
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
    
    # Show dialog with custom styling
    dialog = MDDialog(
        title="",
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
