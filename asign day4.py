import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ATHROPIC_API_KEY"))


system_prompt = """You are an assistant to aa small pharmacy in Kisumu.
Answer questions on opening hours, whether a pharmacy stocks a specific drug,how long prescriptions take to process and
what type of documents are required for repeat prescriptions
The pharmacy opens at nine AM and closes at exactly 5 PM.
rules:
-make your conversation as brief possible.
-any uestion outside our scope say, "you can reach out to our pharmacy line 0741756028 for more information."
-use a kind tone
-make your convesation to be fluid like u ask what else would like to be offered ,or would you still need more information on the same.""" 


messages = []
print("Thank you for contacting Osongo Pharmacy in Kisumu, type 'exit' to end the coversation.")

while True:
    user_input = input("You: ")
    if user_input.lower()== 'exit':
        break

    messages.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 400,
        system = system_prompt,
        messages = messages
    )

    reply = response.content[0].text

    messages.append({"role": "user", "content": reply})

    print(f"assistant: {reply}")