from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

# Create model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Create prompt
prompt = ChatPromptTemplate.from_template(
    "You are a helpful AI assistant. Answer clearly: {question}"
)

# Build chain
chain = LLMChain(llm=llm, prompt=prompt)

# Ask something
while True:
    user_input = input("Ask me something (or 'exit'): ")
    if user_input.lower() == "exit":
        break
    response = chain.run({"question": user_input})
    print("🤖:", response)
