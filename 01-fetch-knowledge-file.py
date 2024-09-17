import requests
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

# Step 2: Fetch available models and print only the 'knowledge' part from 'meta'
base_url = "http://103.213.207.241:9002"
available_models = get_available_models(base_url, headers)
if available_models and 'data' in available_models:
    print_highlight("Knowledge section from the models:")
    for model in available_models['data']:
        meta = model.get('info', {}).get('meta', {})
        knowledge = meta.get('knowledge', [])
        if knowledge:
            print_highlight(f"Knowledge section for model '{model.get('id')}':")
            print(json.dumps(knowledge, indent=2))  # Print the knowledge section
            print("---")
        else:
            print_highlight(f"No knowledge section found for model: {model.get('id')}")
else:
    print_highlight("Unable to fetch available models")
