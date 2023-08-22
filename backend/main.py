
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.callbacks.base import CallbackManager
from langchain.chat_models import ChatOpenAI
from fastapi.responses import StreamingResponse
import queue
import threading
import asyncio
import os
from typing import AsyncIterable, Awaitable, Callable, Union, Any, Dict, List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.callbacks.base import AsyncCallbackHandler
from pydantic import BaseModel
from uuid import UUID

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
# from langchain.callbacks.manager import CallbackManager, AsyncCallbackManagerForLLMRun
from langchain.callbacks.manager import CallbackManager
from langchain.schema import LLMResult, HumanMessage
from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler

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


@app.get('/')
async def hello_world():
    return {'message': "hello world"}


@app.on_event("startup")
async def startup():
    print("Server Startup!")


class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration:
            raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)


class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        print(token)
        self.gen.send(token)


def llm_thread(g):
    template = """
        Question : {question}

        Answer : Let's work this out in a step by step way to be sure we habe the right answer.
        """
    prompt = PromptTemplate(template=template, input_variables=["question"])
    question = "What NFL team won the Super Bowl in the year Justin Bierber was born?"
    try:
        llm = LlamaCpp(model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
                       callbacks=CallbackManager([ChainStreamHandler(g)]), verbose=True, streaming=True, max_tokens=25)
        llm_chain = LLMChain(prompt=prompt, llm=llm,)
        llm_chain.run(question)

    finally:
        g.close()


def chat():
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g)).start()
    return g


@app.get("/qs")
async def stream():
    return StreamingResponse(chat(), media_type='text/event-stream')


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000)
