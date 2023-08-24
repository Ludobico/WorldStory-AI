import threading
import queue
import asyncio
import uvicorn
import time
from typing import AsyncIterable, Awaitable, Callable, Union, Any
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
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
from websockets.exceptions import ConnectionClosedOK
from langchain.chains import ConversationChain
from callback import StreamingLLMCallbackHandler
from query_data import get_chain
from sceemas import ChatResponse
import logging
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    stream_handler = StreamingLLMCallbackHandler(websocket)
    qa_chain = get_chain(stream_handler)

    while True:
        try:
            # Receive and send back the client message
            user_msg = await websocket.receive_text()
            resp = ChatResponse(
                sender="human", message=user_msg, type="stream")
            await websocket.send_json(resp.dict())

            # Construct a response
            start_resp = ChatResponse(sender="bot", message="", type="start")
            await websocket.send_json(start_resp.dict())

            # Send the message to the chain and feed the response back to the client
            output = await qa_chain.acall(
                {
                    "input": user_msg,
                }
            )

            # Send the end-response back to the client
            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())
        except WebSocketDisconnect:
            logging.info("WebSocketDisconnect")
            # TODO try to reconnect with back-off
            break
        except ConnectionClosedOK:
            logging.info("ConnectionClosedOK")
            # TODO handle this?
            break
        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())


# @app.get('/stream_chat')
# def stream_chat():
#     template = """Question: {question}

#     Answer: Let's work this out in a step by step way to be sure we have the right answer."""

#     prompt = PromptTemplate(template=template, input_variables=["question"])

#     callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
#     llm = LlamaCpp(model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
#                    callbacks=[StreamingStdOutCallbackHandler()], verbose=True, streaming=True, max_tokens=25)
#     llm_chain = LLMChain(prompt=prompt, llm=llm,)

#     question = "What NFL team won the Super Bowl in the year Justin Bierber was born?"
#     response = llm_chain.run(question)
#     return StreamingResponse(response, media_type='text/event-stream')


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000)
