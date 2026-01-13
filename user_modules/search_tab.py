"""
Search Tab - Smart Search with Live Suggestions & Recent Searches
Search DB → Live Suggestions → Recent Searches → Web Fallback
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.card import MDCard
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
    """Modern Search Tab with Live Suggestions & Smart History"""
    from user_modules.home_tab import show_book_details
    
    content_scroll.clear_widgets()
    
    # Main Container - Modern spacing
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(18),
        padding=[dp(20), dp(15), dp(20), dp(15)]
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # ========== HEADER SECTION ==========
    header_section = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(70),
        spacing=dp(5)
    )
    
    # Title with icon
    title_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(8)
    )
    
    title_icon = MDIcon(
        icon='book-search',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        size_hint=(None, None),
        size=(dp(32), dp(32)),
        pos_hint={'center_y': 0.5}
    )
    title_box.add_widget(title_icon)
    
    title = MDLabel(
        text="Discover Books",
        font_style='H4',
        bold=True,
        theme_text_color='Custom',
        text_color=(0.1, 0.1, 0.1, 1),
        size_hint_x=1,
        pos_hint={'center_y': 0.5}
    )
    title_box.add_widget(title)
    header_section.add_widget(title_box)
    
    subtitle = MDLabel(
        text="Search our extensive library collection",
        font_style='Body2',
        theme_text_color='Custom',
        text_color=(0.5, 0.5, 0.5, 1),
        size_hint_y=None,
        height=dp(25)
    )
    header_section.add_widget(subtitle)
    
    main_container.add_widget(header_section)
    
    # ========== SEARCH CARD SECTION ==========
    search_card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=0
    )
    search_card.bind(minimum_height=search_card.setter('height'))
    
    # Search Input Container - Cleaner Layout
    search_input_card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(115),
        padding=dp(5),
        spacing=dp(10)
    )
    
    # Search Field (Clean, standalone)
    search_field = MDTextField(
        hint_text="Search books, authors, subjects...",
        mode="rectangle",
        size_hint_y=None,
        height=dp(56),
        font_size='16sp'
    )
    search_input_card.add_widget(search_field)
    
    # Search Button (Full width below field)
    search_btn = MDRaisedButton(
        text="SEARCH",
        size_hint_y=None,
        height=dp(45),
        md_bg_color=(0.13, 0.59, 0.95, 1),
        elevation=2
    )
    search_input_card.add_widget(search_btn)
    search_card.add_widget(search_input_card)
    
    # ========== LIVE SUGGESTIONS CONTAINER ==========
    suggestions_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=0,
        spacing=dp(12),
        padding=[dp(5), dp(15), dp(5), 0]
    )
    search_card.add_widget(suggestions_container)
    
    main_container.add_widget(search_card)
    
    # ========== RECENT SEARCHES SECTION ==========
    recent_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(12)
    )
    recent_container.bind(minimum_height=recent_container.setter('height'))
    
    def show_recent_searches():
        """Display recent searches with modern design"""
        recent_container.clear_widgets()
        recent = load_recent_searches()
        
        if recent:
            recent_container.height = len(recent[:6]) * dp(56) + dp(50)
            
            # Section Header
            recent_header_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(35),
                spacing=dp(8)
            )
            
            recent_icon_header = MDIcon(
                icon='history',
                theme_text_color='Custom',
                text_color=(0.13, 0.59, 0.95, 1),
                size_hint=(None, None),
                size=(dp(22), dp(22)),
                pos_hint={'center_y': 0.5}
            )
            recent_header_box.add_widget(recent_icon_header)
            
            recent_header = MDLabel(
                text="Recent Searches",
                font_style='Subtitle1',
                bold=True,
                theme_text_color='Custom',
                text_color=(0.2, 0.2, 0.2, 1),
                size_hint_x=1,
                pos_hint={'center_y': 0.5}
            )
            recent_header_box.add_widget(recent_header)
            recent_container.add_widget(recent_header_box)
            
            # Recent Items
            for idx, query in enumerate(recent[:6]):
                recent_item = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(56),
                    spacing=dp(12),
                    padding=[dp(16), dp(10), dp(16), dp(10)]
                )
                
                with recent_item.canvas.before:
                    Color(0.98, 0.98, 0.98, 1)
                    recent_item.bg = RoundedRectangle(
                        size=recent_item.size,
                        pos=recent_item.pos,
                        radius=[dp(12)]
                    )
                
                recent_item.bind(
                    size=lambda inst, val, bg=recent_item: setattr(bg.bg, 'size', inst.size),
                    pos=lambda inst, val, bg=recent_item: setattr(bg.bg, 'pos', inst.pos)
                )
                
                # Clock Icon
                time_icon = MDIcon(
                    icon='clock-outline',
                    theme_text_color='Custom',
                    text_color=(0.13, 0.59, 0.95, 1),
                    size_hint=(None, None),
                    size=(dp(26), dp(26)),
                    pos_hint={'center_y': 0.5}
                )
                recent_item.add_widget(time_icon)
                
                # Query Text
                query_label = MDLabel(
                    text=query,
                    theme_text_color='Custom',
                    text_color=(0.25, 0.25, 0.25, 1),
                    font_size='15sp',
                    size_hint_x=1,
                    pos_hint={'center_y': 0.5}
                )
                recent_item.add_widget(query_label)
                
                # Arrow Icon
                arrow_icon = MDIcon(
                    icon='chevron-right',
                    theme_text_color='Custom',
                    text_color=(0.7, 0.7, 0.7, 1),
                    size_hint=(None, None),
                    size=(dp(24), dp(24)),
                    pos_hint={'center_y': 0.5}
                )
                recent_item.add_widget(arrow_icon)
                
                def on_recent_click(instance, touch, q=query):
                    if instance.collide_point(*touch.pos):
                        search_field.text = q
                        search_books(None)
                
                recent_item.bind(on_touch_down=on_recent_click)
                recent_container.add_widget(recent_item)
        else:
            recent_container.height = 0
    
    show_recent_searches()
    main_container.add_widget(recent_container)
    
    # ========== RESULTS CONTAINER ==========
    results_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(12)
    )
    results_container.bind(minimum_height=results_container.setter('height'))
    
    def show_suggestions(query):
        """Show live suggestions with modern styling"""
        suggestions_container.clear_widgets()
        
        if not query or len(query) < 2:
            suggestions_container.height = 0
            show_recent_searches()
            return
        
        # Hide recent searches
        recent_container.clear_widgets()
        recent_container.height = 0
        
        # Show loading
        suggestions_container.height = dp(60)
        loading_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(12),
            padding=dp(15)
        )
        
        spinner = MDSpinner(
            size_hint=(None, None),
            size=(dp(28), dp(28)),
            active=True,
            pos_hint={'center_y': 0.5}
        )
        loading_box.add_widget(spinner)
        
        loading_label = MDLabel(
            text="Searching library...",
            font_style='Body2',
            theme_text_color='Custom',
            text_color=(0.5, 0.5, 0.5, 1),
            size_hint_x=1,
            pos_hint={'center_y': 0.5}
        )
        loading_box.add_widget(loading_label)
        suggestions_container.add_widget(loading_box)
        
        def do_search(dt):
            suggestions_container.clear_widgets()
            
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT title, author
                FROM books 
                WHERE title LIKE ? OR author LIKE ?
                LIMIT 5
            """, (f'%{query}%', f'%{query}%'))
            suggestions = cursor.fetchall()
            conn.close()
            
            if suggestions:
                # Use MDCard for each suggestion to avoid overlap
                suggestions_container.height = len(suggestions) * dp(82)
                
                for title, author in suggestions:
                    # Use MDCard for clean, separated items
                    suggestion_card = MDCard(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=dp(70),
                        padding=dp(12),
                        spacing=dp(10),
                        md_bg_color=(1, 1, 1, 1),
                        elevation=1,
                        radius=[dp(10)]
                    )
                    
                    # Book Icon
                    book_icon = MDIcon(
                        icon='book-outline',
                        theme_text_color='Custom',
                        text_color=(0.13, 0.59, 0.95, 1),
                        size_hint=(None, None),
                        size=(dp(28), dp(28)),
                        pos_hint={'center_y': 0.5}
                    )
                    suggestion_card.add_widget(book_icon)
                    
                    # Text Info
                    text_box = BoxLayout(
                        orientation='vertical',
                        size_hint_x=1,
                        spacing=dp(3)
                    )
                    
                    title_label = MDLabel(
                        text=title,
                        theme_text_color='Custom',
                        text_color=(0.2, 0.2, 0.2, 1),
                        font_size='15sp',
                        bold=True,
                        size_hint_y=None,
                        height=dp(22),
                        shorten=True,
                        shorten_from='right',
                        text_size=(None, None)
                    )
                    text_box.add_widget(title_label)
                    
                    if author:
                        author_label = MDLabel(
                            text=f"by {author}",
                            theme_text_color='Custom',
                            text_color=(0.5, 0.5, 0.5, 1),
                            font_size='13sp',
                            size_hint_y=None,
                            height=dp(20),
                            shorten=True,
                            shorten_from='right',
                            text_size=(None, None)
                        )
                        text_box.add_widget(author_label)
                    
                    suggestion_card.add_widget(text_box)
                    
                    # Arrow
                    arrow = MDIcon(
                        icon='arrow-right',
                        theme_text_color='Custom',
                        text_color=(0.7, 0.7, 0.7, 1),
                        size_hint=(None, None),
                        size=(dp(24), dp(24)),
                        pos_hint={'center_y': 0.5}
                    )
                    suggestion_card.add_widget(arrow)
                    
                    def on_suggestion_click(instance, touch, t=title):
                        if instance.collide_point(*touch.pos):
                            search_field.text = t
                            suggestions_container.height = 0
                            suggestions_container.clear_widgets()
                            search_books(None)
                    
                    suggestion_card.bind(on_touch_down=on_suggestion_click)
                    suggestions_container.add_widget(suggestion_card)
            else:
                suggestions_container.height = 0
        
        Clock.schedule_once(do_search, 0.2)
    
    # Search Timer for Debounce
    search_timer = [None]
    
    def on_text_change(instance, value):
        """Handle text changes for live suggestions"""
        if search_timer[0]:
            search_timer[0].cancel()
        
        def do_suggest(dt):
            show_suggestions(value.strip())
        
        search_timer[0] = Clock.schedule_once(do_suggest, 0.4)
    
    search_field.bind(text=on_text_change)
    
    def search_books(instance):
        """Search books with modern results display"""
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
            # Results Header - Modern Design
            results_header_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(45),
                spacing=dp(10),
                padding=[dp(5), 0, 0, 0]
            )
            
            results_icon = MDIcon(
                icon='book-check',
                theme_text_color='Custom',
                text_color=(0.13, 0.59, 0.95, 1),
                size_hint=(None, None),
                size=(dp(28), dp(28)),
                pos_hint={'center_y': 0.5}
            )
            results_header_box.add_widget(results_icon)
            
            results_header = MDLabel(
                text=f"Found {len(books)} Result{'s' if len(books) > 1 else ''}",
                font_style='H6',
                bold=True,
                theme_text_color='Custom',
                text_color=(0.2, 0.2, 0.2, 1),
                size_hint_x=1,
                pos_hint={'center_y': 0.5}
            )
            results_header_box.add_widget(results_header)
            results_container.add_widget(results_header_box)
            
            # Show Results - Modern Cards
            for book_id, title, subject, author, year in books:
                book_card = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(140),
                    padding=dp(18),
                    spacing=dp(12)
                )
                
                with book_card.canvas.before:
                    Color(1, 1, 1, 1)
                    book_card.bg = RoundedRectangle(
                        size=book_card.size,
                        pos=book_card.pos,
                        radius=[dp(14)]
                    )
                    Color(0.13, 0.59, 0.95, 0.1)
                    book_card.accent = Line(
                        rounded_rectangle=(
                            book_card.x, book_card.y,
                            book_card.width, book_card.height,
                            dp(14)
                        ),
                        width=2
                    )
                
                book_card.bind(
                    size=lambda inst, val, bg=book_card: (
                        setattr(bg.bg, 'size', inst.size),
                        setattr(bg.accent, 'rounded_rectangle', (
                            inst.x, inst.y, inst.width, inst.height, dp(14)
                        ))
                    ),
                    pos=lambda inst, val, bg=book_card: (
                        setattr(bg.bg, 'pos', inst.pos),
                        setattr(bg.accent, 'rounded_rectangle', (
                            inst.x, inst.y, inst.width, inst.height, dp(14)
                        ))
                    )
                )
                
                # Book Info
                info_section = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(75),
                    spacing=dp(6)
                )
                
                # Title
                title_label = MDLabel(
                    text=title[:55] + ('...' if len(title) > 55 else ''),
                    font_style='Subtitle1',
                    bold=True,
                    theme_text_color='Custom',
                    text_color=(0.15, 0.15, 0.15, 1),
                    size_hint_y=None,
                    height=dp(26)
                )
                info_section.add_widget(title_label)
                
                # Author
                if author:
                    author_label = MDLabel(
                        text=f"✍️ {author[:40]}" + ('...' if len(author) > 40 else ''),
                        font_style='Body2',
                        theme_text_color='Custom',
                        text_color=(0.4, 0.4, 0.4, 1),
                        size_hint_y=None,
                        height=dp(22)
                    )
                    info_section.add_widget(author_label)
                
                # Subject and Year
                meta_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(22),
                    spacing=dp(15)
                )
                
                if subject:
                    subject_label = MDLabel(
                        text=f"📚 {subject[:25]}" + ('...' if len(subject or '') > 25 else ''),
                        font_style='Caption',
                        theme_text_color='Custom',
                        text_color=(0.5, 0.5, 0.5, 1),
                        size_hint_x=0.6
                    )
                    meta_box.add_widget(subject_label)
                
                if year:
                    year_label = MDLabel(
                        text=f"📅 {year}",
                        font_style='Caption',
                        theme_text_color='Custom',
                        text_color=(0.5, 0.5, 0.5, 1),
                        size_hint_x=0.4
                    )
                    meta_box.add_widget(year_label)
                
                info_section.add_widget(meta_box)
                book_card.add_widget(info_section)
                
                # Action Button
                view_btn = MDRaisedButton(
                    text="VIEW DETAILS",
                    size_hint=(1, None),
                    height=dp(42),
                    md_bg_color=(0.13, 0.59, 0.95, 1),
                    elevation=0
                )
                
                def make_view_handler(bid=book_id):
                    def handler(instance):
                        show_book_details(parent_instance, bid)
                    return handler
                
                view_btn.bind(on_release=make_view_handler())
                book_card.add_widget(view_btn)
                results_container.add_widget(book_card)
        else:
            # NOT FOUND - Show Popup Dialog
            def show_not_found_popup():
                popup = ModalView(
                    size_hint=(0.85, None),
                    height=dp(320),
                    background='',
                    background_color=(0, 0, 0, 0),
                    overlay_color=(0, 0, 0, 0.6)
                )
                
                popup_content = BoxLayout(
                    orientation='vertical',
                    padding=dp(25),
                    spacing=dp(20)
                )
                
                with popup_content.canvas.before:
                    Color(1, 1, 1, 1)
                    popup_content.bg = RoundedRectangle(
                        size=popup_content.size,
                        pos=popup_content.pos,
                        radius=[dp(20)]
                    )
                
                popup_content.bind(
                    size=lambda inst, val: setattr(inst.bg, 'size', inst.size),
                    pos=lambda inst, val: setattr(inst.bg, 'pos', inst.pos)
                )
                
                # Close button (X)
                close_btn_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(30)
                )
                close_btn_box.add_widget(BoxLayout())  # Spacer
                
                close_btn = MDIconButton(
                    icon='close-circle',
                    theme_text_color='Custom',
                    text_color=(0.5, 0.5, 0.5, 1),
                    size_hint=(None, None),
                    size=(dp(32), dp(32)),
                    on_release=lambda x: popup.dismiss()
                )
                close_btn_box.add_widget(close_btn)
                popup_content.add_widget(close_btn_box)
                
                # Icon
                icon_box = BoxLayout(
                    size_hint_y=None,
                    height=dp(60)
                )
                icon_box.add_widget(BoxLayout())
                not_found_icon = MDIcon(
                    icon='book-alert',
                    theme_text_color='Custom',
                    text_color=(0.96, 0.26, 0.21, 1),
                    size_hint=(None, None),
                    size=(dp(60), dp(60))
                )
                icon_box.add_widget(not_found_icon)
                icon_box.add_widget(BoxLayout())
                popup_content.add_widget(icon_box)
                
                # Title
                popup_content.add_widget(MDLabel(
                    text="No Results Found",
                    font_style='H5',
                    bold=True,
                    halign='center',
                    theme_text_color='Custom',
                    text_color=(0.2, 0.2, 0.2, 1),
                    size_hint_y=None,
                    height=dp(35)
                ))
                
                # Query display
                popup_content.add_widget(MDLabel(
                    text=f'"{query[:40]}..."' if len(query) > 40 else f'"{query}"',
                    font_style='Body1',
                    halign='center',
                    theme_text_color='Custom',
                    text_color=(0.4, 0.4, 0.4, 1),
                    size_hint_y=None,
                    height=dp(25)
                ))
                
                # Description
                popup_content.add_widget(MDLabel(
                    text="This book is not in our library.\nWould you like to search the web?",
                    font_style='Body2',
                    halign='center',
                    theme_text_color='Custom',
                    text_color=(0.5, 0.5, 0.5, 1),
                    size_hint_y=None,
                    height=dp(40)
                ))
                
                # Buttons
                btn_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(50),
                    spacing=dp(12),
                    padding=[dp(10), 0]
                )
                
                # Close Button
                cancel_btn = MDRaisedButton(
                    text="CANCEL",
                    size_hint=(0.45, None),
                    height=dp(50),
                    md_bg_color=(0.9, 0.9, 0.9, 1),
                    theme_text_color='Custom',
                    text_color=(0.3, 0.3, 0.3, 1),
                    elevation=0,
                    on_release=lambda x: popup.dismiss()
                )
                btn_box.add_widget(cancel_btn)
                
                # Web Search Button
                def open_browser_and_close(instance):
                    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    open_url_safely(search_url)
                    popup.dismiss()
                
                web_btn = MDRaisedButton(
                    text="🌐 SEARCH WEB",
                    size_hint=(0.55, None),
                    height=dp(50),
                    md_bg_color=(0.13, 0.59, 0.95, 1),
                    elevation=2,
                    on_release=open_browser_and_close
                )
                btn_box.add_widget(web_btn)
                
                popup_content.add_widget(btn_box)
                popup.add_widget(popup_content)
                popup.open()
            
            # Show the popup
            show_not_found_popup()
    
    search_field.bind(on_text_validate=search_books)
    
    # Bind search button
    search_btn.bind(on_release=search_books)
    
    main_container.add_widget(results_container)
    content_scroll.add_widget(main_container)
