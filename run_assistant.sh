#!/bin/bash

API_KEY="your_api_key_here"
ASSISTANT_ID="asst_CsRUOSckEYjuORKgVduj9Yib"

# Debugging: Output to verify API key and Assistant ID
echo "Using API Key: $API_KEY"
echo "Using Assistant ID: $ASSISTANT_ID"

# Step 1: Create a thread
echo "Creating a thread..."
THREAD_RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/threads" \
-H "Authorization: Bearer $API_KEY" \
-H "OpenAI-Beta: assistants=v2" \
-H "Content-Type: application/json" \
-d '{"messages": []}')

# Debugging: Print the response from thread creation
echo "Thread Response: $THREAD_RESPONSE"

# Extract the thread ID from the response
THREAD_ID=$(echo $THREAD_RESPONSE | jq -r '.id')
echo "Thread ID: $THREAD_ID"

# Check if THREAD_ID is empty
if [[ -z "$THREAD_ID" || "$THREAD_ID" == "null" ]]; then
    echo "Error: Could not create thread. Exiting."
    exit 1
fi

# User input loop
while true; do
    # Step 2: Prompt the user for input
    read -p "You: " USER_MESSAGE

    # Exit the loop if the user types "exit", "quit", or "q"
    if [[ "$USER_MESSAGE" == "exit" || "$USER_MESSAGE" == "quit" || "$USER_MESSAGE" == "q" ]]; then
        echo "Exiting the chat. Goodbye!"
        break
    fi

    # Step 3: Send the user message to the assistant
    echo "Sending user message..."
    MESSAGE_RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/threads/$THREAD_ID/messages" \
    -H "Authorization: Bearer $API_KEY" \
    -H "OpenAI-Beta: assistants=v2" \
    -H "Content-Type: application/json" \
    -d "{\"role\": \"user\", \"content\": \"$USER_MESSAGE\"}")

    # Debugging: Print the response from sending the message
    echo "Message Response: $MESSAGE_RESPONSE"

    # Extract the message ID from the response
    MESSAGE_ID=$(echo $MESSAGE_RESPONSE | jq -r '.id')
    echo "Message ID: $MESSAGE_ID"

    # Step 4: Run the assistant
    echo "Running assistant..."
    RUN_RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/threads/$THREAD_ID/runs" \
    -H "Authorization: Bearer $API_KEY" \
    -H "OpenAI-Beta: assistants=v2" \
    -H "Content-Type: application/json" \
    -d "{\"assistant_id\": \"$ASSISTANT_ID\"}")

    # Remove 'instructions' field from the run response
    RUN_RESPONSE_CLEANED=$(echo "$RUN_RESPONSE" | jq 'del(.instructions)')

    # Debugging: Print the cleaned response (after removing instructions)
    echo "Run Response (after removing instructions): $RUN_RESPONSE_CLEANED"

    # Extract the run ID from the cleaned response
    RUN_ID=$(echo "$RUN_RESPONSE_CLEANED" | jq -r '.id')
    echo "Run ID: $RUN_ID"

    # Step 5: Fetch assistant response messages
    echo "Fetching assistant response..."
    sleep 2  # Add a small delay to ensure the response is generated

    MESSAGES_RESPONSE=$(curl -s -X GET "https://api.openai.com/v1/threads/$THREAD_ID/messages" \
    -H "Authorization: Bearer $API_KEY" \
    -H "OpenAI-Beta: assistants=v2" \
    -H "Content-Type: application/json")

    # Debugging: Print the messages response
    echo "Messages Response: $MESSAGES_RESPONSE"

    # Extract and print the assistant's message (last message)
    ASSISTANT_MESSAGE=$(echo "$MESSAGES_RESPONSE" | jq -r '.data[0].content[0].text.value')
    echo "Assistant: $ASSISTANT_MESSAGE"

done
