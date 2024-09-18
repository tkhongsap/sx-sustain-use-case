import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the API key and assistant ID
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = "asst_CsRUOSckEYjuORKgVduj9Yib"  # Replace with your assistant ID
base_url = "https://api.openai.com/v1"

# Define headers for the requests
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "OpenAI-Beta": "assistants=v2"
}

# Function to create a new thread with no initial messages
def create_thread():
    url = f"{base_url}/threads"
    payload = {
        "messages": []  # No initial messages
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        thread_data = response.json()
        return thread_data['id'], thread_data  # Returning the thread ID and all metadata
    else:
        return None, None

# Function to create a user message in the thread
def create_message(thread_id, user_message):
    url = f"{base_url}/threads/{thread_id}/messages"
    payload = {
        "role": "user",
        "content": user_message
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        message_data = response.json()
        return message_data['id'], message_data  # Returning the message ID and metadata
    else:
        return None, None

# Function to run the assistant and generate a response
def run_assistant(thread_id):
    url = f"{base_url}/threads/{thread_id}/runs"
    payload = {
        "assistant_id": assistant_id
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        run_data = response.json()

        # Remove the 'instructions' field
        if "instructions" in run_data:
            del run_data["instructions"]

        return run_data['id'], run_data  # Returning run ID and metadata without 'instructions'
    else:
        return None, None

# Function to wait on the assistant's run to complete
def wait_on_run(run_id, thread_id):
    run_url = f"{base_url}/threads/{thread_id}/runs/{run_id}"
    while True:
        response = requests.get(run_url, headers=headers)
        if response.status_code == 200:
            run_data = response.json()

            # Remove the 'instructions' field
            if "instructions" in run_data:
                del run_data["instructions"]

            if run_data.get('status') in ['completed']:
                return run_data  # Returning the full run metadata once complete
        time.sleep(1)  # Small delay to avoid overwhelming the API

# Function to fetch the latest message from the assistant
def fetch_thread_messages(thread_id):
    url = f"{base_url}/threads/{thread_id}/messages"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        messages_data = response.json()
        assistant_responses = []
        # Reverse the order to get the latest message first
        for message in reversed(messages_data.get('data', [])):
            if message.get('role') == 'assistant':
                content = message.get('content')
                if isinstance(content, list):
                    for item in content:
                        text = item.get('text', {}).get('value')
                        if text:
                            assistant_responses.append(text)
                elif isinstance(content, dict):
                    text = content.get('text', {}).get('value')
                    if text:
                        assistant_responses.append(text)
                elif isinstance(content, str):
                    assistant_responses.append(content)
                else:
                    assistant_responses.append(str(content))
        
        if assistant_responses:
            # Return the latest assistant response and all metadata
            return assistant_responses[-1], messages_data
        else:
            return None, messages_data
    else:
        return None, None

# Main function to handle the conversation and return responses in JSON
def chat_with_assistant():
    # Step 1: Create a thread with no initial messages
    thread_id, thread_metadata = create_thread()
    
    if not thread_id:
        print("Unable to start chat without a thread. Exiting.")
        return

    while True:
        try:
            # Step 2: Accept user input
            user_message = input("\n You: ").strip()
            
            if user_message.lower() in {"exit", "quit", "q"}:
                print("Exiting the chat. Goodbye!")
                break
            
            if not user_message:
                print("Please enter a message or type 'exit' to quit.\n")
                continue
            
            # Step 3: Create a message in the thread
            message_id, message_metadata = create_message(thread_id, user_message)
            
            if not message_id:
                print("Failed to create a message. Please try again.\n")
                continue
            
            # Step 4: Run the assistant to generate a response
            run_id, run_metadata = run_assistant(thread_id)
            if not run_id:
                print("Failed to run the assistant. Please try again.\n")
                continue
            
            # Step 5: Wait for the assistant's run to complete
            run_metadata = wait_on_run(run_id, thread_id)
            
            # Step 6: Fetch the assistant's response
            assistant_response, messages_metadata = fetch_thread_messages(thread_id)
            if assistant_response:
                result = {
                    "user_message": user_message,
                    "assistant_message": assistant_response,
                    "thread_metadata": thread_metadata,
                    "message_metadata": message_metadata,
                    "run_metadata": run_metadata,
                    "messages_metadata": messages_metadata
                }
                
                # Print the result as JSON
                print(json.dumps(result, indent=4))
                
            else:
                print("Assistant did not return a response.\n")
        
        except KeyboardInterrupt:
            print("\nChat interrupted. Exiting...")
            break
        except EOFError:
            print("\nEnd of input detected. Exiting...")
            break

# Run the chat program
if __name__ == "__main__":
    if not api_key:
        print("Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable or in the .env file.")
    elif not assistant_id:
        print("Error: Assistant ID not set. Please provide a valid assistant ID.")
    else:
        chat_with_assistant()
