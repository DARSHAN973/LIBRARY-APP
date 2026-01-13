"""
Browse Tab - Subject-based Exploration
Subject Grid → Dynamic Book List Page
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
import sqlite3


def load_browse_tab(content_scroll, parent_instance):
    """Load browse tab content"""
    from user_modules.home_tab import load_book_list_page
    
    content_scroll.clear_widgets()
    
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(15),
        padding=dp(15)
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # Attractive Header with Icon
    header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(50),
        spacing=dp(10)
    )
    
    header_icon = MDLabel(
        text="🔎",
        font_style='H5',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        size_hint=(None, None),
        size=(dp(40), dp(40)),
        pos_hint={'center_y': 0.5}
    )
    header_box.add_widget(header_icon)
    
    header_label = MDLabel(
        text="Browse by Subject",
        font_style='H5',
        bold=True,
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        size_hint_x=1,
        pos_hint={'center_y': 0.5}
    )
    header_box.add_widget(header_label)
    main_container.add_widget(header_box)
    
    # Search Bar
    search_field = MDTextField(
        hint_text="Search subjects...",
        mode="rectangle",
        size_hint_y=None,
        height=dp(50),
        font_size='16sp',
        icon_left='magnify'
    )
    main_container.add_widget(search_field)
    
    # Get all subjects
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, COUNT(*) as count 
        FROM books 
        WHERE subject IS NOT NULL AND subject != ''
        GROUP BY subject 
        ORDER BY subject ASC
    """)
    subjects = cursor.fetchall()
    conn.close()
    
    # Subject grid (2 columns)
    subject_grid = GridLayout(
        cols=2,
        size_hint_y=None,
        spacing=dp(15),
        padding=[0, dp(5)]
    )
    subject_grid.bind(minimum_height=subject_grid.setter('height'))
    
    # Icon mapping for subjects
    subject_icons = {
        'Computer Science': 'laptop',
        'Biology': 'molecule',
        'Commerce': 'briefcase',
        'Law': 'gavel',
        'Mathematics': 'calculator',
        'Physics': 'atom',
        'Chemistry': 'flask',
        'History': 'book-clock',
        'Geography': 'earth',
        'English': 'alphabetical'
    }
    
    def populate_subjects(subjects_to_show):
        """Populate the subject grid"""
        subject_grid.clear_widgets()
        
        if not subjects_to_show:
            # No results message
            no_results = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(150),
                padding=dp(20)
            )
            no_results.add_widget(MDLabel(
                text="No subjects found",
                font_style='H6',
                halign='center',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(30)
            ))
            subject_grid.add_widget(no_results)
            return
        
        for subject, count in subjects_to_show:
            subject_card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(120),
                padding=dp(15),
                spacing=dp(10)
                )
            
            with subject_card.canvas.before:
                Color(1, 1, 1, 1)
                subject_card.bg = RoundedRectangle(
                    size=subject_card.size,
                    pos=subject_card.pos,
                    radius=[dp(12)]
                )
            
            subject_card.bind(
                size=lambda inst, val, bg=subject_card: setattr(bg.bg, 'size', inst.size),
                pos=lambda inst, val, bg=subject_card: setattr(bg.bg, 'pos', inst.pos)
            )
            
            # Icon
            icon = MDIcon(
                icon=subject_icons.get(subject, 'book'),
                theme_text_color='Custom',
                text_color=(0.13, 0.59, 0.95, 1),
                font_size='48sp',
                halign='center',
                size_hint_y=None,
                height=dp(50)
            )
            subject_card.add_widget(icon)
            
            # Subject name with text limit
            subject_text = subject if len(subject) <= 20 else subject[:17] + '...'
            subject_card.add_widget(MDLabel(
                text=subject_text,
                font_style='Subtitle1',
                bold=True,
                halign='center',
                theme_text_color='Primary',
                size_hint_y=None,
                height=dp(25)
            ))
            
            # Book count
            subject_card.add_widget(MDLabel(
                text=f"{count} books",
                font_style='Caption',
                halign='center',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(18)
            ))
            
            # Add click handler to open dynamic book list page
            def on_subject_click(instance, touch, subj=subject):
                if instance.collide_point(*touch.pos):
                    # Fetch books for this subject
                    conn = sqlite3.connect('library.db')
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, title, author, year_of_publication, subject 
                        FROM books 
                        WHERE subject = ? 
                        ORDER BY title
                    """, (subj,))
                    books = cursor.fetchall()
                    conn.close()
                    
                    # Load dynamic book list page
                    load_book_list_page(parent_instance, subj, books)
            
            subject_card.bind(on_touch_down=on_subject_click)
            
            subject_grid.add_widget(subject_card)
    
    # Initial population
    populate_subjects(subjects)
    
    # Search functionality
    search_timer = [None]
    
    def on_search_text(instance, value):
        """Handle search with debounce"""
        if search_timer[0]:
            search_timer[0].cancel()
        
        def do_search(dt):
            query = value.strip().lower()
            if not query:
                populate_subjects(subjects)
            else:
                filtered = [(s, c) for s, c in subjects if query in s.lower()]
                populate_subjects(filtered)
        
        search_timer[0] = Clock.schedule_once(do_search, 0.3)
    
    search_field.bind(text=on_search_text)
    
    main_container.add_widget(subject_grid)
    
    # Bottom spacer
    bottom_spacer = BoxLayout(
        size_hint_y=None,
        height=dp(80)
    )
    main_container.add_widget(bottom_spacer)
    
    content_scroll.add_widget(main_container)
