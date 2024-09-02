import os
import requests

# Initialize global variables
conversation_retrieval_chain = None
chat_history = []
llm_hub = None
embeddings = None

import fitz  # PyMuPDF

def process_document(document_path):
    global text
    doc = fitz.open(document_path)
    text = ""
    for page in doc:
        text += page.get_text()

    text = text[:2000]



# Function to process a user prompt using Groq's API
def llm_llama(prompt):
    # Retrieve the Groq API key from environment variables
    groq_api_key = os.getenv('GROQ_API_KEY')

    # API endpoint for Groq
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Request payload
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": f"Context: {text}"
            },
            {
                "role": "user",
                "content": f"answer the question {prompt}"
            }
        ],
        "max_tokens": 800,
        "temperature": 0.1
    }

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(url, json=payload, headers=headers)

    # Check for a successful response
    if response.status_code == 200:
        result = response.json()
        choices = result.get('choices', [])
        if choices:
            return choices[0].get('message', {}).get('content', 'No content in response')
        else:
            return 'No choices in response'
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to process a user prompt
def process_prompt(prompt):
    global chat_history

    # Query the model
    answer = llm_llama(prompt)

    # Update the chat history
    chat_history.append((prompt, answer))

    # Return the model's response
    return answer


