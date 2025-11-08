#!/usr/bin/env python3
"""
********************************************************
    Project: Frames AI
    Version: 0.1
    Author: CBOMBS
    Date:   November 7th, 2025
    Description: An AI animation assitant that helps build storyboards 
                 and generate motion poses from user commands
    
    source .venv/bin/activate
    python3 main.py
    memory.json
*********************************************************
"""
import os, json, re, sys, signal
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# --- Pose Engine Stub ---
class PoseEngine:
    """Detects pose or motion commands and handles them."""

    def __init__(self):
        # You can expand this with more motion commands later
        self.pose_keywords = {
            "pixelate": "Generate pixelated character",
            "walk": "Generate walking pose sequence",
            "run": "Generate running animation",
            "sit": "Generate seated pose",
            "jump": "Generate jumping pose",
            "turn": "Generate turning motion"
        }

    def detect_pose(self, text: str):
        """Return the matched pose keyword if found."""
        for keyword in self.pose_keywords:
            if re.search(rf"\b{keyword}\b", text.lower()):
                return keyword
        return None

    def handle_pose(self, keyword: str):
        """Stub action: what happens when we detect a pose."""
        action = self.pose_keywords[keyword]
        # Eventually: call image generation here
        return f"🩰 PoseEngine: {action} (simulation only for now)."

# --- Setup ---
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

if not api_key:
    raise ValueError("❌ Missing GITHUB_TOKEN in .env file!")

model = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=api_key
)

memory_file = "memory.json"
pose_engine = PoseEngine()

def save_memory():
    with open(memory_file, "w") as f:
        json.dump([{"role": m.type, "content": m.content} for m in memory], f, indent=2)

# --- Load memory --- 
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        raw = json.load(f)
        memory = [SystemMessage(m["content"]) if m["role"] == "system"
                  else HumanMessage(m["content"]) if m["role"] == "user"
                  else AIMessage(m["content"]) for m in raw]
else:
    memory = [SystemMessage(
        "You are Frames AI — a creative assistant that helps build "
        "storyboards and generate motion poses from user commands."
    )]

print("🎞️ Frames AI ready! Type 'exit' to quit.\n")
    
# --- Handle abrupt exits ---
def handle_exit(sig=None, frame=None):
    save_memory()
    print("\n💾 Memory saved. 👋 Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit)  # kill command

print("🤖 Chat agent ready! Type 'exit' to quit.")

# --- Main chat loop --- 
while True:
    user_input = input("🎙️ You: ")
    if user_input.lower() in ["exit", "quit"]:
        handle_exit()

    # Add user input to memory
    memory.append(HumanMessage(user_input))

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
