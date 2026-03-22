## ✨ AI Chatbot Integration - Setup Guide

### Quick Start
The library app now includes an AI-powered chatbot accessible directly from the user dashboard!

### 🔧 Setup (One-time)

#### 1. Get Groq API Key (Free)
- Go to https://console.groq.com
- Create a free account (no credit card needed!)
- Generate an API key
- Copy the key

#### 2. Create Local Configuration File
```bash
# Copy the template
cp .env.example .env

# Edit .env and paste your API key
GROQ_API_KEY=your_key_here
```

#### 3. Verify Setup
```bash
python test_ai_api.py
```
You should see: `✅ API Configuration is READY!`

### 🤖 Using AI Chatbot

#### In the App
1. Login as a user
2. Navigate to dashboard
3. Click the **🤖 AI Chat** tab (5th button)
4. Type your query and get instant AI responses!

#### Features
- **Book Recommendations** - Get personalized book suggestions
- **Library Help** - Learn about app features
- **Query Resolution** - Solve common issues
- **Context Memory** - AI remembers recent conversation

#### Example Queries
- "Recommend a suspense thriller for me"
- "How do I search for magazines?"
- "What Python books are good for beginners?"
- "How does the reading history work?"

### 📋 Model Used
- **Groq llama-3.3-70b-versatile**
  - Fast response times (~200ms)
  - Free tier: 30 requests/minute
  - Excellent for book recommendations

### ⚠️ Important Security Notes

**⚠️ API Key Already Exposed**  
The Groq API key was accidentally pushed to this repository. Please:

1. **Immediately regenerate your old API key** at https://console.groq.com
   - The old key should be considered compromised
   - Generate a new one
   - Update your .env file with the new key

2. **NEVER commit .env files**
   - .env is in .gitignore
   - Always use .env.example as template
   - Keep API keys local only

### 📁 Files Changed
- `main.py` - Added AI module initialization on startup
- `user_modules/user_dashboard.py` - Added 5th tab for AI Chat
- `ai_chatbot.py` - Core AI module with Groq API integration
- `.env.example` - Template for local configuration
- `.gitignore` - Updated to exclude .env files

### 🚀 Architecture
```
User Dashboard (5 tabs)
└── AI Chat Tab
    └── AIChat Widget (Kivy/KivyMD UI)
        └── query_groq() function
            └── Groq REST API
                └── llama-3.3-70b-versatile model
```

### 📚 Chat History
- Saves to `data/chat_history.json`
- Persists between app sessions
- Last 5 messages used for context
- Clear from settings if needed

### 🆘 Troubleshooting

**Issue: "API Key not found" warning**
- Solution: Copy .env.example to .env and add your key

**Issue: No response from AI**
- Check: API key is valid at https://console.groq.com
- Check: Running within rate limit (30 req/min)
- Check: Internet connection active

**Issue: Slow responses**
- Normal: First response takes ~200-500ms
- Check: Groq service status if consistent slowdowns

### 📖 More Info
- Groq Docs: https://console.groq.com/docs
- Model Card: llama-3.3-70b-versatile
- Free Tier Limits: 30 requests/minute

---
**Last Updated:** March 22, 2026
