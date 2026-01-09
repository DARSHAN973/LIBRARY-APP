"""
Search Tab - Smart Search with Web Fallback
Search DB → If not found → Open in Browser
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
import sqlite3
from utils import open_url_safely


def load_search_tab(content_scroll, parent_instance):
    """Load search tab content"""
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
        text="Search Books",
        font_style='H5',
        bold=True,
        theme_text_color='Primary',
        size_hint_y=None,
        height=dp(40)
    )
    main_container.add_widget(header)
    
    # Search bar
    search_field = MDTextField(
        hint_text="Search book title, subject, author...",
        mode="rectangle",
        size_hint_y=None,
        height=dp(56)
    )
    main_container.add_widget(search_field)
    
    # Results container
    results_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(10)
    )
    results_container.bind(minimum_height=results_container.setter('height'))
    
    def search_books(instance):
        """Search books in database"""
        query = search_field.text.strip()
        if not query:
            return
        
        results_container.clear_widgets()
        
        # Search in database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, subject, year_of_publication 
            FROM books 
            WHERE title LIKE ? OR subject LIKE ? OR author LIKE ?
            LIMIT 20
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        books = cursor.fetchall()
        conn.close()
        
        if books:
            # Show results
            for book_id, title, subject, year in books:
                book_card = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(100),
                    padding=dp(15),
                    spacing=dp(8)
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
                    text=title[:50] + ('...' if len(title) > 50 else ''),
                    font_style='Subtitle1',
                    bold=True,
                    theme_text_color='Primary',
                    size_hint_y=None,
                    height=dp(25)
                ))
                
                book_card.add_widget(MDLabel(
                    text=f"{subject or 'N/A'} • {year or 'N/A'}",
                    font_style='Caption',
                    theme_text_color='Secondary',
                    size_hint_y=None,
                    height=dp(18)
                ))
                
                view_btn = MDRaisedButton(
                    text="View Book",
                    size_hint=(None, None),
                    size=(dp(120), dp(36)),
                    md_bg_color=(0.13, 0.59, 0.95, 1)
                )
                book_card.add_widget(view_btn)
                
                results_container.add_widget(book_card)
        else:
            # NOT FOUND - Show web search option 🔥
            not_found_card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(180),
                padding=dp(20),
                spacing=dp(15)
            )
            
            with not_found_card.canvas.before:
                Color(1, 0.95, 0.95, 1)
                not_found_card.bg = RoundedRectangle(
                    size=not_found_card.size,
                    pos=not_found_card.pos,
                    radius=[dp(12)]
                )
            
            not_found_card.bind(
                size=lambda inst, val, bg=not_found_card: setattr(bg.bg, 'size', inst.size),
                pos=lambda inst, val, bg=not_found_card: setattr(bg.bg, 'pos', inst.pos)
            )
            
            not_found_card.add_widget(MDLabel(
                text="❌ Book not found in library",
                font_style='H6',
                bold=True,
                halign='center',
                theme_text_color='Custom',
                text_color=(0.96, 0.26, 0.21, 1),
                size_hint_y=None,
                height=dp(30)
            ))
            
            not_found_card.add_widget(MDLabel(
                text="🔎 Search this book on the web",
                font_style='Subtitle1',
                halign='center',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(25)
            ))
            
            def open_browser(instance):
                """Open browser with Google search"""
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                open_url_safely(search_url)
            
            web_btn = MDRaisedButton(
                text="OPEN IN BROWSER",
                pos_hint={'center_x': 0.5},
                size_hint=(None, None),
                size=(dp(200), dp(45)),
                md_bg_color=(0.13, 0.59, 0.95, 1),
                on_release=open_browser
            )
            
            btn_container = BoxLayout(size_hint_y=None, height=dp(45))
            btn_container.add_widget(BoxLayout())
            btn_container.add_widget(web_btn)
            btn_container.add_widget(BoxLayout())
            
            not_found_card.add_widget(btn_container)
            results_container.add_widget(not_found_card)
    
    search_field.bind(on_text_validate=search_books)
    
    # Search button
    search_btn = MDRaisedButton(
        text="SEARCH",
        size_hint_y=None,
        height=dp(45),
        md_bg_color=(0.13, 0.59, 0.95, 1),
        on_release=search_books
    )
    main_container.add_widget(search_btn)
    
    main_container.add_widget(results_container)
    content_scroll.add_widget(main_container)
