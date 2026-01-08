"""
Manage Books Module - Modern Mobile-Optimized Book Management
Clean, efficient book CRUD operations for admin dashboard
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.chip import MDChip
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.icon_definitions import md_icons
from functools import partial
import sqlite3


def create_book_card(book_data, edit_callback, delete_callback, view_callback):
    """
    Create a clean mobile-optimized card for a book
    
    Args:
        book_data: tuple (id, title, subject, publisher, year)
    """
    book_id, title, subject, publisher, year = book_data
    
    from kivymd.uix.label import MDIcon
    
    card = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        padding=dp(14),
        spacing=dp(10)
    )
    card.bind(minimum_height=card.setter('height'))
    
    # Card background
    with card.canvas.before:
        Color(1, 1, 1, 1)
        card.bg_rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(10)])
        Color(0.85, 0.85, 0.85, 1)
        card.border = Line(rounded_rectangle=(card.x, card.y, card.width, card.height, dp(10)), width=1)
    
    def update_card(instance, value):
        card.bg_rect.size = instance.size
        card.bg_rect.pos = instance.pos
        card.border.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, dp(10))
    
    card.bind(size=update_card, pos=update_card)
    
    # Title with icon (wrap to keep inside card)
    title_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(44), spacing=dp(8))
    
    book_icon = MDIcon(
        icon='book',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='24sp',
        size_hint_x=None,
        width=dp(30)
    )
    title_row.add_widget(book_icon)
    
    # Container for title to control width
    title_container = BoxLayout(size_hint_x=1)
    title_label = MDLabel(
        text=str(title),
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Primary',
        markup=True,
        halign='left',
        valign='middle',
        shorten=True,
        shorten_from='right',
        max_lines=2
    )
    # Bind to set text_size for proper wrapping and adjust row height as text grows
    title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))
    title_label.bind(texture_size=lambda instance, value: setattr(title_row, 'height', max(dp(44), value[1] + dp(8))))
    title_container.add_widget(title_label)
    title_row.add_widget(title_container)
    card.add_widget(title_row)
    
    # Info row
    info_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(25), spacing=dp(15))
    
    if subject:
        subject_box = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(140), spacing=dp(4))
        subject_icon = MDIcon(
            icon='tag',
            theme_text_color='Secondary',
            font_size='14sp',
            size_hint_x=None,
            width=dp(18)
        )
        subject_box.add_widget(subject_icon)
        subject_label = MDLabel(
            text=str(subject)[:18],
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_x=1
        )
        subject_box.add_widget(subject_label)
        info_row.add_widget(subject_box)
    
    if year:
        year_box = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(80), spacing=dp(4))
        year_icon = MDIcon(
            icon='calendar',
            theme_text_color='Secondary',
            font_size='14sp',
            size_hint_x=None,
            width=dp(18)
        )
        year_box.add_widget(year_icon)
        year_label = MDLabel(
            text=str(year)[:4],
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_x=1
        )
        year_box.add_widget(year_label)
        info_row.add_widget(year_box)
    
    card.add_widget(info_row)
    
    # Publisher (if exists)
    if publisher:
        pub_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20), spacing=dp(4))
        pub_icon = MDIcon(
            icon='domain',
            theme_text_color='Hint',
            font_size='12sp',
            size_hint_x=None,
            width=dp(16)
        )
        pub_row.add_widget(pub_icon)
        pub_label = MDLabel(
            text=str(publisher)[:40] + '...' if len(str(publisher)) > 40 else str(publisher),
            font_style='Caption',
            theme_text_color='Hint',
            size_hint_x=1
        )
        pub_row.add_widget(pub_label)
        card.add_widget(pub_row)
    
    # Action buttons
    actions_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(32),
        spacing=dp(6)
    )
    
    # View button
    view_btn = MDIconButton(
        icon='eye',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        on_release=lambda x: view_callback(book_id)
    )
    actions_box.add_widget(view_btn)
    
    # Edit button
    edit_btn = MDIconButton(
        icon='pencil',
        theme_text_color='Custom',
        text_color=(0.30, 0.69, 0.31, 1),
        on_release=lambda x: edit_callback(book_id)
    )
    actions_box.add_widget(edit_btn)
    
    # Delete button
    delete_btn = MDIconButton(
        icon='delete',
        theme_text_color='Custom',
        text_color=(0.96, 0.26, 0.21, 1),
        on_release=lambda x: delete_callback(book_id)
    )
    actions_box.add_widget(delete_btn)
    
    card.add_widget(actions_box)
    return card


def create_loading_overlay():
    """Create loading spinner overlay"""
    overlay = BoxLayout(
        orientation='vertical',
        size_hint=(1, None),
        height=dp(100),
        padding=dp(20)
    )
    
    spinner = MDSpinner(
        size_hint=(None, None),
        size=(dp(46), dp(46)),
        pos_hint={'center_x': 0.5},
        active=True
    )
    
    label = MDLabel(
        text="Loading books...",
        font_style='Caption',
        theme_text_color='Secondary',
        halign='center',
        size_hint_y=None,
        height=dp(30)
    )
    
    overlay.add_widget(spinner)
    overlay.add_widget(label)
    return overlay


def create_styled_dropdown(hint_text, values, callback):
    """Create modern filter chip selector"""
    container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(70),
        spacing=dp(5)
    )
    
    # Label
    label = MDLabel(
        text=hint_text,
        font_style='Caption',
        bold=True,
        theme_text_color='Secondary',
        size_hint_y=None,
        height=dp(18)
    )
    container.add_widget(label)
    
    # Dropdown button - modern style
    dropdown_btn = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(46),
        padding=(dp(15), 0),
        spacing=dp(10)
    )
    
    with dropdown_btn.canvas.before:
        Color(1, 1, 1, 1)
        dropdown_btn.bg = RoundedRectangle(
            size=dropdown_btn.size,
            pos=dropdown_btn.pos,
            radius=[dp(10)]
        )
        Color(0.13, 0.59, 0.95, 1)
        dropdown_btn.border = Line(
            rounded_rectangle=(dropdown_btn.x, dropdown_btn.y, dropdown_btn.width, dropdown_btn.height, dp(10)),
            width=1.5
        )
    
    def update_dropdown_graphics(instance, value):
        dropdown_btn.bg.size = instance.size
        dropdown_btn.bg.pos = instance.pos
        dropdown_btn.border.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, dp(10))
    
    dropdown_btn.bind(size=update_dropdown_graphics, pos=update_dropdown_graphics)
    
    # Icon
    from kivymd.uix.label import MDIcon
    icon = MDIcon(
        icon='filter-variant',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='20sp',
        size_hint_x=None,
        width=dp(25)
    )
    dropdown_btn.add_widget(icon)
    
    # Selected value label
    dropdown_label = MDLabel(
        text=values[0] if values else hint_text,
        font_style='Body2',
        theme_text_color='Primary',
        size_hint_x=1
    )
    dropdown_btn.add_widget(dropdown_label)
    
    # Dropdown arrow icon
    arrow_icon = MDIcon(
        icon='chevron-down',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='20sp',
        size_hint_x=None,
        width=dp(25)
    )
    dropdown_btn.add_widget(arrow_icon)
    
    # Create dropdown menu
    menu_items = [{"text": v, "on_release": lambda x=v: callback(x, dropdown_label)} for v in values]
    menu = MDDropdownMenu(
        caller=dropdown_btn,
        items=menu_items,
        width_mult=4,
        max_height=dp(300)
    )
    
    # Make button clickable
    from kivy.uix.behaviors import ButtonBehavior
    class ClickableDropdown(ButtonBehavior, BoxLayout):
        pass
    
    clickable = ClickableDropdown()
    clickable.add_widget(container)
    clickable.bind(on_press=lambda x: menu.open())
    
    return clickable, dropdown_label


def create_pagination_controls(current_page, total_pages, callback):
    """Create pagination controls"""
    pagination = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(50),
        spacing=dp(8),
        padding=dp(10)
    )
    
    # Previous button
    prev_btn = MDIconButton(
        icon='chevron-left',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1) if current_page > 1 else (0.7, 0.7, 0.7, 1),
        disabled=current_page <= 1,
        on_release=lambda x: callback(current_page - 1)
    )
    pagination.add_widget(prev_btn)
    
    # Page info
    page_label = MDLabel(
        text=f"Page {current_page} of {total_pages}",
        font_style='Body2',
        theme_text_color='Primary',
        halign='center',
        size_hint_x=1
    )
    pagination.add_widget(page_label)
    
    # Next button
    next_btn = MDIconButton(
        icon='chevron-right',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1) if current_page < total_pages else (0.7, 0.7, 0.7, 1),
        disabled=current_page >= total_pages,
        on_release=lambda x: callback(current_page + 1)
    )
    pagination.add_widget(next_btn)
    
    return pagination


def load_manage_books_content(content_scroll, parent_instance):
    """
    Main function to load Manage Books interface with pagination
    
    Args:
        content_scroll: ScrollView to add content to
        parent_instance: AdminDashboard instance for callbacks
    """
    # Clear existing content
    content_scroll.clear_widgets()
    
    # Main container
    main_container = BoxLayout(
        orientation='vertical',
        spacing=dp(12),
        size_hint_y=None,
        padding=dp(10)
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # State variables
    state = {
        'current_page': 1,
        'books_per_page': 20,
        'total_books': 0,
        'total_pages': 1,
        'search_text': '',
        'selected_subject': 'All Subjects',
        'selected_publisher': 'All Publishers'
    }
    
    # ==================== HEADER ====================
    from kivymd.uix.label import MDIcon
    
    header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(10)
    )
    
    header_icon = MDIcon(
        icon='book-multiple',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='28sp',
        size_hint_x=None,
        width=dp(35)
    )
    header_box.add_widget(header_icon)
    
    header = MDLabel(
        text="Manage Books",
        font_style='H5',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    )
    header_box.add_widget(header)
    main_container.add_widget(header_box)
    
    # ==================== SEARCH BAR ====================
    search_field = MDTextField(
        hint_text="Search books by title, subject, publisher...",
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    main_container.add_widget(search_field)
    
    # ==================== FILTERS ====================
    # Show loading message while getting filter data
    filters_container = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(56),
        spacing=dp(15)
    )
    
    # Get filter data
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Limit subject names to prevent overflow
    cursor.execute("SELECT DISTINCT subject FROM books WHERE subject IS NOT NULL AND subject != '' ORDER BY subject")
    all_subjects_raw = [s[0] for s in cursor.fetchall()]
    # Filter out subjects with non-ASCII characters and clean them
    all_subjects = [s for s in all_subjects_raw if s and s.isascii() and s.isprintable()]
    # Truncate long subject names to max 25 characters
    subjects = ['All Subjects'] + [s[:25] + '...' if len(s) > 25 else s for s in all_subjects]
    
    cursor.execute("SELECT DISTINCT publisher FROM books WHERE publisher IS NOT NULL AND publisher != '' ORDER BY publisher LIMIT 30")
    all_publishers = [pub[0] for pub in cursor.fetchall() if pub[0]]
    # Truncate long publisher names to max 25 characters
    publishers = ['All Publishers'] + [p[:25] + '...' if len(p) > 25 else p for p in all_publishers]
    conn.close()

    # Shared spinner styling helper
    def style_spinner(spinner_widget):
        spinner_widget.size_hint_y = None
        spinner_widget.height = dp(50)
        spinner_widget.padding = [dp(12), dp(10)]
        spinner_widget.background_normal = ''
        spinner_widget.background_down = ''
        spinner_widget.background_color = (1, 1, 1, 1)
        spinner_widget.color = (0.2, 0.2, 0.2, 1)
        spinner_widget.halign = 'left'
        spinner_widget.valign = 'middle'
        
        # Bind to set proper text_size for left alignment
        def update_text_size(instance, value):
            instance.text_size = (value[0] - dp(24), None)  # Account for padding
        spinner_widget.bind(size=update_text_size)

        with spinner_widget.canvas.before:
            Color(1, 1, 1, 1)
            spinner_widget.bg_rect = RoundedRectangle(size=spinner_widget.size, pos=spinner_widget.pos, radius=[dp(10)])
            Color(0.85, 0.85, 0.85, 1)
            spinner_widget.border_line = Line(rounded_rectangle=(spinner_widget.x, spinner_widget.y, spinner_widget.width, spinner_widget.height, dp(10)), width=1)

        def update_spinner_bg(instance, value):
            spinner_widget.bg_rect.size = instance.size
            spinner_widget.bg_rect.pos = instance.pos
            spinner_widget.border_line.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, dp(10))

        spinner_widget.bind(size=update_spinner_bg, pos=update_spinner_bg)
    
    # Create custom spinner option class
    from kivy.uix.button import Button
    
    class CustomSpinnerOption(Button):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.background_normal = ''
            self.background_color = (1, 1, 1, 1)  # White background
            self.color = (0.2, 0.2, 0.2, 1)  # Dark text
            self.halign = 'left'
            self.valign = 'middle'
            self.size_hint_y = None
            self.height = dp(50)
            self.padding = [dp(10), 0]
            # Bind size to set text_size for proper left alignment
            self.bind(size=self._update_text_size)
        
        def _update_text_size(self, instance, value):
            self.text_size = (self.width - dp(20), None)
    
    # Subject filter
    subject_spinner = Spinner(
        text='All Subjects',
        values=subjects,
        size_hint_x=0.5,
        option_cls=CustomSpinnerOption
    )
    style_spinner(subject_spinner)
    
    def on_subject_select(spinner, text):
        state['selected_subject'] = text
        state['current_page'] = 1
        load_books_page(books_container, pagination_container, state, search_field, parent_instance)
    
    subject_spinner.bind(text=on_subject_select)
    filters_container.add_widget(subject_spinner)
    
    # Publisher filter
    publisher_spinner = Spinner(
        text='All Publishers',
        values=publishers,
        size_hint_x=0.5,
        option_cls=CustomSpinnerOption
    )
    style_spinner(publisher_spinner)
    
    def on_publisher_select(spinner, text):
        state['selected_publisher'] = text
        state['current_page'] = 1
        load_books_page(books_container, pagination_container, state, search_field, parent_instance)
    
    publisher_spinner.bind(text=on_publisher_select)
    filters_container.add_widget(publisher_spinner)
    
    main_container.add_widget(filters_container)
    
    # ==================== ACTION BUTTONS ====================
    actions_bar = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(50),
        spacing=dp(10)
    )
    
    # Add New Book button
    add_book_btn = MDRaisedButton(
        text="Add Book",
        icon="book-plus",
        md_bg_color=(0.13, 0.59, 0.95, 1),
        size_hint_x=0.5,
        on_release=lambda x: show_add_book_form(parent_instance, lambda: load_books_page(books_container, pagination_container, state, search_field, parent_instance))
    )
    actions_bar.add_widget(add_book_btn)
    
    # Refresh button
    refresh_btn = MDRaisedButton(
        text="Refresh",
        icon="refresh",
        md_bg_color=(0.30, 0.69, 0.31, 1),
        size_hint_x=0.5,
        on_release=lambda x: load_books_page(books_container, pagination_container, state, search_field, parent_instance)
    )
    actions_bar.add_widget(refresh_btn)
    
    main_container.add_widget(actions_bar)
    
    # ==================== PAGINATION (TOP) ====================
    pagination_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(50)
    )
    main_container.add_widget(pagination_container)
    
    # ==================== BOOKS CONTAINER ====================
    books_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(15)
    )
    books_container.bind(minimum_height=books_container.setter('height'))
    main_container.add_widget(books_container)
    
    # ==================== PAGINATION (BOTTOM) ====================
    pagination_bottom = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(50)
    )
    main_container.add_widget(pagination_bottom)
    
    # ==================== FOOTER ====================
    from datetime import datetime
    
    footer_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(65),
        padding=dp(15),
        spacing=dp(4)
    )
    
    # Footer background
    with footer_container.canvas.before:
        Color(0.96, 0.96, 0.96, 1)
        footer_container.bg_rect = RoundedRectangle(
            size=footer_container.size,
            pos=footer_container.pos,
            radius=[dp(8)]
        )
    
    def update_footer_bg(instance, value):
        footer_container.bg_rect.size = instance.size
        footer_container.bg_rect.pos = instance.pos
    
    footer_container.bind(size=update_footer_bg, pos=update_footer_bg)
    
    # Footer title
    footer_title = MDLabel(
        text="Library Management System (Admin)",
        font_style='Caption',
        bold=True,
        theme_text_color='Primary',
        halign='center',
        size_hint_y=None,
        height=dp(18)
    )
    footer_container.add_widget(footer_title)
    
    # Footer info
    today = datetime.now().strftime("%B %d, %Y")
    footer_info = MDLabel(
        text=f"DB: SQLite • Last updated: {today}",
        font_style='Caption',
        theme_text_color='Secondary',
        halign='center',
        size_hint_y=None,
        height=dp(16)
    )
    footer_container.add_widget(footer_info)
    
    main_container.add_widget(footer_container)
    
    # Wire up search
    def on_search(instance):
        state['search_text'] = search_field.text
        state['current_page'] = 1
        load_books_page(books_container, pagination_container, state, search_field, parent_instance)
        load_books_page(books_container, pagination_bottom, state, search_field, parent_instance, update_pagination_only=True)
    
    search_field.bind(on_text_validate=on_search)
    
    # Initial load
    content_scroll.add_widget(main_container)
    Clock.schedule_once(lambda dt: load_books_page(books_container, pagination_container, state, search_field, parent_instance), 0.1)
    Clock.schedule_once(lambda dt: load_books_page(books_container, pagination_bottom, state, search_field, parent_instance, update_pagination_only=True), 0.1)


def load_books_page(books_container, pagination_container, state, search_field, parent_instance, update_pagination_only=False):
    """Load books for current page with pagination"""
    
    if not update_pagination_only:
        # Clear and show loading indicator
        books_container.clear_widgets()
        
        loading_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(20)
        )
        
        spinner = MDSpinner(
            size_hint=(None, None),
            size=(dp(46), dp(46)),
            pos_hint={'center_x': 0.5},
            active=True
        )
        
        loading_label = MDLabel(
            text="Loading books...",
            font_style='Body1',
            theme_text_color='Secondary',
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        loading_box.add_widget(spinner)
        loading_box.add_widget(loading_label)
        books_container.add_widget(loading_box)
    
    # Build query
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Count total books
    count_query = "SELECT COUNT(*) FROM books WHERE 1=1"
    where_params = []
    
    # Search filter (universal - searches all books)
    if search_field.text.strip():
        search_term = f"%{search_field.text.strip()}%"
        count_query += " AND (title LIKE ? OR subject LIKE ? OR publisher LIKE ? OR author LIKE ?)"
        where_params.extend([search_term, search_term, search_term, search_term])
    
    # Subject filter
    if state['selected_subject'] != 'All Subjects':
        count_query += " AND subject = ?"
        where_params.append(state['selected_subject'])
    
    # Publisher filter
    if state['selected_publisher'] != 'All Publishers':
        count_query += " AND publisher = ?"
        where_params.append(state['selected_publisher'])
    
    cursor.execute(count_query, where_params)
    state['total_books'] = cursor.fetchone()[0]
    state['total_pages'] = max(1, (state['total_books'] + state['books_per_page'] - 1) // state['books_per_page'])
    
    # Ensure current page is valid
    if state['current_page'] > state['total_pages']:
        state['current_page'] = state['total_pages']
    
    # Get books for current page
    offset = (state['current_page'] - 1) * state['books_per_page']
    data_query = count_query.replace("COUNT(*)", "id, title, subject, publisher, year_of_publication")
    data_query += f" ORDER BY title LIMIT {state['books_per_page']} OFFSET {offset}"
    
    cursor.execute(data_query, where_params)
    books = cursor.fetchall()
    conn.close()
    
    if not update_pagination_only:
        # Clear loading and add books
        books_container.clear_widgets()
        
        if books:
            for book in books:
                card = create_book_card(
                    book,
                    lambda book_id: show_edit_form(book_id, parent_instance, lambda: load_books_page(books_container, pagination_container, state, search_field, parent_instance)),
                    lambda book_id: show_delete_confirmation(book_id, parent_instance, lambda: load_books_page(books_container, pagination_container, state, search_field, parent_instance)),
                    lambda book_id: show_view_details(book_id, parent_instance)
                )
                books_container.add_widget(card)
        else:
            # No results
            no_results = MDLabel(
                text="No books found\nTry adjusting your search or filters",
                font_style='Body1',
                theme_text_color='Secondary',
                halign='center',
                size_hint_y=None,
                height=dp(100)
            )
            books_container.add_widget(no_results)
    
    # Update pagination
    pagination_container.clear_widgets()
    if state['total_pages'] > 1:
        pagination = create_pagination_controls(
            state['current_page'],
            state['total_pages'],
            lambda page: change_page(page, books_container, pagination_container, state, search_field, parent_instance)
        )
        pagination_container.add_widget(pagination)


def change_page(new_page, books_container, pagination_container, state, search_field, parent_instance):
    """Change to a different page"""
    state['current_page'] = new_page
    load_books_page(books_container, pagination_container, state, search_field, parent_instance)


def show_add_book_form(parent_instance, refresh_callback):
    """Show add book form in a modal dialog"""
    
    # Create form container
    form_container = BoxLayout(
        orientation='vertical',
        spacing=dp(15),
        padding=dp(20),
        size_hint_y=None
    )
    form_container.bind(minimum_height=form_container.setter('height'))
    
    # Title field (required)
    title_field = MDTextField(
        hint_text="Title *",
        required=True,
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(title_field)
    
    # Subject field
    subject_field = MDTextField(
        hint_text="Subject",
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(subject_field)
    
    # Author field
    author_field = MDTextField(
        hint_text="Author",
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(author_field)
    
    # Publisher field
    publisher_field = MDTextField(
        hint_text="Publisher",
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(publisher_field)
    
    # Year field
    year_field = MDTextField(
        hint_text="Year of Publication",
        mode="rectangle",
        input_filter="int",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(year_field)
    
    # PDF Link field
    pdf_field = MDTextField(
        hint_text="PDF Link (URL)",
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(pdf_field)
    
    # Scroll view for form
    scroll = ScrollView(size_hint=(1, None), height=dp(400))
    scroll.add_widget(form_container)
    
    # Dialog
    dialog = MDDialog(
        title="Add New Book",
        type="custom",
        content_cls=scroll,
        buttons=[
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: dialog.dismiss()
            ),
            MDRaisedButton(
                text="SAVE",
                md_bg_color=(0.13, 0.59, 0.95, 1),
                on_release=lambda x: save_new_book(
                    title_field.text,
                    subject_field.text,
                    author_field.text,
                    publisher_field.text,
                    year_field.text,
                    pdf_field.text,
                    dialog,
                    refresh_callback
                )
            ),
        ],
    )
    dialog.open()


def save_new_book(title, subject, author, publisher, year, pdf_link, dialog, refresh_callback):
    """Save new book to database"""
    
    # Validation
    if not title.strip():
        # Show error
        error_dialog = MDDialog(
            title="Error",
            text="Title is required!",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
        )
        error_dialog.open()
        return
    
    if year and not year.isdigit():
        error_dialog = MDDialog(
            title="Error",
            text="Year must be a number!",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
        )
        error_dialog.open()
        return
    
    if pdf_link and not (pdf_link.startswith('http://') or pdf_link.startswith('https://')):
        error_dialog = MDDialog(
            title="Error",
            text="PDF link must start with http:// or https://",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
        )
        error_dialog.open()
        return
    
    # Insert into database
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, subject, author, publisher, year_of_publication, pdf_link)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title.strip(), subject.strip() or None, author.strip() or None, 
              publisher.strip() or None, year or None, pdf_link.strip() or None))
        conn.commit()
        conn.close()
        
        dialog.dismiss()
        
        # Success message
        success_dialog = MDDialog(
            title="Success",
            text=f"Book '{title}' added successfully!",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: success_dialog.dismiss())]
        )
        success_dialog.open()
        
        # Refresh list
        if refresh_callback:
            refresh_callback()
    
    except Exception as e:
        error_dialog = MDDialog(
            title="Database Error",
            text=f"Failed to add book: {str(e)}",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
        )
        error_dialog.open()


def show_edit_form(book_id, parent_instance, refresh_callback):
    """Show edit book form"""
    
    # Get book data
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, subject, author, publisher, year_of_publication, pdf_link
        FROM books WHERE id = ?
    """, (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if not book:
        return
    
    title, subject, author, publisher, year, pdf_link = book
    
    # Create form container
    form_container = BoxLayout(
        orientation='vertical',
        spacing=dp(15),
        padding=dp(20),
        size_hint_y=None
    )
    form_container.bind(minimum_height=form_container.setter('height'))
    
    # Title field
    title_field = MDTextField(
        hint_text="Title *",
        text=title or '',
        required=True,
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(title_field)
    
    # Subject field
    subject_field = MDTextField(
        hint_text="Subject",
        text=subject or '',
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(subject_field)
    
    # Author field
    author_field = MDTextField(
        hint_text="Author",
        text=author or '',
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(author_field)
    
    # Publisher field
    publisher_field = MDTextField(
        hint_text="Publisher",
        text=publisher or '',
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(publisher_field)
    
    # Year field
    year_field = MDTextField(
        hint_text="Year of Publication",
        text=str(year) if year else '',
        mode="rectangle",
        input_filter="int",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(year_field)
    
    # PDF Link field
    pdf_field = MDTextField(
        hint_text="PDF Link (URL)",
        text=pdf_link or '',
        mode="rectangle",
        size_hint_y=None,
        height=dp(50)
    )
    form_container.add_widget(pdf_field)
    
    # Scroll view for form
    scroll = ScrollView(size_hint=(1, None), height=dp(400))
    scroll.add_widget(form_container)
    
    # Dialog
    dialog = MDDialog(
        title=f"Edit Book",
        type="custom",
        content_cls=scroll,
        buttons=[
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: dialog.dismiss()
            ),
            MDRaisedButton(
                text="UPDATE",
                md_bg_color=(0.30, 0.69, 0.31, 1),
                on_release=lambda x: update_book(
                    book_id,
                    title_field.text,
                    subject_field.text,
                    author_field.text,
                    publisher_field.text,
                    year_field.text,
                    pdf_field.text,
                    dialog,
                    refresh_callback
                )
            ),
        ],
    )
    dialog.open()


def update_book(book_id, title, subject, author, publisher, year, pdf_link, dialog, refresh_callback):
    """Update book in database"""
    
    # Validation
    if not title.strip():
        error_dialog = MDDialog(
            title="Error",
            text="Title is required!",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
        )
        error_dialog.open()
        return
    
    if year and not year.isdigit():
        error_dialog = MDDialog(
            title="Error",
            text="Year must be a number!",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
        )
        error_dialog.open()
        return
    
    if pdf_link and not (pdf_link.startswith('http://') or pdf_link.startswith('https://')):
        error_dialog = MDDialog(
            title="Error",
            text="PDF link must start with http:// or https://",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
        )
        error_dialog.open()
        return
    
    # Update database
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE books 
            SET title = ?, subject = ?, author = ?, publisher = ?, 
                year_of_publication = ?, pdf_link = ?
            WHERE id = ?
        """, (title.strip(), subject.strip() or None, author.strip() or None,
              publisher.strip() or None, year or None, pdf_link.strip() or None, book_id))
        conn.commit()
        conn.close()
        
        dialog.dismiss()
        
        # Success message
        success_dialog = MDDialog(
            title="Success",
            text=f"Book updated successfully!",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: success_dialog.dismiss())]
        )
        success_dialog.open()
        
        # Refresh list
        if refresh_callback:
            refresh_callback()
    
    except Exception as e:
        error_dialog = MDDialog(
            title="Database Error",
            text=f"Failed to update book: {str(e)}",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
        )
        error_dialog.open()


def show_view_details(book_id, parent_instance):
    """Show book details in a modal"""
    
    # Get book data
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, subject, author, publisher, year_of_publication, pdf_link,
               views, rating, rating_count
        FROM books WHERE id = ?
    """, (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if not book:
        return
    
    title, subject, author, publisher, year, pdf_link, views, rating, rating_count = book
    
    # Create details container
    details = BoxLayout(
        orientation='vertical',
        spacing=dp(10),
        padding=dp(15),
        size_hint_y=None
    )
    details.bind(minimum_height=details.setter('height'))
    
    # Add details
    def add_detail(label, value):
        if value:
            row = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(40), spacing=dp(2))
            row.add_widget(MDLabel(
                text=label,
                font_style='Caption',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(15)
            ))
            row.add_widget(MDLabel(
                text=str(value),
                font_style='Body2',
                theme_text_color='Primary',
                size_hint_y=None,
                height=dp(25)
            ))
            details.add_widget(row)
    
    add_detail("Title", title)
    add_detail("Subject", subject)
    add_detail("Author", author)
    add_detail("Publisher", publisher)
    add_detail("Year", year)
    add_detail("Views", views or 0)
    add_detail("Rating", f"{rating:.1f} ⭐ ({rating_count} ratings)" if rating and rating_count else "No ratings")
    
    if pdf_link:
        details.add_widget(MDRaisedButton(
            text="Open PDF Link",
            md_bg_color=(0.13, 0.59, 0.95, 1),
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: print(f"Open: {pdf_link}")  # TODO: Open in browser
        ))
    
    # Scroll view
    scroll = ScrollView(size_hint=(1, None), height=dp(400))
    scroll.add_widget(details)
    
    # Dialog
    dialog = MDDialog(
        title="Book Details",
        type="custom",
        content_cls=scroll,
        buttons=[
            MDFlatButton(
                text="CLOSE",
                on_release=lambda x: dialog.dismiss()
            ),
        ],
    )
    dialog.open()


def show_delete_confirmation(book_id, parent_instance, refresh_callback):
    """Show delete confirmation dialog"""
    
    # Get book title
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if not book:
        return
    
    title = book[0]
    
    def confirm_delete(dialog):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            conn.close()
            
            dialog.dismiss()
            
            # Success message
            success_dialog = MDDialog(
                title="Success",
                text=f"Book '{title}' deleted successfully!",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: success_dialog.dismiss())]
            )
            success_dialog.open()
            
            # Refresh list
            if refresh_callback:
                refresh_callback()
        
        except Exception as e:
            error_dialog = MDDialog(
                title="Database Error",
                text=f"Failed to delete book: {str(e)}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
            )
            error_dialog.open()
    
    # Confirmation dialog
    dialog = MDDialog(
        title="Confirm Delete",
        text=f"Are you sure you want to delete:\n\n'{title}'?\n\nThis action cannot be undone.",
        buttons=[
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: dialog.dismiss()
            ),
            MDRaisedButton(
                text="DELETE",
                md_bg_color=(0.96, 0.26, 0.21, 1),
                on_release=lambda x: confirm_delete(dialog)
            ),
        ],
    )
    dialog.open()
