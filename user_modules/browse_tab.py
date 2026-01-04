"""
Browse Tab - Subject-based Exploration
Subject Grid → Book List
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivymd.uix.label import MDLabel, MDIcon
import sqlite3


def load_browse_tab(content_scroll, parent_instance):
    """Load browse tab content"""
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
        text="Browse by Subject",
        font_style='H5',
        bold=True,
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(40)
    )
    main_container.add_widget(header)
    
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
    
    for subject, count in subjects:
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
        
        # Subject name
        subject_card.add_widget(MDLabel(
            text=subject,
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
        
        subject_grid.add_widget(subject_card)
    
    main_container.add_widget(subject_grid)
    content_scroll.add_widget(main_container)
