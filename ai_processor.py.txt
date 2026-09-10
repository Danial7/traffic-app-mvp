from groq import Groq

def generate_commute_briefing(groq_key, start, destination, base_eta, weather, hazards):
    """Leverages Groq LPU processing to generate an empathetic, mentally-preparing travel summary."""
    client = Groq(api_key=groq_key)
    
    prompt = f"""
    You are an intelligent local transit assistant for Karachi, Pakistan. 
    Analyze the raw voyage telemetry metrics below and synthesize a highly human-centric, conversational commute preview.
    The primary goal is to mentally prepare the commuter for exactly what they will encounter on their route.

    --- TRIP TELEMETRY ---
    - Route: From {start} to {destination}
    - Baseline Standard Duration: {base_eta} minutes
    - Weather Profile: {weather['temp']}°C, {weather['humidity']}% Humidity, Condition is {weather['condition']}
    - Route Hazard Alerts Pulled: {", ".join(hazards)}
    ---
    
    Provide the response in two short, punchy paragraphs:
    Paragraph 1: Summarize the traffic delays, hazards, and an adjusted mental ETA expectations.
    Paragraph 2: Mention the climate vibe (weather) and end with an encouraging local driving tip.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Could not generate briefing due to AI processing latency: {str(e)}"
