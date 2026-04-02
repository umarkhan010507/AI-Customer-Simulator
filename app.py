"""
from flask import Flask,request,jsonify
from client import send_whatsapp_message
from ai_client import ask_ai,reset_ai_memory
import config
import random
from persona import CUSTOMERS
from logger import log_conversation
app=Flask(__name__)
persona_history={}
MAX_TURNS=10
@app.route('/webhook',methods=['POST'],strict_slashes=False)
def handle_incoming_webhook():
    payload=request.json
    if not payload:
        return jsonify({"status":"error","message":"No payload"}),400
    incoming_text=None
    sender_phone=None
    
    if payload.get("event")== "message:in:new":
        data=payload.get("data",{})
        sender_phone=data.get("fromNumber")
        incoming_text=data.get("body")
        print(f"DEBUG: Message from {sender_phone} to my bot {data.get('phone')}")
    if incoming_text and str(sender_phone) == str(config.TRINGTRING_NUMBER):
        if incoming_text.strip().upper()=="RESET":
            if sender_phone in persona_history:
                del persona_history[sender_phone]
                reset_ai_memory(sender_phone)
                return jsonify({"status":"reset"}),200
            if sender_phone not in persona_history:
                assigned_key=random.choice(list(CUSTOMERS.keys()))
                persona_history[sender_phone]={"persona":assigned_key,
                                               "turn":0,
                                               "history":[]}
                print(f"New session started for {sender_phone} with persona {assigned_key}")
        current_key=persona_history[sender_phone]
        key=current_key["persona"]
        current_persona_name=CUSTOMERS[key]["name"]
        if current_key["turn"] >=MAX_TURNS:
                print(f"Max turns reached.Ending session")
                del persona_history[sender_phone]
                reset_ai_memory(sender_phone)
                return jsonify({"status":"session_ended"}),200
        current_key["turn"] +=1
        current_key['history'].append({"role":"user","content":incoming_text})
        log_conversation(sender_phone,"TRING TRING AGENT",incoming_text,persona_name=current_persona_name)
        customer_reply=ask_ai(sender_phone,current_key['history'],persona_key=key)
        current_key['history'].append({"role":"assistant","content":customer_reply})
        log_conversation(sender_phone,"CUSTOMER",customer_reply,persona_name=current_persona_name)
        
        send_whatsapp_message(sender_phone,customer_reply)
        return jsonify({"status":"succcess"}),200
    return jsonify({"status":"ignored"}),200
if __name__ == '__main__':
    app.run(port=5000)  
"""
from flask import Flask, request, jsonify
from client import send_whatsapp_message
from ai_client import ask_ai, reset_ai_memory
import config
import random
import time
from persona import CUSTOMERS
from logger import log_conversation

app = Flask(__name__)
persona_history = {}
MAX_TURNS = 10

@app.route('/webhook', methods=['POST'], strict_slashes=False)
def handle_incoming_webhook():
    payload = request.json
    if not payload:
        return jsonify({"status": "error", "message": "No payload"}), 400
    
    if payload.get("event") == "message:in:new":
        data = payload.get("data", {})
        # FIX 1: Force string conversion to ensure memory matches every time
        sender_phone = str(data.get("fromNumber")) 
        incoming_text = data.get("body", "")

        # Only process if it's from your designated testing number
        if incoming_text and sender_phone == str(config.TRINGTRING_NUMBER):
            text_norm = incoming_text.strip().upper()
            
            # --- COMMAND: RESET ---
            if text_norm == "RESET":
                if sender_phone in persona_history:
                    del persona_history[sender_phone]
                    reset_ai_memory(sender_phone)
                print(f"🔄 SYSTEM: Resetting session for {sender_phone}")
                return jsonify({"status": "reset"}), 200

            # --- COMMAND: CONFIG (Fix: Must return immediately) ---
            if text_norm.startswith("CONFIG"):
                parts = incoming_text.split()
                specs = {"lang": "English", "tone": "Calm", "style": "Long"}
                for p in parts:
                    if ":" in p:
                        k, v = p.split(":")
                        specs[k.lower()] = v
                
                persona_history[sender_phone] = {
                    "persona": "manual_spec",
                    "turn": 0,
                    "active": True,
                    "specs": specs
                }
                # Confirmation message so you know it worked
                send_whatsapp_message(sender_phone, f"✅ Configured: {specs['tone']} | {specs['lang']} | {specs['style']}")
                return jsonify({"status": "configured"}), 200

            # Start session if new
            if sender_phone not in persona_history:
                assigned_key = random.choice(list(CUSTOMERS.keys()))
                persona_history[sender_phone] = {
                    "persona": assigned_key,
                    "turn": 0,
                    "active": True,
                    "specs": {
                        "lang": CUSTOMERS[assigned_key].get("languages", "English"),
                        "tone": CUSTOMERS[assigned_key].get("tone", "Neutral"),
                        "style": CUSTOMERS[assigned_key].get("style", "Long")
                    }
                }

            current_key = persona_history[sender_phone]
            
            if not current_key["active"]:
                return jsonify({"status": "inactive"}), 200

            # --- STOP LOGIC: Detect Escalation Phrases from Sunteck Bot ---
            # Based on Sunteck Protocol Step 2 
            stop_phrases = ["escalating this now", "pause the conversation", "team member will take this forward"]
            if any(phrase in incoming_text.lower() for phrase in stop_phrases) or current_key["turn"] >= MAX_TURNS:
                current_key["active"] = False
                print(f"🏁 SESSION ENDED: Turn {current_key['turn']}")
                return jsonify({"status": "ended"}), 200

            current_key["turn"] += 1
            specs = current_key["specs"]
            
            # FIX 2: Harsh System Instruction to stop acting like Sonia (the Agent)
            buyer_instruction = (
                f"STRICT ROLEPLAY: You are a BUYER, NOT an agent. "
                f"The person texting you is a bot named Sonia[cite: 886]. "
                f"You are interested in Sunteck One World but you are the customer. "
                f"Tone: {specs['tone']}. Language: {specs['lang']}."
            )
            
            log_conversation(sender_phone, "TRING TRING AGENT", incoming_text)
            
            # Request AI reply as the CUSTOMER
            customer_reply = ask_ai(sender_phone, f"{buyer_instruction}\n\nAgent Message: {incoming_text}", persona_key=current_key["persona"])
            
            log_conversation(sender_phone, "CUSTOMER", customer_reply)

            # --- STYLE: Burst Logic ---
            if specs["style"].lower() == "burst":
                # Sunteck rule: never burst on amenities[cite: 1519], but as a CUSTOMER we can!
                for part in customer_reply.split('.'):
                    if part.strip():
                        send_whatsapp_message(sender_phone, part.strip())
                        time.sleep(1.5)
            else:
                send_whatsapp_message(sender_phone, customer_reply)

            return jsonify({"status": "success"}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    app.run(port=5000)