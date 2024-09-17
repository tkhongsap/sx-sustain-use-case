import requests
import uuid
import sys
import json

# ANSI escape codes for blue bold text and reset
BLUE_BOLD = "\033[1;34m"
RESET = "\033[0m"

def print_highlight(message):
    print(f"\n{BLUE_BOLD}{message}{RESET}")

def get_available_models(base_url, headers):
    models_url = f"{base_url}/api/models"
    try:
        response = requests.get(models_url, headers=headers)
        response.raise_for_status()
        print_highlight(f"Raw models response: {response.text}")
        return response.json()
    except requests.RequestException as e:
        print_highlight(f"Error fetching available models: {e}")
        return None

# Step 1: Authenticate and get the token
auth_url = "http://103.213.207.241:9002/api/v1/auths/signin"
auth_payload = {
    "email": "api-service-test@thaibev.com",
    "password": "test"
}
try:
    auth_response = requests.post(auth_url, json=auth_payload)
    auth_response.raise_for_status()
    token = auth_response.json().get("token")
    if not token:
        raise ValueError("Token not found in response")
    print_highlight(f"Authentication successful, Token: {token}")
except requests.RequestException as e:
    print_highlight(f"Authentication request failed: {e}")
    sys.exit(1)
except ValueError as e:
    print_highlight(f"Authentication failed: {e}")
    sys.exit(1)

# Define headers after getting the token
headers = {
    "Authorization": f"Bearer {token}"
}

# Step 2: Fetch available models
base_url = "http://103.213.207.241:9002"
available_models = get_available_models(base_url, headers)
if available_models and 'data' in available_models:
    print_highlight("Available models:")
    for model in available_models['data']:
        print(json.dumps(model, indent=2))
        print("---")
else:
    print_highlight("Unable to fetch available models")

# Step 3: Fetch response from the model
model_url = "http://103.213.207.241:9002/api/chat/completions"

# Dynamically generate session ID using uuid4
session_id = str(uuid.uuid4())

# Adjust chat payload
chat_payload = {
    "stream": True,
    "model": "thaibev-sustainguide-",  # Custom model
    "stream_options": {
        "include_usage": True
    },
    "messages": [
        {
            "role": "user",
            "content": "How does ThaiBev’s sustainability strategy contribute to its long-term economic growth?"
        }
    ],
    "session_id": session_id,
    "chat_id": "",
    "id": str(uuid.uuid4())
}

try:
    chat_response = requests.post(model_url, json=chat_payload, headers=headers)
    chat_response.raise_for_status()
    print_highlight(f"Model Response: {chat_response.json()}")
except requests.RequestException as e:
    print_highlight(f"Error fetching model response: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print_highlight(f"Status code: {e.response.status_code}")
        print_highlight(f"Response text: {e.response.text}")
    print_highlight(f"Request payload: {json.dumps(chat_payload, indent=2)}")
    sys.exit(1)

