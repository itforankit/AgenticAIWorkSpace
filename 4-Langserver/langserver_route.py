from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# 1. create prompt template
system_template = "You are a language translator expert. Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser = StrOutputParser()

## Create chain
chain=prompt_template|model|parser

## App definition
app = FastAPI(title="Langchain API", description="API for Langchain", version="0.1")

from langserve import add_routes
add_routes(app, chain, path="/chain")

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)