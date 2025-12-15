"""Quick test for Gemini API key"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found")

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say 'API test successful!' in 3 words")
    print(f"\n✅ API Test Successful!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"\n❌ API Test Failed!")
    print(f"Error: {e}")
