"""
System Settings Module - App Information and Configuration
Clean settings interface for library management system
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime
import sqlite3
import json
import os
import platform


# Settings file path - store in data directory
SETTINGS_FILE = os.path.join('data', 'app_settings.json')


def load_settings():
    """Load app settings from file"""
    default_settings = {
        'items_per_page': 20
    }
    
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                return {**default_settings, **settings}
        except:
            return default_settings
    return default_settings


def save_settings(settings):
    """Save app settings to file"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)


def load_settings_content(content_scroll, parent_instance):
    """Load the System Settings screen"""
    # Clear existing content
    content_scroll.clear_widgets()
    
    main_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(15),
        padding=dp(15)
    )
    main_container.bind(minimum_height=main_container.setter('height'))
    
    # Load current settings
    current_settings = load_settings()
    settings_modified = {'changed': False}
    
    # ==================== HEADER ====================
    header_box = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(40),
        spacing=dp(10)
    )
    
    header_icon = MDIcon(
        icon='cog',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='28sp',
        size_hint_x=None,
        width=dp(35)
    )
    header_box.add_widget(header_icon)
    
    header = MDLabel(
        text="System Settings",
        font_style='H5',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    )
    header_box.add_widget(header)
    
    main_container.add_widget(header_box)
    
    # ==================== DESCRIPTION ====================
    desc_box = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(50),
        padding=[dp(5), 0]
    )
    
    desc_label = MDLabel(
        text="Configure your application preferences and view system information",
        font_style='Body2',
        theme_text_color='Secondary',
        halign='left',
        size_hint_y=None,
        height=dp(40)
    )
    desc_box.add_widget(desc_label)
    main_container.add_widget(desc_box)
    
    # ==================== APP INFORMATION (READ-ONLY) ====================
    app_info_section = create_settings_section(
        "App Information",
        "information",
        [
            ("App Name", "Library Management System", "application"),
            ("Version", "v1.0", "tag"),
            ("Platform", "Kivy + Python", "language-python"),
            ("Developer", "College Project", "school"),
        ],
        read_only=True
    )
    main_container.add_widget(app_info_section)
    
    # ==================== ITEMS PER PAGE SETTING ====================
    pagination_section = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(140),
        padding=dp(16),
        spacing=dp(12)
    )
    
    # Section background
    with pagination_section.canvas.before:
        Color(1, 1, 1, 1)
        pagination_section.bg_rect = RoundedRectangle(
            size=pagination_section.size,
            pos=pagination_section.pos,
            radius=[dp(10)]
        )
        Color(0.85, 0.85, 0.85, 1)
        pagination_section.border = Line(
            rounded_rectangle=(
                pagination_section.x,
                pagination_section.y,
                pagination_section.width,
                pagination_section.height,
                dp(10)
            ),
            width=1
        )
    
    def update_pagination_bg(instance, value):
        pagination_section.bg_rect.size = instance.size
        pagination_section.bg_rect.pos = instance.pos
        pagination_section.border.rounded_rectangle = (
            instance.x, instance.y, instance.width, instance.height, dp(10)
        )
    
    pagination_section.bind(size=update_pagination_bg, pos=update_pagination_bg)
    
    # Section header
    section_header = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(30),
        spacing=dp(8)
    )
    
    section_icon = MDIcon(
        icon='format-list-numbered',
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='20sp',
        size_hint_x=None,
        width=dp(25)
    )
    section_header.add_widget(section_icon)
    
    section_title = MDLabel(
        text="Items Per Page",
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    )
    section_header.add_widget(section_title)
    pagination_section.add_widget(section_header)
    
    # Description
    desc_label = MDLabel(
        text="Number of items shown in book and user lists",
        font_style='Caption',
        theme_text_color='Secondary',
        size_hint_y=None,
        height=dp(20)
    )
    pagination_section.add_widget(desc_label)
    
    # Dropdown for items per page
    items_row = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(50),
        spacing=dp(10)
    )
    
    items_label = MDLabel(
        text="Items:",
        font_style='Body2',
        theme_text_color='Primary',
        size_hint_x=0.3
    )
    items_row.add_widget(items_label)
    
    # Dropdown button
    dropdown_btn = MDRaisedButton(
        text=f"{current_settings['items_per_page']} items",
        size_hint_x=0.7,
        md_bg_color=(0.95, 0.95, 0.95, 1),
        theme_text_color='Primary'
    )
    
    def on_items_select(text_item):
        # text_item is the menu item that was clicked
        try:
            value = int(text_item.split()[0])
            current_settings['items_per_page'] = value
            dropdown_btn.text = f"{value} items"
            settings_modified['changed'] = True
        except:
            pass
    
    menu_items = [
        {
            "text": "10 items",
            "on_release": lambda x=None: (on_items_select("10 items"), menu.dismiss()),
        },
        {
            "text": "20 items",
            "on_release": lambda x=None: (on_items_select("20 items"), menu.dismiss()),
        },
        {
            "text": "50 items",
            "on_release": lambda x=None: (on_items_select("50 items"), menu.dismiss()),
        },
    ]
    
    menu = MDDropdownMenu(
        caller=dropdown_btn,
        items=menu_items,
        width_mult=4,
    )
    
    dropdown_btn.bind(on_release=lambda x: menu.open())
    items_row.add_widget(dropdown_btn)
    
    pagination_section.add_widget(items_row)
    main_container.add_widget(pagination_section)
    
    # ==================== DATABASE INFO (READ-ONLY) ====================
    # Get database stats
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    conn.close()
    
    db_info_section = create_settings_section(
        "Database Information",
        "database",
        [
            ("Database Type", "SQLite", "database-settings"),
            ("Storage", "Local (library.db)", "harddisk"),
            ("Status", "✅ Connected", "check-circle"),
            ("Total Books", str(total_books), "book-open-variant"),
            ("Total Users", str(total_users), "account-multiple"),
        ],
        read_only=True
    )
    main_container.add_widget(db_info_section)
    
    # ==================== SAVE BUTTON ====================
    def save_settings_action(instance):
        save_settings(current_settings)
        settings_modified['changed'] = False
        
        # Show success dialog
        success_dialog = MDDialog(
            title="Settings Saved",
            text=f"Settings have been saved successfully!\n\nItems per page: {current_settings['items_per_page']}",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: success_dialog.dismiss()
                )
            ]
        )
        success_dialog.open()
    
    save_btn = MDRaisedButton(
        text="SAVE SETTINGS",
        size_hint_y=None,
        height=dp(50),
        md_bg_color=(0.30, 0.69, 0.31, 1),
        on_release=save_settings_action
    )
    main_container.add_widget(save_btn)
    
    # ==================== FOOTER ====================
    footer_container = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        height=dp(65),
        padding=dp(15),
        spacing=dp(4)
    )
    
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
    
    today = datetime.now().strftime("%B %d, %Y")
    footer_info = MDLabel(
        text=f"Settings • Last updated: {today}",
        font_style='Caption',
        theme_text_color='Secondary',
        halign='center',
        size_hint_y=None,
        height=dp(16)
    )
    footer_container.add_widget(footer_info)
    
    main_container.add_widget(footer_container)
    
    content_scroll.add_widget(main_container)


