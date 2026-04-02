import requests
import config
# 1. Use localhost for direct testing, or your ngrok URL for remote testing
URL = "http://127.0.0.1:5000/webhook" 

# 2. This mimics the JSON format Wassenger sends
test_payload = {
    "event": "message:in:new",
    "data": {
        "phone": config.TRINGTRING_NUMBER, # Match this with config.py
        "body": "Hello from the test script!"
    }
}

try:
    response = requests.post(URL, json=test_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Server Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")