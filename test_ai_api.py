#!/usr/bin/env python3
"""
test_ai_api.py
Quick test script to validate Groq API configuration and test responses.

Usage: python test_ai_api.py
"""

import os
import sys
import requests
import json
from datetime import datetime

def test_groq_api():
    """Test Groq API connection and response."""
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY environment variable not set!")
        print("\nTo set it:")
        print("  Linux/Mac:  export GROQ_API_KEY='your-api-key'")
        print("  Windows:    set GROQ_API_KEY=your-api-key")
        return False
    
    print("✅ API Key found:", api_key[:20] + "...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful library assistant. Give short, concise responses."
            },
            {
                "role": "user",
                "content": "Suggest a good book for someone who likes science fiction."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 256
    }
    
    print("\n📤 Sending test request to Groq API...")
    print("   Model: mixtral-8x7b-32768")
    print("   Message: 'Suggest a good book for someone who likes science fiction.'")
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=15
        )
        
        if response.status_code != 200:
            print(f"\n❌ API Error {response.status_code}:")
            print(response.text)
            return False
        
        data = response.json()
        ai_response = data["choices"][0]["message"]["content"]
        
        print("\n✅ SUCCESS! API is working correctly.")
        print("\n📝 AI Response:")
        print("-" * 50)
        print(ai_response)
        print("-" * 50)
        
        # Test multiple queries
        print("\n🔄 Testing multiple rapid queries...")
        test_questions = [
            "What is the best way to organize a library?",
            "Can you recommend Python books for beginners?",
            "How does reading history help recommendations?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            payload["messages"] = [
                {
                    "role": "system",
                    "content": "You are a helpful library assistant. Give short responses (under 50 words)."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                resp_text = response.json()["choices"][0]["message"]["content"]
                print(f"\n   Q{i}: {question}")
                print(f"   A{i}: {resp_text[:100]}...")
        
        print("\n" + "="*50)
        print("✅ API Configuration is READY!")
        print("="*50)
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Login to the app")
        print("3. Click '🤖 AI Chat' button")
        print("4. Start asking questions!")
        return True
        
    except requests.exceptions.Timeout:
        print("\n❌ ERROR: Request timeout. Check:")
        print("   - Internet connection")
        print("   - API key validity")
        print("   - Groq API status")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ ERROR: Connection failed: {e}")
        return False
    except json.JSONDecodeError:
        print(f"\n❌ ERROR: Invalid JSON response")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("🤖 Groq AI API - Configuration Test")
    print("="*50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    success = test_groq_api()
    sys.exit(0 if success else 1)
