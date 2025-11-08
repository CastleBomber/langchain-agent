#!/usr/bin/env python3
"""
********************************************************
    Author: CBOMBS
    Date:   November 3rd, 2025

    Project: LangChain Agent
    Description: Conversational AI agent with persistent memory 

    Notes:
    source .venv/bin/activate
    python3 main.py
    memory.json

*********************************************************
"""
import os, json
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# --- Setup ---
load_dotenv()
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

if not token:
    raise ValueError("❌ Missing GITHUB_TOKEN in .env file!")

client = ChatCompletionsClient(endpoint=endpoint,credential=AzureKeyCredential(token))
memory_file = "memory.json"

# --- Load memory --- 
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        raw = json.load(f)
        memory = [SystemMessage(m["content"]) if m["role"]=="system" else UserMessage(m["content"]) for m in raw]
else:
    memory = [SystemMessage("You are a helpful AI assistant that remembers past chats.")]

print("🤖 Chat agent ready! Type 'exit' to quit.")

# --- Chat loop --- 
while True:
    user_input = input("You:")
    if user_input.lower() in ["exit", "quit"]:
        with open(memory_file, "w") as f:
            json.dump([{"role": m.role, "content": m.content} for m in memory], f, indent=2)
        print("💾 Memory saved. 👋 Goodbye!")
        break

    # Add user input to memory
    memory.append(UserMessage(user_input))

    # Generate AI response
    response = client.complete(
        messages=memory,
        temperature=0.7,
        model=model
    )

    # Extract and print AI's message
    ai_message = response.choices[0].message.content
    print("🤖:", ai_message)

    # Add AI's message to memory
    memory.append(SystemMessage(ai_message))
