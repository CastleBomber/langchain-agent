#!/usr/bin/env python
'''
********************************************************
    Author: CBombs
    Date:   October 28th, 2025

    Project: LangChain Agent

    Environment: Github Marketplace Openai playground
        
*********************************************************
'''
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv()  # Load .env file

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage(""),
        UserMessage("What is the meaning of life?"),
    ],
    temperature=1,
    top_p=1,
    model=model
)

print(response.choices[0].message.content)


