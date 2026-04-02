from openai import OpenAI
import config
from persona import CUSTOMERS

client = OpenAI(
    base_url=config.OPENROUTER_URL,
    api_key=config.OPENROUTER_KEY,
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Sunteck Customer Simulator"
    }
)
_sessions = {}

def ask_ai(phone, agent_message, persona_key="anxious_first_timer"):
    if phone not in _sessions:
        _sessions[phone] = {
            "persona": persona_key,
            "history": [] 
        }
    
    session = _sessions[phone]
    
    persona_data = CUSTOMERS.get(session["persona"], CUSTOMERS["anxious_first_timer"])
    system_instruction = persona_data["prompt"]

    # 2. Add the NEW agent message to the history
    session["history"].append({"role": "user", "content": agent_message})

    # 3. Build the full message payload (System Prompt + History)
    # This ensures the AI remembers what it said previously.
    messages_to_send = [
        {"role": "system", "content": system_instruction}
    ] + session["history"]

    try:
        # 4. Call OpenRouter
        response = client.chat.completions.create(
            model=config.AI_MODEL,
            messages=messages_to_send,
            temperature=0.8,
            max_tokens=200
        )

        reply = response.choices[0].message.content

        # 5. Save the AI's reply to history so it stays consistent
        session["history"].append({"role": "assistant", "content": reply})

        return reply

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return "I'm not sure how to respond to that right now."
def reset_ai_memory(phone):
    """Clears the chat history for a specific phone number"""
    if phone in _sessions:
        del _sessions[phone]
        return True
    return False