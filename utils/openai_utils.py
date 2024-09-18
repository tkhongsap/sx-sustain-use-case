import openai
import time
import os
from openai import OpenAI

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


# Initialize OpenAI client using the API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")


print(f"API Key: {api_key[:10]}...") # Print first 10 characters for verification
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add your API key.")

client = OpenAI(api_key=api_key) # You can also configure `openai.api_key` directly if needed

# Manage thread_id manually
thread_id = None

# Function: wait on the run to complete
def wait_on_run(run, thread_id):
    while run.status == 'queued' or run.status == 'in_progress':
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        time.sleep(1)  # Small delay to avoid overwhelming the API

# Function: display the response
def display_thread_messages(messages):
    message_texts = []
    for thread_message in messages.data[::-1]:
        message_texts.append(thread_message.content[0].text.value)
    return "\n\n".join(message_texts)

# Function: generate response
def generate_response(user_message, assistant_id):
    global thread_id

    if thread_id is None:
        # Initiate a new thread if one does not exist
        thread = client.beta.threads.create()
        thread_id = thread.id
        print(f"New thread created: {thread.id}")
    else:
        print(f"Using existing thread: {thread_id}")

    try:
        # Add user_message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role='user',
            content=user_message)

        # Run the assistant on the thread
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id)

        print("Generating answer...")  # Print instead of using st.spinner
        wait_on_run(run, thread_id)

        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order='asc',
            after=message.id)

        return display_thread_messages(messages)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "Error generating response. Please try again."