def create_settings_section(title, icon_name, items, read_only=False):
    """Create a settings section card"""
    section = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        padding=dp(16),
        spacing=dp(12)
    )
    
    # Calculate height based on items
    section.height = dp(60 + (len(items) * 45))
    
    # Section background
    with section.canvas.before:
        Color(1, 1, 1, 1)
        section.bg_rect = RoundedRectangle(
            size=section.size,
            pos=section.pos,
            radius=[dp(12)]
        )
        Color(0.13, 0.59, 0.95, 0.1)
        section.highlight = RoundedRectangle(
            size=section.size,
            pos=section.pos,
            radius=[dp(12)]
        )
    
    def update_section_bg(instance, value):
        section.bg_rect.size = instance.size
        section.bg_rect.pos = instance.pos
        section.highlight.size = instance.size
        section.highlight.pos = instance.pos
    
    section.bind(size=update_section_bg, pos=update_section_bg)
    
    # Section header
    header = BoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height=dp(30),
        spacing=dp(8)
    )
    
    icon = MDIcon(
        icon=icon_name,
        theme_text_color='Custom',
        text_color=(0.13, 0.59, 0.95, 1),
        font_size='20sp',
        size_hint_x=None,
        width=dp(25)
    )
    header.add_widget(icon)
    
    title_label = MDLabel(
        text=title,
        font_style='Subtitle1',
        bold=True,
        theme_text_color='Primary',
        size_hint_x=1
    )
    header.add_widget(title_label)
    
    if read_only:
        readonly_badge = MDLabel(
            text="READ-ONLY",
            font_style='Caption',
            theme_text_color='Secondary',
            size_hint_x=None,
            width=dp(80),
            halign='right'
        )
        header.add_widget(readonly_badge)
    
    section.add_widget(header)
    
    # Items
    for label, value, item_icon in items:
        item_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            spacing=dp(8)
        )
        
        # Item icon
        item_icon_widget = MDIcon(
            icon=item_icon,
            theme_text_color='Secondary',
            font_size='18sp',
            size_hint_x=None,
            width=dp(25)
        )
        item_row.add_widget(item_icon_widget)
        
        # Label
        label_widget = MDLabel(
            text=label,
            font_style='Body2',
            theme_text_color='Secondary',
            size_hint_x=0.4
        )
        item_row.add_widget(label_widget)
        
        # Value
        value_widget = MDLabel(
            text=str(value),
            font_style='Body2',
            bold=True,
            theme_text_color='Primary',
            size_hint_x=0.6,
            halign='right'
        )
        item_row.add_widget(value_widget)
        
        section.add_widget(item_row)
    
    return section
