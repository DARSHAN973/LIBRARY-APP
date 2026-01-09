"""
Search Tab - Smart Search with Live Suggestions & Recent Searches
Search DB → Live Suggestions → Recent Searches → Web Fallback
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.spinner import MDSpinner
import sqlite3
import json
import os
from utils import open_url_safely


def load_recent_searches():
    """Load recent searches from file"""
    try:
        if os.path.exists('data/recent_searches.json'):
            with open('data/recent_searches.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return []


def save_recent_search(query):
    """Save a search query to recent searches"""
    try:
        recent = load_recent_searches()
        # Remove if already exists
        if query in recent:
            recent.remove(query)
        # Add to beginning
        recent.insert(0, query)
        # Keep only last 10
        recent = recent[:10]
        
        os.makedirs('data', exist_ok=True)
        with open('data/recent_searches.json', 'w') as f:
            json.dump(recent, f)
    except:
        pass


def load_search_tab(content_scroll, parent_instance):
    """Load search tab content with live suggestions and recent searches"""
    from user_modules.home_tab import show_book_details
    
    content_scroll.clear_widgets()
    
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(2),
        padding=dp(15)
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # Header
    header = MDLabel(
        text="🔍 Search Books",
        font_style='H5',
        bold=True,
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        size_hint_y=None,
        height=dp(40)
    )
    main_container.add_widget(header)
    
    # Search section container (search bar + suggestions)
    search_section = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=0
    )
    # Auto-size to its children so suggestions sit directly under the field
    search_section.bind(minimum_height=search_section.setter('height'))
    
    # Search bar
    search_field = MDTextField(
        hint_text="Search book title, subject, author...",
        mode="rectangle",
        size_hint_y=None,
        height=dp(56),
        font_size='16sp'
    )
    search_section.add_widget(search_field)
    
    # Live suggestions container (initially hidden) - directly below search
    suggestions_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=0,
        spacing=dp(4)
    )
    suggestions_container.bind(minimum_height=suggestions_container.setter('height'))
    search_section.add_widget(suggestions_container)
    
    main_container.add_widget(search_section)
    
    # Recent searches section
    recent_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(10)
    )
    recent_container.bind(minimum_height=recent_container.setter('height'))
    
    def show_recent_searches():
        """Display recent searches"""
        recent_container.clear_widgets()
        recent = load_recent_searches()
        
        if recent:
            # Set height for recent container
            recent_container.height = len(recent[:5]) * dp(40) + dp(40)
            
            recent_header = MDLabel(
                text="Recent Searches",
                font_style='Subtitle1',
                bold=True,
                theme_text_color='Primary',
                size_hint_y=None,
                height=dp(30)
            )
            recent_container.add_widget(recent_header)
            
            for query in recent[:5]:  # Show only 5 most recent
                recent_item = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(40),
                    spacing=dp(10),
                    padding=[dp(10), dp(5)]
                )
                
                with recent_item.canvas.before:
                    Color(0.96, 0.96, 0.96, 1)
                    recent_item.bg = RoundedRectangle(
                        size=recent_item.size,
                        pos=recent_item.pos,
                        radius=[dp(8)]
                    )
                
                recent_item.bind(
                    size=lambda inst, val, bg=recent_item: setattr(bg.bg, 'size', inst.size),
                    pos=lambda inst, val, bg=recent_item: setattr(bg.bg, 'pos', inst.pos)
                )
                
                recent_icon = MDIcon(
                    icon='history',
                    theme_text_color='Custom',
                    text_color=(0.6, 0.6, 0.6, 1),
                    size_hint=(None, None),
                    size=(dp(24), dp(24)),
                    pos_hint={'center_y': 0.5}
                )
                recent_item.add_widget(recent_icon)
                
                recent_label = MDLabel(
                    text=query,
                    theme_text_color='Primary',
                    size_hint_x=1,
                    pos_hint={'center_y': 0.5}
                )
                recent_item.add_widget(recent_label)
                
                def on_recent_click(instance, touch, q=query):
                    if instance.collide_point(*touch.pos):
                        search_field.text = q
                        search_books(None)
                
                recent_item.bind(on_touch_down=on_recent_click)
                recent_container.add_widget(recent_item)
        else:
            # Hide recent container if no history
            recent_container.height = 0
    
    show_recent_searches()
    main_container.add_widget(recent_container)
    
    # Results container
    results_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(10)
    )
    results_container.bind(minimum_height=results_container.setter('height'))
    
    def show_suggestions(query):
        """Show live suggestions while typing with loading indicator"""
        suggestions_container.clear_widgets()
        
        if not query or len(query) < 2:
            suggestions_container.height = 0
            # Show recent searches again when no suggestions
            show_recent_searches()
            return
        
        # Hide recent searches when showing suggestions
        recent_container.clear_widgets()
        recent_container.height = 0
        
        # Show loading spinner
        suggestions_container.height = dp(50)
        loading_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        loading_box.add_widget(BoxLayout())  # Spacer
        spinner = MDSpinner(
            size_hint=(None, None),
            size=(dp(25), dp(25)),
            active=True,
            pos_hint={'center_y': 0.5}
        )
        loading_box.add_widget(spinner)
        loading_label = MDLabel(
            text="Loading suggestions...",
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_x=None,
            width=dp(150),
            pos_hint={'center_y': 0.5}
        )
        loading_box.add_widget(loading_label)
        loading_box.add_widget(BoxLayout())  # Spacer
        suggestions_container.add_widget(loading_box)
        
        def do_search(dt):
            # Search for suggestions
            suggestions_container.clear_widgets()
            
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT title 
                FROM books 
                WHERE title LIKE ? 
                LIMIT 5
            """, (f'%{query}%',))
            suggestions = cursor.fetchall()
            conn.close()
            
            if suggestions:
                suggestions_container.height = len(suggestions) * dp(50) + dp(10)
                
                for (title,) in suggestions:
                    suggestion_item = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=dp(50),
                        padding=[dp(12), dp(8)],
                        spacing=dp(10)
                    )
                
                with suggestion_item.canvas.before:
                    Color(1, 1, 1, 1)
                    suggestion_item.bg = RoundedRectangle(
                        size=suggestion_item.size,
                        pos=suggestion_item.pos,
                        radius=[dp(6)]
                    )
                
                suggestion_item.bind(
                    size=lambda inst, val, bg=suggestion_item: setattr(bg.bg, 'size', inst.size),
                    pos=lambda inst, val, bg=suggestion_item: setattr(bg.bg, 'pos', inst.pos)
                )
                
                suggestion_icon = MDIcon(
                    icon='magnify',
                    theme_text_color='Custom',
                    text_color=(0.7, 0.7, 0.7, 1),
                    size_hint=(None, None),
                    size=(dp(24), dp(24)),
                    pos_hint={'center_y': 0.5}
                )
                suggestion_item.add_widget(suggestion_icon)
                
                suggestion_label = MDLabel(
                    text=title[:60] + ('...' if len(title) > 60 else ''),
                    theme_text_color='Primary',
                    font_size='15sp',
                    size_hint_x=1,
                    pos_hint={'center_y': 0.5}
                )
                suggestion_item.add_widget(suggestion_label)
                
                def on_suggestion_click(instance, touch, t=title):
                    if instance.collide_point(*touch.pos):
                        search_field.text = t
                        suggestions_container.height = 0
                        suggestions_container.clear_widgets()
                        search_books(None)
                
                suggestion_item.bind(on_touch_down=on_suggestion_click)
                suggestions_container.add_widget(suggestion_item)
            else:
                suggestions_container.height = 0
        
        # Schedule search with small delay to show loading
        Clock.schedule_once(do_search, 0.1)
    
    # Search functionality with debounce for live suggestions
    search_timer = [None]
    
    def on_text_change(instance, value):
        """Handle text changes for live suggestions"""
        if search_timer[0]:
            search_timer[0].cancel()
        
        def do_suggest(dt):
            show_suggestions(value.strip())
        
        search_timer[0] = Clock.schedule_once(do_suggest, 0.3)
    
    search_field.bind(text=on_text_change)
    
    def search_books(instance):
        """Search books in database"""
        query = search_field.text.strip()
        if not query:
            return
        
        # Hide suggestions
        suggestions_container.height = 0
        suggestions_container.clear_widgets()
        
        # Save to recent searches
        save_recent_search(query)
        show_recent_searches()
        
        results_container.clear_widgets()
        
        # Search in database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, subject, author, year_of_publication 
            FROM books 
            WHERE title LIKE ? OR subject LIKE ? OR author LIKE ?
            LIMIT 20
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        books = cursor.fetchall()
        conn.close()
        
        if books:
            # Results header
            results_header = MDLabel(
                text=f"Found {len(books)} book(s)",
                font_style='Subtitle1',
                bold=True,
                theme_text_color='Primary',
                size_hint_y=None,
                height=dp(30)
            )
            results_container.add_widget(results_header)
            
            # Show results
            for book_id, title, subject, author, year in books:
                book_card = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(110),
                    padding=dp(15),
                    spacing=dp(15)
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
                
                # Book info section
                info_section = BoxLayout(
                    orientation='vertical',
                    size_hint_x=0.7,
                    spacing=dp(5)
                )
                
                # Title
                title_label = MDLabel(
                    text=title[:45] + ('...' if len(title) > 45 else ''),
                    font_style='Subtitle1',
                    bold=True,
                    theme_text_color='Primary',
                    size_hint_y=None,
                    height=dp(28)
                )
                info_section.add_widget(title_label)
                
                # Author
                if author:
                    author_label = MDLabel(
                        text=f"By: {author[:30]}" + ('...' if len(author) > 30 else ''),
                        font_style='Caption',
                        theme_text_color='Secondary',
                        size_hint_y=None,
                        height=dp(20)
                    )
                    info_section.add_widget(author_label)
                
                # Subject and Year
                meta_label = MDLabel(
                    text=f"{subject or 'N/A'} • {year or 'N/A'}",
                    font_style='Caption',
                    theme_text_color='Secondary',
                    size_hint_y=None,
                    height=dp(20)
                )
                info_section.add_widget(meta_label)
                
                book_card.add_widget(info_section)
                
                # Button section
                btn_section = BoxLayout(
                    orientation='vertical',
                    size_hint_x=0.3,
                    padding=[0, dp(10), 0, dp(10)]
                )
                
                view_btn = MDRaisedButton(
                    text="View",
                    size_hint=(1, None),
                    height=dp(40),
                    md_bg_color=(0.13, 0.59, 0.95, 1)
                )
                
                def make_view_handler(bid=book_id):
                    def handler(instance):
                        show_book_details(parent_instance, bid)
                    return handler
                
                view_btn.bind(on_release=make_view_handler())
                btn_section.add_widget(view_btn)
                
                book_card.add_widget(btn_section)
                results_container.add_widget(book_card)
        else:
            # NOT FOUND - Show web search option
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
