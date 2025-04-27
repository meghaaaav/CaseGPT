import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit()

# Initialize the OpenAI client
client = OpenAI(api_key="api_key")

try:
    # Make a request to the OpenAI API
    completion = client.chat.completions.create(
        model="o3-mini",
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    print("API Response:")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
