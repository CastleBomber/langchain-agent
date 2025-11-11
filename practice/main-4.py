#!/usr/bin/env python3
"""
********************************************************
    Author: CBOMBS
    Date:   November 6th, 2025

    Project: LangChain Agent
    Description: Conversational AI agent with crash-safe persistent memory 

    Notes:
    source .venv/bin/activate
    python3 main.py
    memory.json

*********************************************************
"""
import os, json, signal, sys
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

def save_memory():
    with open(memory_file, "w") as f:
        json.dump([{"role": m.role, "content": m.content} for m in memory], f, indent=2)

# --- Load memory --- 
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        raw = json.load(f)
        memory = [SystemMessage(m["content"]) if m["role"]=="system" else UserMessage(m["content"]) for m in raw]
else:
    memory = [SystemMessage("You are a helpful AI assistant that remembers past chats.")]

# --- Handle abrupt exits ---
def handle_exit(sig=None, frame=None):
    save_memory()
    print("\n💾 Memory saved. 👋 Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit)  # kill command

print("🤖 Chat agent ready! Type 'exit' to quit.")

# --- Chat loop --- 
while True:
    user_input = input("You:")
    if user_input.lower() in ["exit", "quit"]:
        handle_exit()

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

    # Auto save memory after every turn
    save_memory()
