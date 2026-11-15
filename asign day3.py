import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt = """You are a wholesaler assistant to a wholesaler distributor in Nakuru town.
Extract data from a messy language of sheng, swahili, and english from his customers, and return raw json object, do not wrap.
The fields to be extracted include the following:
-items(a list of dictionary which each dictionary has a product name and the quntity or null.)
-Location(string or null.)
-payment atatus(paid, unknown and payment on delivery otherwise null.)
-M-PESA code(string of 10 character code if mentioned otherwise null.)
-Urgency(true or false depending on the tone of the client.)
CRITICAL RULES:
- Return ONLY valid JSON. 
- Do NOT wrap the JSON in ```json or ``` markdown blocks.
- Do NOT include any intro or outro text.
"""

test_inquiries = ["Niaje boss, ni Kamau wa Eldoret. Nitumie mabale 5 za unga ya Pembe na cartons 3 za mafuta ya Elianto haraka sana, nishalipa via M-Pesa QK89L2M4P1.",
"Mambo! I need 4 crates of soda, 12 packets of milk, and 2 bales of tissue delivered to Kisumu by tomorrow morning. Lipa mdogo mdogo or COD?"]

for i, inquiry in enumerate(test_inquiries, start=1):
    print(f"\n---inquiry # {i}: '{inquiry}'--")

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        system=system_prompt,
        messages =[{"role": "user", "content": inquiry}]
    )
    raw_data = message.content[0].text
    

    extracted_data = json.loads(raw_data)

    for key, value in extracted_data.items():
        print(f" {key}:, {value}")






