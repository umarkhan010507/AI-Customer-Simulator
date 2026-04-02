"""
import os
from datetime import datetime
DIR_NAME='logs'
os.makedirs(DIR_NAME,exist_ok=True)
def log_conversation(phone,sender_role,message):
    date=datetime.now().strftime("%Y-%m-%d")
    filename=f"{DIR_NAME}/{phone}_{date}.txt"
    timestamp=datetime.now().strftime("%H:%M:%S")
    with open(filename,"a",encoding="utf-8") as f:
        f.write(f"[{timestamp}] {sender_role} : {message}\n")
        """ 
# logger.py
import os
from datetime import datetime

def log_conversation(phone, sender_type, message, persona_name="Unknown"):
    # Create logs directory if it doesn't exist
    log_dir = os.path.join("logs", str(phone))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Log file named by date
    file_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.txt")
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    with open(file_path, "a", encoding="utf-8") as f:
        # Added [Persona] tag to the log entry
        f.write(f"[{timestamp}] [{persona_name}] {sender_type}: {message}\n")