#!/usr/bin/env python3
"""
********************************************************
    Author: CBombs
    Date:   October 30th, 2025

    Project: LangChain Agent
    Description: Conversational AI agent with basic memory (GitHub Models)
    Details: Keeps each turn of the conversation in RAM; when the script ends, the memory is gone
             Stores both user inputs and AI outputs (UserMessage + SystemMessage)
    Environment: Github Marketplace's Openai playground using Azure SDK for Python

    Commands to run:
    source .venv/bin/activate
    python3 main.py

*********************************************************
"""
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables from .env file
load_dotenv()

# Set up models and credentials
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

if not token:
    raise ValueError("❌ Missing GITHUB_TOKEN in .env file!")

# Client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Memory (conversation history)
memory = [SystemMessage("You are a helpful AI assistant that remembers the conversation.")]

print("🤖 Chat agent ready! Type 'exit' to quit.")
while True:
    user_input = input("You:")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Add user input to memory
    memory.append(UserMessage(user_input))

    # Generate AI response
    response = client.complete(
        messages=memory,
        temperature=0.7,
        top_p=1,
        model=model,
    )

    # Extract and print AI message
    ai_message = response.choices[0].message.content
    print("🤖:", ai_message)

    # Add AI message to memory
    memory.append(SystemMessage(ai_message))
