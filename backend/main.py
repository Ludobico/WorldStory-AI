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
from langchain.callbacks.manager import CallbackManager, AsyncCallbackManagerForLLMRun
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


template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template=template, input_variables=["question"])


Sender = Callable[[Union[str, bytes]], Awaitable[None]]


class AsyncStreamCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming, inheritance from AsyncCallbackHandler."""

    def __init__(self, send: Sender):
        super().__init__()
        self.send = send

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Rewrite on_llm_new_token to send token to client."""
        await self.send(f"data: {token}\n\n")


async def send_message(message: str) -> AsyncIterable[str]:
    # Callbacks support token-wise streaming
    callback = AsyncIteratorCallbackHandler()
    callback_manager = CallbackManager([callback])
    # Verbose is required to pass to the callback manager

    # Make sure the model path is correct for your system!
    llm = LlamaCpp(
        # replace with your model path
        model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
        callback_manager=callback_manager,
        verbose=True,
        streaming=True,
        max_tokens=25
    )

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        """Wrap an awaitable with an event to signal when it's done or an exception is raised."""
        try:
            await fn
        except Exception as e:
            print(f"Caught exception: {e}")
        finally:
            # Signal the aiter to stop.
            event.set()

    # Begin a task that runs in the background.
    task = asyncio.create_task(wrap_done(
        llm_chain.arun(question),
        callback.done),
    )

    async for token in callback.aiter():
        # Use server-sent-events to stream the response
        yield f"data: {token}\n\n"

    await task


class StreamRequest(BaseModel):
    """Request body for streaming."""
    message: str


@app.post("/stream")
def stream(body: StreamRequest):
    return StreamingResponse(send_message(body.message), media_type="text/event-stream")


@app.post("/stream_chat")
def stream_chat():
    template = """
    Question: {instruct}

    Answer: Let's work this out in a step by step way to be sure we have the right answer.
    """

    llm = LlamaCpp(model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
                   verbose=True, temperature=0.95, max_tokens=512, n_ctx=4096, streaming=True)
    prompt = PromptTemplate(template=template, input_variables=["instruct"])
    model = LLMChain(prompt=prompt, llm=llm)

    # for chunk in llm._stream(prompt=template):
    #     print(chunk.text)
    # response = model.run(
    #     "What NFL team won the Super Bowl in the year Justin Bieber was born?")

    for chunk in llm._stream(prompt=prompt):
        print(chunk.text)

# Need chunk update


@app.post("/langdocs_stream")
async def test():
    token_list = []

    class MyCustomSyncHandler(AsyncCallbackManagerForLLMRun):
        def on_llm_new_token(self, token: str, **kwargs) -> None:
            # 실제 chunk 단위로 답변
            print(
                f"Sync handler being called in a `thread_pool_executor`: token: {token}")
            return JSONResponse(content={"token": token})

    class MyCustomAsyncHandler(AsyncCallbackHandler):

        async def on_llm_start(
                self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
            print("zzzz....")
            await asyncio.sleep(0.3)

        async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
            print("token end")
            await asyncio.sleep(0.3)

    callback_manager = AsyncCallbackManagerForLLMRun([MyCustomSyncHandler])

    template = """
    Question: {instruct}

    Answer: Let's work this out in a step by step way to be sure we have the right answer.
    """

    llm = LlamaCpp(model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
                   verbose=True, temperature=0.95, max_tokens=25, n_ctx=4096, streaming=True, callback_manager=callback_manager)
    prompt = PromptTemplate(template=template, input_variables=["instruct"])
    model = LLMChain(prompt=prompt, llm=llm)
    question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

    await model.arun(question)

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000)
