"""
AI Chatbot Integration Guide
=============================

This guide explains how to integrate the AI chatbot module into your Library Mobile App.

STEP 1: Get Groq API Key
------------------------
1. Visit: https://console.groq.com
2. Sign up with email
3. Go to API Keys section
4. Copy your API key
5. Set it as environment variable:
   
   Linux/Mac:
   export GROQ_API_KEY="your-api-key-here"
   
   Windows (CMD):
   set GROQ_API_KEY=your-api-key-here
   
   Windows (PowerShell):
   $env:GROQ_API_KEY="your-api-key-here"

STEP 2: Install Dependencies
-----------------------------
pip install requests

STEP 3: Update main.py
----------------------
Add this at the top of main.py:
"""
from ai_chatbot import init_ai_module, show_ai_chat
"""

Then in LibraryApp.on_start() method, add:
"""
def on_start(self):
    db = Database()
    db.create_tables()
    db.close()
    
    # Initialize AI module with API key
    import os
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        init_ai_module(api_key)
"""

STEP 4: Add AI Chat Button to User Dashboard
--------------------------------------------
Edit user_modules/user_dashboard.py and add this button to the navigation area:

```python
from ai_chatbot import show_ai_chat

# In the UserDashboard class, add to __init__ or build method:
ai_btn = MDRaisedButton(
    text="🤖 AI Chat",
    on_press=lambda x: show_ai_chat(user_id=self.app.current_user_id)
)
nav_box.add_widget(ai_btn)
```

STEP 5: Test the Integration
-----------------------------
1. Start the app with: python main.py
2. Login with any user account
3. Look for "🤖 AI Chat" button in the user dashboard
4. Click it to open the chatbot
5. Try asking:
   - "Suggest a good science fiction book"
   - "How do I add a book to my watchlist?"
   - "What are some popular Python books?"

STEP 6: Use in Admin Dashboard (Optional)
------------------------------------------
You can also add AI help to admin sections. Just call show_ai_chat() from any admin screen.

FREE API QUOTAS
===============
Groq Free Tier:
- 30 requests per minute
- No credit card required
- Perfect for mobile app usage

ALTERNATIVES (if Groq has issues)
==================================

Option 2: Google Gemini API
- Limit: 60 requests/day (free tier)
- Setup: https://ai.google.dev
- Model: gemini-1.5-flash

Option 3: DeepSeek API
- Limit: 100 requests/day (free tier)
- Setup: https://plataform.deepseek.com
- Model: deepseek-chat

TROUBLESHOOTING
===============

Issue: "API key not configured"
Solution: 
  1. Make sure GROQ_API_KEY environment variable is set
  2. Restart the app
  3. Check: echo $GROQ_API_KEY (Linux/Mac)

Issue: "Error: Connection timeout"
Solution:
  1. Check internet connection
  2. Try again - Groq might be temporarily slow
  3. Check api.groq.com status

Issue: "Response is blank"
Solution:
  1. Check API key is valid
  2. Groq rate limit reached - wait a minute
  3. Try simpler question

FEATURES
========
✅ Contextual conversations (remembers last 5 messages)
✅ Book recommendations
✅ Library help and support
✅ Query resolution
✅ Chat history saved locally
✅ Works offline (stored history)
✅ Beautiful Kivy UI with chat bubbles
✅ Threaded requests (doesn't freeze UI)

"""
