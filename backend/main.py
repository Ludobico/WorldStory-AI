import asyncio
import os
from typing import AsyncIterable, Awaitable, Callable, Union, Any

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.callbacks.base import AsyncCallbackHandler
from pydantic import BaseModel

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from fastapi.middleware.cors import CORSMiddleware
import tracemalloc
import uvicorn
from langchain.llms import CTransformers
# Load env variables from .env file
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracemalloc.start()


class Message(BaseModel):
    content: str


async def send_message(content: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    template = """Question: {question}

    Answer: Let's work this out in a step by step way to be sure we have the right answer."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    # llm = LlamaCpp(
    #     model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
    #     callbacks=[callback],
    #     verbose=True,
    #     streaming=True,
    #     max_tokens=25,
    # )
    llm = CTransformers(
        model="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin", model_type="llama", callbacks=[callback], verbose=True)

    model = LLMChain(prompt=prompt, llm=llm, verbose=True)

    question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

    task = asyncio.create_task(
        model.arun(question)
    )

    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task


@app.post("/stream_chat")
async def stream_chat(message: Message):
    generator = send_message(message.content)
    return StreamingResponse(generator, media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
