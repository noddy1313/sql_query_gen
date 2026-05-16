import streamlit as st
import requests

# Set the model you're using (you must have already pulled this with: ollama pull gemma)
OLLAMA_MODEL = "gemma"

# Add your API key here
API_KEY = "your_api_key_here"

# Function to generate SQL using the Ollama model
def generate_sql_with_ollama(prompt):
    try:
        # Send a POST request to the Ollama API with the prompt and model details
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            headers={
                "Authorization": f"Bearer {API_KEY}"
            }
        )
        # Check if the response is successful
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            # Return error details if the response is not successful
            return f"❌ Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        # Handle the case where the Ollama server is not running
        return "⚠️ Ollama server not running. Please open a terminal and run: `ollama run gemma`"
