from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load GEMINI_API_KEY from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )

# Create the Gemini client
client = genai.Client(api_key=api_key)

# Ask the user for a question
question = input("Ask me anything: ")

# Send the question to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=question,
    config=types.GenerateContentConfig(
        max_output_tokens=1024
    )
)
# Print Gemini's answer
print("Answer:", response.text)

# Print token usage
usage = response.usage_metadata

print(
    f"Tokens used: {usage.prompt_token_count} in, "
    f"{usage.candidates_token_count} out"
)