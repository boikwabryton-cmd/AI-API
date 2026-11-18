import anthropic 
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

orders_database = {
    "ORD-102":"Out for delivery with rider (expected by 4pm)",
    "ORD-105":"Disputed from warehouse",
    "ORD-200":"Delivered succefully"
}

Mpesa_transaction_database = {
    "QRT89ZXYZ":{"status": "confirmed", "amount": 4500},
    "ABC123DEF":{"status": "confirmed", "amount": 1200},
    "XYZ999ZZZ":{"status": "pending", "amount": 3000}
}

def check_order_status(order_id):
    clean_id = order_id.strip().upper()
    if clean_id in orders_database:
        return f"order{clean_id} status: {orders_database[clean_id]}"
    return f"order {order_id} not found inour delivery records."

def verify_mpesa_payment(transaction_code):
    clean_code = transaction_code.strip().upper()
    if clean_code in Mpesa_transaction_database:
        payment_info = Mpesa_transaction_database[clean_code]
        return f"Mpesa code,{clean_code}: status is {payment_info["status"]}, amount received is KES {payment_info["amount"]}"
    return f"transaction code {clean_code} not found."

tools = [
    {
           "name":"check_order_status",
           "description": "check the delivery and shipping status of actual order using its order ID.",
           "input_schema": {
               "type":"object",
               "properties": {
                   "order_id":{
                       "type":"string",
                       "description":"the order ID, eg ORD-102"
                   }
               },
               "required":["order_id"]
               }
        },
    {
               "name":"verify_mpesa_payment",
               "description": "check on status and the amount of the mpesa statements using the transaction code .",
               "input_schema": {
                   "type":"object",
                   "properties": {
                       "transaction_code":{
                           "type":"string",
                           "description":"transaction_code eg xyz999zzz"
                       }
                   },
                   "required":["transaction_code"]
                   }
            }
            ]

system_prompt = "You are a helpfull retail custorm support for Osongo Super Stores, always be polite."

customer_question = input("Type your customer inquiry here..")

messages = [{"role": "user", "content": customer_question}]

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=400,
    tools=tools,
    system=system_prompt,
    messages=messages
)

if message.stop_reason == "tool_use":
    print("\n[AI Agent triggered tool use:]")
    messages.append({"role": "assistant","content":message.content})

    tool_results_content = []

    for content_block in message.content:
        if content_block.type == "tool_use":
            tool_name = content_block.name
            tool_arguments = content_block.input
            tool_call_id = content_block.id

            print(f"-> claude wants to run tool:{tool_name}")
            print(f"-> Extracted input from user text:{tool_arguments}")

            execution_result = ""

            if tool_name == "check_order_status":
                input_order_id = tool_arguments.get("order_id", "")
                execution_result = check_order_status(input_order_id)
            elif tool_name == "verify_mpesa_payment":
                input_mpesa_code = tool_arguments.get("transaction code", "")
                execution_result = verify_mpesa_payment(input_mpesa_code)
            else: execution_result = "unknown tool requested"

            print(f"-> database result: {execution_result}") 

            tool_results_content.append({"type": "tool_result", "tool_use_id": tool_call_id, "content": execution_result})

    messages.append({"role": "user", "content": tool_results_content})



    final_message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        system = system_prompt,
        tools=tools,
        messages=messages
    )

    print("AI Final response")
    print(final_message.content[0].text)

else:
    print("AI Final response")
    print(message.content[0].text)



















