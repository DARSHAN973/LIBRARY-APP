"""
ai_chatbot.py
AI-powered chatbot module for library app using Groq API.
Provides book recommendations, query resolution, and library assistance.
"""

import json
import os
import threading
try:
    import requests
except Exception:
    requests = None
from datetime import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
try:
    from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRectangleFlatButton
except Exception:
    from kivymd.uix.button import MDRaisedButton, MDFlatButton
    MDRectangleFlatButton = MDFlatButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp

# ─── CONFIGURATION ──────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_data_dir():
    """Return a writable app data directory (works on Android and desktop)."""
    try:
        app = App.get_running_app()
        if app and getattr(app, "user_data_dir", None):
            return os.path.join(app.user_data_dir, "data")
    except Exception:
        pass
    return os.path.join(os.getcwd(), "data")


def get_chat_history_file():
    return os.path.join(get_data_dir(), "chat_history.json")

# ─── HELPERS ────────────────────────────────────────────────────────────────

def ensure_chat_dir():
    """Ensure data directory exists."""
    os.makedirs(get_data_dir(), exist_ok=True)

def load_chat_history():
    """Load previous chat messages from file."""
    try:
        ensure_chat_dir()
    except Exception:
        return []
    chat_file = get_chat_history_file()
    if os.path.exists(chat_file):
        try:
            with open(chat_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_chat_history(messages):
    """Save chat messages to file."""
    try:
        ensure_chat_dir()
        with open(get_chat_history_file(), "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2)
    except Exception:
        # Do not crash UI if storage is unavailable on device.
        pass

def get_system_prompt():
    """System prompt for library assistant AI."""
    return """You are a helpful library assistant AI. Your role is to:
1. Answer questions about books (title, author, genre, plot)
2. Recommend books based on user interests
3. Help with library features and how to use the app
4. Suggest reading based on genres or authors
5. Resolve common user issues with the library app

Be concise, friendly, and helpful. Keep responses under 300 characters when possible.
Always prioritize helping users find or understand books."""

def query_groq(user_message, chat_history):
    """Send message to Groq API and get response."""
    if not GROQ_API_KEY:
        return "⚠️ AI API key not configured. Please set GROQ_API_KEY in .env file."
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build messages with context
    messages = [
        {"role": "system", "content": get_system_prompt()}
    ]
    
    # Add previous messages (keep last 5 for context)
    for msg in chat_history[-5:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Add current user message
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 0.9
    }
    
    try:
        if requests is None:
            return "❌ Network library not available. Please check your installation."
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ API Error: {str(e)[:100]}"

# ─── UI COMPONENTS ──────────────────────────────────────────────────────────

class AIChat(MDBoxLayout):
    """Main AI chatbot UI component."""
    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [dp(10), dp(6), dp(10), dp(6)]
        self.spacing = dp(6)
        self.size_hint_y = None
        self.height = max(Window.height - dp(210), dp(440))
        self.user_id = user_id
        
        # Load chat history
        self.chat_history = load_chat_history()
        
        # Header
        header_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(42),
            spacing=dp(6)
        )
        header_icon = MDIcon(
            icon="robot-happy-outline",
            theme_text_color="Custom",
            text_color=(0.13, 0.59, 0.95, 1),
            size_hint=(None, None),
            size=(dp(32), dp(32)),
            pos_hint={"center_y": 0.5}
        )
        header_label = MDLabel(
            text="Library AI Assistant",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            size_hint_x=1,
            valign="middle"
        )
        clear_btn = MDRectangleFlatButton(
            text="Clear",
            line_color=(0.13, 0.59, 0.95, 1),
            text_color=(0.13, 0.59, 0.95, 1),
            size_hint=(None, None),
            size=(dp(78), dp(34)),
            on_press=self.clear_chat
        )
        header_box.add_widget(header_icon)
        header_box.add_widget(header_label)
        header_box.add_widget(clear_btn)
        self.add_widget(header_box)
        
        # Chat display area (scrollable)
        self.chat_scroll = MDScrollView(size_hint=(1, 1))
        self.chat_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(4),
            padding=[dp(4), dp(2), dp(4), dp(2)],
            size_hint_y=None
        )
        self.chat_box.bind(minimum_height=self.chat_box.setter("height"))
        self.chat_scroll.add_widget(self.chat_box)
        self.add_widget(self.chat_scroll)
        
        # Load and display previous messages
        self._refresh_messages()
        
        # Input area
        input_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(68),
            spacing=dp(8),
            padding=[dp(0), dp(2), dp(0), dp(2)]
        )
        
        self.message_input = MDTextField(
            hint_text="Ask me about books, recommendations...",
            size_hint=(1, None),
            height=dp(52),
            mode="rectangle",
            multiline=False
        )
        input_box.add_widget(self.message_input)
        
        send_btn = MDRaisedButton(
            text="Send",
            size_hint=(None, None),
            size=(dp(82), dp(46)),
            on_press=self.send_message
        )
        input_box.add_widget(send_btn)
        self.add_widget(input_box)
    
    def _refresh_messages(self):
        """Refresh chat display from history."""
        self.chat_box.clear_widgets()
        if not self.chat_history:
            # Show welcome message
            welcome = MDLabel(
                text="👋 Hello! I'm your library AI assistant.\nAsk me about books, recommendations, or how to use the app!",
                size_hint_y=None,
                height=dp(52),
                halign="center",
                theme_text_color="Custom",
                text_color=(0.5, 0.5, 0.5, 1)
            )
            self.chat_box.add_widget(welcome)
        else:
            for msg in self.chat_history:
                self._add_message_bubble(msg["content"], msg["role"] == "user")
        
        self.chat_box.height = self.chat_box.minimum_height
        # Auto-scroll to bottom
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
    
    def _add_message_bubble(self, text, is_user):
        """Add a single message bubble."""
        bubble_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(1),
            spacing=dp(6),
            padding=[0, dp(2), 0, dp(2)]
        )
        
        leading_spacer = MDLabel(size_hint_x=0.22, size_hint_y=None, height=dp(1))
        trailing_spacer = MDLabel(size_hint_x=0.22, size_hint_y=None, height=dp(1))

        bubble = MDCard(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(2),
            size_hint_x=0.78,
            size_hint_y=None,
            radius=[dp(16), dp(16), dp(16), dp(16)],
            md_bg_color=(0.2, 0.6, 0.95, 1) if is_user else (0.95, 0.95, 0.95, 1)
        )
        
        msg_label = MDLabel(
            text=text,
            size_hint_y=None,
            halign="left",
            valign="middle",
            text_color=(1, 1, 1, 1) if is_user else (0, 0, 0, 1),
            theme_text_color="Custom"
        )
        
        bubble.add_widget(msg_label)
        if is_user:
            bubble_box.add_widget(leading_spacer)
            bubble_box.add_widget(bubble)
        else:
            bubble_box.add_widget(bubble)
            bubble_box.add_widget(trailing_spacer)
        
        def set_height(*args):
            bubble_width = max(bubble.width - dp(24), dp(120))
            msg_label.text_size = (bubble_width, None)
            msg_label.texture_update()
            text_height = msg_label.texture_size[1]
            bubble_height = max(text_height + dp(16), dp(38))
            msg_label.height = text_height
            bubble.height = bubble_height
            bubble_box.height = bubble_height + dp(4)
            self.chat_box.height = self.chat_box.minimum_height
        
        bubble.bind(width=set_height)
        Clock.schedule_once(set_height, 0.05)
        self.chat_box.add_widget(bubble_box)
    
    def _scroll_to_bottom(self):
        """Auto-scroll to latest message."""
        if self.chat_scroll:
            self.chat_scroll.scroll_y = 0
    
    def send_message(self, instance):
        """Send user message and get AI response."""
        user_msg = self.message_input.text.strip()
        if not user_msg:
            return
        
        # Add user message to display
        self.message_input.text = ""
        self._add_message_bubble(user_msg, True)
        
        # Add to history
        self.chat_history.append({
            "role": "user",
            "content": user_msg,
            "timestamp": datetime.now().isoformat()
        })
        
        # Show loading indicator
        loading_msg = MDLabel(
            text="🤖 Thinking...",
            size_hint_y=None,
            height=dp(30),
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1)
        )
        self.chat_box.add_widget(loading_msg)
        self._scroll_to_bottom()
        
        # Get AI response in background
        def get_response():
            response = query_groq(user_msg, self.chat_history)
            Clock.schedule_once(
                lambda dt: self._display_ai_response(response, loading_msg),
                0
            )
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def _display_ai_response(self, response, loading_msg):
        """Display AI response in chat."""
        if loading_msg in self.chat_box.children:
            self.chat_box.remove_widget(loading_msg)
        
        # Add to history
        self.chat_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save to file
        save_chat_history(self.chat_history)
        
        # Display response
        self._add_message_bubble(response, False)
        self._scroll_to_bottom()
    
    def clear_chat(self, instance):
        """Clear chat history."""
        self.chat_history = []
        save_chat_history([])
        self._refresh_messages()


def show_ai_chat(content_scroll=None, user_id=None):
    """Open AI chat in a modal popup or add to content scroll view."""
    chat_widget = AIChat(user_id=user_id)
    
    if content_scroll is not None:
        # Match the same scroll-container structure used by the other tabs.
        main_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(15), dp(15), dp(15), dp(70)]
        )
        main_container.bind(minimum_height=main_container.setter("height"))
        main_container.add_widget(chat_widget)

        content_scroll.clear_widgets()
        content_scroll.add_widget(main_container)
    else:
        # Show as popup (original behavior)
        content = MDBoxLayout(orientation="vertical")
        content.add_widget(chat_widget)
        
        close_btn = MDFlatButton(
            text="Close Chat",
            size_hint_y=0.08,
            on_press=lambda x: popup.dismiss()
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title="Library AI Assistant",
            content=content,
            size_hint=(0.95, 0.9)
        )
        popup.open()
        return popup


# ─── INTEGRATION HELPER ──────────────────────────────────────────────────────

def init_ai_module(api_key):
    """Initialize AI module with API key (call from main.py)."""
    global GROQ_API_KEY
    GROQ_API_KEY = api_key
    ensure_chat_dir()
