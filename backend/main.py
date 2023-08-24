import threading
import queue
import asyncio
import uvicorn
import time
from typing import AsyncIterable, Awaitable, Callable, Union, Any
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from pydantic import BaseModel
import tracemalloc
import uvicorn
from dotenv import load_dotenv
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Load env variables from .env file
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracemalloc.start()


@app.get('/')
async def hello_world():
    return {'message': "hello world"}


@app.get('/stream_chat')
def stream_chat():
    template = """Question: {question}

    Answer: Let's work this out in a step by step way to be sure we have the right answer."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
                   callbacks=[StreamingStdOutCallbackHandler()], verbose=True, streaming=True, max_tokens=25)
    llm_chain = LLMChain(prompt=prompt, llm=llm,)

    question = "What NFL team won the Super Bowl in the year Justin Bierber was born?"
    response = llm_chain.run(question)
    return StreamingResponse(response, media_type='text/event-stream')


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000)
