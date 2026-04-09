import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def list_my_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("ERROR: GEMINI_API_KEY is not set in .env")
        return

    genai.configure(api_key=api_key)
    
    print(f"Checking models for API key: {api_key[:5]}...{api_key[-5:]}")
    try:
        models = genai.list_models()
        print("\nAvailable models that support 'generateContent':")
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"FAILED to list models: {e}")

if __name__ == "__main__":
    list_my_models()
