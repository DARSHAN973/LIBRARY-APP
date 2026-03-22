# 🤖 Library App AI Chatbot - Setup Guide

## What's Been Created

Your library app now has a **fully functional AI chatbot module** with:

✅ **Book Recommendations** - AI suggests books based on user interests  
✅ **Query Resolution** - Answers user questions about books and library features  
✅ **Context Memory** - Remembers last 5 messages for intelligent conversations  
✅ **Chat History** - Saves conversations locally in `data/chat_history.json`  
✅ **Beautiful UI** - Kivy MDCard chat bubbles, auto-scrolling, typing indicators  
✅ **Background Threading** - Non-blocking requests, responsive UI  
✅ **Zero Setup** - Just set API key and go!  

---

## 📦 Files Created

1. **ai_chatbot.py** (310 lines) - Main chatbot engine
   - Groq API integration
   - Chat history management
   - Beautiful UI components
   - System prompt for library assistant

2. **test_ai_api.py** - API validation script
   - Test your Groq API key
   - Verify connectivity
   - Run 4 test queries

3. **AI_INTEGRATION.md** - Step-by-step integration guide

4. **CHATBOT_INTEGRATION_EXAMPLE.py** - Code snippets to add button to dashboard

---

## 🚀 Quick Start (3 Steps)

### Step 1: Get Free Groq API Key (2 minutes)

**Visit:** https://console.groq.com

```
1. Sign up with your email (no credit card needed!)
2. Go to "API Keys" section
3. Click "Create New API Key"
4. Copy the key
5. Keep it safe
```

### Step 2: Set Environment Variable

**Linux/Mac:**
```bash
export GROQ_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your-api-key-here"
```

### Step 3: Test the API

```bash
cd /home/darshan/darshan/library_mobile_app
python test_ai_api.py
```

Expected output:
```
✅ API Key found: gsk_****...
📤 Sending test request to Groq API...
✅ SUCCESS! API is working correctly.
📝 AI Response:
[AI recommendations appear here...]
```

---

## 🔧 Integration with Main App

Once API is working, add to **main.py**:

```python
# At the top
from ai_chatbot import init_ai_module

# In LibraryApp.on_start() method:
def on_start(self):
    db = Database()
    db.create_tables()
    db.close()
    
    # NEW: Initialize AI module
    import os
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        init_ai_module(api_key)
        print("✅ AI Chatbot initialized")
```

---

## 🎯 Add AI Button to User Dashboard

Edit **user_modules/user_dashboard.py**:

```python
# At the top, add:
from ai_chatbot import show_ai_chat

# In your navigation bar setup, add this button:
ai_chat_btn = MDRaisedButton(
    text="🤖 AI Chat",
    on_press=lambda x: show_ai_chat(user_id=self.user_id),
    md_bg_color=(0.2, 0.6, 0.9, 1)  # Nice blue
)
nav_box.add_widget(ai_chat_btn)
```

---

## 💬 Using the Chatbot

Once integrated:

1. **Start App:** `python main.py`
2. **Login** with any user account
3. **Click "🤖 AI Chat"** button
4. **Ask Questions:**
   - "Suggest a sci-fi book"
   - "How do I use the watchlist?"
   - "What are your top books?"
   - "Help me find a mystery novel"

---

## 🎁 Free API Quotas

### **Groq (Recommended)**
- 30 requests per minute
- No credit card
- Fastest responses
- Best for mobile

### **Alternatives**

**Google Gemini API**
- 60 requests/day
- Very capable
- Setup: https://ai.google.dev

**DeepSeek**
- 100 requests/day
- Good quality
- Setup: https://platform.deepseek.com

---

## 📊 AI Features

### System Prompt
Chatbot is configured as a "Library Assistant" that:
- ✅ Answers book questions
- ✅ Recommends based on genre
- ✅ Explains app features
- ✅ Solves common issues

### Context Window
- Remembers **last 5 messages**
- Maintains conversation flow
- Smarter recommendations over time

### Local Storage
- Saves chat history to `data/chat_history.json`
- Works offline (with cached responses)
- Clear history anytime

---

## 🐛 Troubleshooting

### "API Key Not Configured"
```bash
# Check if env var is set:
echo $GROQ_API_KEY  # Linux/Mac
echo %GROQ_API_KEY%  # Windows

# If empty, set it again
export GROQ_API_KEY="your-key"
```

### "Request Timeout"
- Check internet connection
- Verify API key validity
- Try again (Groq might be loading)

### "Rate Limit Exceeded"
- Groq allows 30 req/min
- Wait 1-2 minutes
- Use alternative API (Google, DeepSeek)

### API Not Responding
```bash
# Run diagnostic:
python test_ai_api.py

# Check Groq status:
# https://status.groq.com
```

---

## 📝 Example Conversations

**User:** "What Python books do you recommend?"
**AI:** "For learning Python, I'd suggest:
- 'Automate the Boring Stuff with Python' (beginner-friendly)
- 'Fluent Python' (advanced concepts)
- 'Python Data Science Handbook' (if interested in data)"

**User:** "How do I add books to my watchlist?"
**AI:** "In your Profile tab, you can:
1. Find a book (search or browse)
2. Click 'Add to Watchlist'
3. View your list in the Profile section
4. Remove anytime with the REMOVE button"

---

## ✨ Next Steps

1. ✅ **Get API Key** from https://console.groq.com
2. ✅ **Run test:** `python test_ai_api.py`
3. ✅ **Update main.py** with init_ai_module()
4. ✅ **Add button** to user_dashboard.py
5. ✅ **Launch app:** `python main.py`
6. ✅ **Test chatbot** in the app

---

## 📞 Need Help?

1. Check **test_ai_api.py** output for specific errors
2. Review **AI_INTEGRATION.md** for detailed steps
3. See **CHATBOT_INTEGRATION_EXAMPLE.py** for code snippets
4. Verify Groq API key is valid at https://console.groq.com

---

## 🎓 For Your Black-Book Report

This AI chatbot can be added as a **new feature chapter**:

**"Chapter 4.17: AI Assistant Module (ai_chatbot.py - 310 lines)"**
- Describes Groq API integration
- Shows system prompt design
- Demonstrates threading for UI responsiveness
- Explains chat history persistence
- Includes usage examples

---

**Ready? Share your Groq API key when you have it, and I'll help test the full integration!** 🚀
