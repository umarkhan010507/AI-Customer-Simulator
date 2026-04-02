from ai_client import ask_ai


if __name__ == "__main__":
    # Fake a message from the TringTring agent
    test_agent_msg = "Hello! I am the AI assistant for XYZ store. How can I help you?"
    
    # Fake a persona
    test_persona = "You are a happy customer and want to share a good feedback of the product received."
    
    # Run the function
    reply = ask_ai(test_agent_msg, test_persona)
    print(f"User says: {reply}")