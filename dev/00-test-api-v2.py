import requests
import uuid
import sys
import json
import readline  # For better input handling
from rich import print as rprint
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

# ANSI escape codes for text colors
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"

console = Console()

def print_highlight(message, color=BLUE):
    print(f"\n{color}{message}{RESET}")

def get_available_models(base_url, headers):
    models_url = f"{base_url}/api/models"
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Fetching available models...", total=None)
            response = requests.get(models_url, headers=headers)
            progress.update(task, completed=100)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print_highlight(f"Error fetching available models: {e}", RED)
        return None

def select_model(available_models):
    rprint("[bold]Available models:[/bold]")
    for i, model in enumerate(available_models['data'], 1):
        rprint(f"{i}. {model['id']}")
    
    choice = Prompt.ask("Select a model", choices=[str(i) for i in range(1, len(available_models['data'])+1)])
    return available_models['data'][int(choice)-1]['id']

def process_stream_response(response):
    full_response = ""
    for line in response.iter_lines():
        if line:
            try:
                json_response = json.loads(line.decode('utf-8').split('data: ')[1])
                if 'choices' in json_response and json_response['choices']:
                    content = json_response['choices'][0].get('delta', {}).get('content', '')
                    if content:
                        print(f"{BLUE}{content}{RESET}", end='', flush=True)
                        full_response += content
                elif 'usage' in json_response:
                    print(f"\n\n{GREEN}Usage: {json_response['usage']}{RESET}")
            except json.JSONDecodeError:
                if b'data: [DONE]' in line:
                    continue  # Skip the [DONE] message
                print(f"{RED}Error decoding JSON: {line}{RESET}")
    print()  # Add a newline at the end
    return full_response

def interactive_chat(base_url, headers, model):
    print_highlight(f"Starting interactive chat with model: {model}")
    print_highlight("Type 'exit' to end the conversation.")
    
    session_id = str(uuid.uuid4())
    messages = []

    while True:
        user_input = Prompt.ask(f"\n{GREEN}You{RESET}")
        if user_input.lower() == 'exit':
            break

        messages.append({"role": "user", "content": user_input})
        chat_payload = {
            "stream": True,
            "model": model,
            "stream_options": {"include_usage": True},
            "messages": messages,
            "session_id": session_id,
            "chat_id": "",
            "id": str(uuid.uuid4())
        }

        print(f"\n{BLUE}AI{RESET}: ", end='', flush=True)
        try:
            with requests.post(f"{base_url}/api/chat/completions", json=chat_payload, headers=headers, stream=True) as chat_response:
                chat_response.raise_for_status()
                ai_response = process_stream_response(chat_response)
                messages.append({"role": "assistant", "content": ai_response})
        except requests.RequestException as e:
            print_highlight(f"Error: {e}", RED)

def main():
    # Step 1: Authenticate and get the token
    base_url = "http://103.213.207.241:9002"
    auth_url = f"{base_url}/api/v1/auths/signin"
    auth_payload = {
        "email": "api-service-test@thaibev.com",
        "password": "test"
    }
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Authenticating...", total=None)
            auth_response = requests.post(auth_url, json=auth_payload)
            progress.update(task, completed=100)
        auth_response.raise_for_status()
        token = auth_response.json().get("token")
        if not token:
            raise ValueError("Token not found in response")
        print_highlight("Authentication successful", GREEN)
    except requests.RequestException as e:
        print_highlight(f"Authentication request failed: {e}", RED)
        sys.exit(1)
    except ValueError as e:
        print_highlight(f"Authentication failed: {e}", RED)
        sys.exit(1)

    # Define headers after getting the token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Step 2: Fetch available models
    available_models = get_available_models(base_url, headers)
    if not available_models:
        print_highlight("Unable to fetch available models. Exiting.", RED)
        sys.exit(1)

    # Step 3: Select model
    model_name = select_model(available_models)

    # Step 4: Start interactive chat
    interactive_chat(base_url, headers, model_name)

if __name__ == "__main__":
    main()