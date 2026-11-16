import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# --- 1. DATABASES / MOCK DATA ---
inventory = {
    "maize flour": 120,
    "wheat flour": 85,
    "rice": 200,
    "sugar": 0,
    "cooking oil": 45
}

prices = {
    "maize flour": 2800, 
    "wheat flour": 3200, 
    "rice": 4500
}


# --- 2. PYTHON FUNCTIONS (The Backend Work) ---
def get_stock_level(product_name):
    product = product_name.lower()
    if product in inventory:
        qty = inventory[product]
        if qty == 0:
            return f"{product_name} is currently out of stock."
        return f"{product_name}: {qty} bags in stock."
    return f"Product '{product_name}' not found in the system."


def get_price(product_name):
    p = product_name.lower()
    if p in prices:
        return f"{product_name}: KES {prices[p]:,} per bag"
    return f"Price not found for '{product_name}'"


# --- 3. TOOLS DEFINITION MENU (The Instructions for Claude) ---
tools = [
    {
        "name": "get_stock_level",
        "description": "Get the current stock quantity for a product at Kamau Stores",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product to check stock for"
                }
            },
            "required": ["product_name"]
        }
    },
    {
        "name": "get_price",
        "description": "Get the price per bag for a product at Kamau Stores",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product to check price for"
                }
            },
            "required": ["product_name"]
        }
    }
]


# --- 4. SENDING THE REQUEST TO CLAUDE ---
# Testing with a prompt that requires Claude to call BOTH tools (rice stock + rice price)
messages = [
    {"role": "user", "content": "How much does a bag of rice cost and how many do we have?"}
]

print("Sending request to Claude...")
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    tools=tools,
    messages=messages
)


# --- 5. HANDLING THE TOOL CALL(S) ---
if response.stop_reason == "tool_use":
    print("\n[AI Agent triggered tool use!]")
    
    # Loop through content blocks to handle multiple tool requests if Claude calls more than one
    for content_block in response.content:
        if content_block.type == "tool_use":
            fn_name = content_block.name
            fn_input = content_block.input
            product = fn_input.get("product_name")
            
            print(f"\nFunction called: {fn_name}({fn_input})")
            
            # Execute the correct local Python function based on what Claude requested
            if fn_name == "get_stock_level":
                result = get_stock_level(product)
            elif fn_name == "get_price":
                result = get_price(product)
            else:
                result = "Unknown function call."
                
            print(f"Result: {result}")