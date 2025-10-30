#!/usr/bin/env python3
"""
********************************************************
    Author: CBombs
    Date:   October 28th, 2025

    Project: LangChain Agent

    Environment: Github Marketplace Openai playground using Azure SDK for Python

*********************************************************
"""
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load .env file
load_dotenv()

# Set up models + credentials
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

if not token:
    raise ValueError("❌ Missing GITHUB_TOKEN in .env file!")

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Simple math tool
def do_math(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Error: invalid math expression."

# Initialize conversation memory
messages = [SystemMessage("You are a helpful assistant. Keep answers concise.")]

print("🤖 Chat agent ready! Type 'exit' to quit or 'calc <expression>' for math.\n")

while True:
    user_input = input("You:")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    # Tool use: math
    if user_input.startswith("calc "):
        result = do_math(user_input[5:])
        print("🧮:", result)
        continue

    # Add user message to context
    messages.append(UserMessage(user_input))

    # Generate AI reply
    response = client.complete(
        messages=messages,
        temperature=0.7,
        top_p=1,
        model=model,
    )

    reply = response.choices[0].message.content.strip()
    print("🤖:", reply)

    # Add reply to memory so it remembers context
    messages.append(SystemMessage(reply))

