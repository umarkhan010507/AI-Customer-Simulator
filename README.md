AI Simulator: Customer Persona Tester
This project is a specialized Testing Suite designed to stress-test conversational AI models. It simulates various customer personas—ranging from "Arrogant Investors" to "Confused First-Time Buyers"—to evaluate how well a target AI handles different languages, tones, and messaging styles.

🚀 Core Features
Dynamic Persona Switching: Randomly assigns a unique customer profile to each new WhatsApp session.

Manual Configuration: Override defaults in real-time by texting CONFIG commands (e.g., lang:Hinglish tone:Arrogant style:Burst).

Behavioral Simulation:

Tone Control: Test for "Abusive/Irate" handling or "Polite" persistence.

Burst Messaging: Simulates "impatient" users by splitting responses into multiple rapid-fire WhatsApp messages.

Language Testing: Support for English, Hindi, Marathi, and Hinglish.

Auto-Termination: Automatically kills the session after 10 turns or if the target bot "escalates" to a human.

Session Management: Clear memory and start fresh at any time using the RESET command.
