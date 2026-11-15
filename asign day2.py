import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt = """You are a matatu secretary sacco assistant .In Thika Nairobi.

Your rules:
- Only answer questions related to the current membership fees of the sacco, the next meeting and 
the depature time of the matatus in the morning.
- The morning depature for the matatus is 0700HRS.
- All the transactions are in KSH not USD.
- The current membership fees is  KSH 10,000.
- The next meeting is scheduled in KICC 5TH floor confrence hall, on 12TH December.
- Any questions outside your scope, say:"please contact office line: 0741756028 for more inquiry."
- Always use a kind tone and finish with: "Thank you for contacting us."
"""

user_question = input("what type of services would you like to be offered today at our sacco?")

message = client.messages.create(
    model = "claude-haiku-4-5",
    max_tokens = 400,
    system = system_prompt,
    messages = [{"role": "user","content": user_question}])

print(message.content[0].text)