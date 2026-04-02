import requests
import config
def send_whatsapp_message(phone,message):
    headers= {
        "Token":config.WASSENGER_KEY,
        "Content-Type":"application/json"
    }
    payload = {
        "phone" : phone,
        "message" : message
    }
    try:
        response=requests.post(config.WASSENGER_URL,json=payload,headers=headers,timeout=10)
        print(f"DEBUG Wassenger Response: {response.text}")
        return response.status_code
    except Exception:
        return None