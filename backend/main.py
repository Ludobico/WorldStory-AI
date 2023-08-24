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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracemalloc.start()


# template = """Question: {question}

# Answer: Let's work this out in a step by step way to be sure we have the right answer."""

# prompt = PromptTemplate(template=template, input_variables=["question"])


# Sender = Callable[[Union[str, bytes]], Awaitable[None]]


# async def send_message(message: str) -> AsyncIterable[str]:
#     # Callbacks support token-wise streaming
#     callback = AsyncIteratorCallbackHandler()
#     callback_manager = CallbackManager([callback])
#     # Verbose is required to pass to the callback manager

#     # Make sure the model path is correct for your system!
#     llm = LlamaCpp(
#         # replace with your model path
#         model_path="./Models/puddlejumper-13b.ggmlv3.Q2_K.bin",
#         callback_manager=callback_manager,
#         verbose=True,
#         streaming=True,
#         max_tokens=25,
#     )

#     llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True,)

#     question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

#     async def wrap_done(fn: Awaitable, event: asyncio.Event):
#         """Wrap an awaitable with an event to signal when it's done or an exception is raised."""
#         try:
#             await fn
#         except Exception as e:
#             # TODO: handle exception
#             print(f"Caught exception: {e}")
#         finally:
#             # Signal the aiter to stop.
#             event.set()

#     # Begin a task that runs in the background.
#     task = asyncio.create_task(wrap_done(
#         llm_chain.arun(question),
#         callback.done),
#     )

#     async for token in callback.aiter():
#         # Use server-sent-events to stream the response
#         yield f"data: {token}\n\n"

#     await task


# class StreamRequest(BaseModel):
#     """Request body for streaming."""
#     message: str


# @app.post("/stream")
# def stream(body: StreamRequest):
#     return StreamingResponse(send_message(body.message), media_type="text/event-stream")

class Message(BaseModel):
    content: str


async def send_message(content: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    template = """Question: {question}

    Answer: Let's work this out in a step by step way to be sure we have the right answer."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm = LlamaCpp(
        model_path="./Models/puddlejumper-13b.ggmlv3.Q2_K.bin",
        callbacks=[callback],
        verbose=True,
        streaming=True,
        max_tokens=25,
    )

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
