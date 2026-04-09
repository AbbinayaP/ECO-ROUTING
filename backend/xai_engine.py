import os
from google import genai
from typing import Dict, Any

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("WARNING: GEMINI_API_KEY environment variable is missing or using placeholder.")
        return None
    
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        print(f"Failed to initialize Gemini Client: {e}")
        return None

def generate_explanation(route_context: Dict[str, Any], user_message: str) -> str:
    """
    Generates an explanation using the new Google GenAI SDK.
    """
    client = get_client()
    if not client:
        return "I'm sorry, my AI engine is offline because the GEMINI_API_KEY is not configured or the client failed to start."

    # Construct the prompt context
    system_prompt = f"""
    You are an eco-routing explainable AI assistant. Your goal is to help users understand why certain routes are better and explain the trade-offs between speed and emissions.
    
    Current Route Context:
    - Origin: {route_context.get('origin', 'Unknown')}
    - Destination: {route_context.get('destination', 'Unknown')}
    - Mode: {route_context.get('mode', 'Unknown')}
    - Algorithm Used: {route_context.get('algorithm', 'Unknown')}
    
    Route Options:
    """
    
    options = route_context.get('options', [])
    if not options:
        system_prompt += "\n- No specific route options calculated yet. The user might be asking a general question."
    
    for opt in options:
        opt_mode = opt.get('mode', 'Unknown')
        dist = opt.get('distance_km', 0)
        time = opt.get('duration_min', 0)
        co2 = opt.get('co2_kg', 0)
        score = opt.get('eco_score', 0)
        system_prompt += f"\n- {opt_mode.upper()}: Distance: {dist:.2f} km, Time: {time:.2f} min, CO2 Emissions: {co2:.2f} kg, EcoScore: {score}/100"

    system_prompt += f"""
    
    The user is asking a question about these specific route metrics or why a certain decision was made. 
    Keep your answer concise (2-4 short paragraphs), insightful, and direct. Explain the trade-offs clearly.
    
    User Question: {user_message}
    """

    # Model attempts
    models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
    
    last_error = ""
    for model_name in models_to_try:
        try:
            print(f"Generating XAI explanation with {model_name} using new SDK...")
            response = client.models.generate_content(
                model=model_name,
                contents=system_prompt
            )
            print(f"Success with {model_name}!")
            return response.text
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            last_error = str(e)
            continue

    return f"I encountered an error trying to generate an explanation with the new SDK: {last_error}"
