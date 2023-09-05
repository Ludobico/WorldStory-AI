import asyncio
import os
from typing import AsyncIterable

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from pydantic import BaseModel

from langchain import PromptTemplate, LLMChain
from fastapi.middleware.cors import CORSMiddleware
import tracemalloc
import uvicorn
from langchain.llms import CTransformers
from Module.CharacterSettingCT_Stream import send_message
from Module.CharacterSettingOA_Stream import send_message_open_ai

from Config.AxiosConfig import CTransformerConfig

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


class CT_parameters(BaseModel):
    content: str
    top_k: int
    top_p: float
    temperature: float
    last_n_tokens: int
    max_new_tokens: int
    gpu_layers: int


@app.post("/stream_chat")
async def stream_chat(ct_params: CT_parameters):
    # Generate a stream of messages based on the content of the input message
    generator = send_message(ct_params)
    # Return a streaming response with the generated messages
    return StreamingResponse(generator, media_type="text/event-stream")


# @app.post("/stream_chat_open_ai")
# async def stream_chat(message: Message):
#     # Generate a stream of messages based on the content of the input message
#     generator = send_message_open_ai(message.content)
#     # Return a streaming response with the generated messages
#     return StreamingResponse(generator, media_type="text/event-stream")


@app.get("/generate_setting_config")
def generate_setting_config():
    config_instance = CTransformerConfig()
    top_k, top_q, temperature, last_n_tokens, max_new_tokens, gpu_layers = config_instance.get_config()
    return {"top_k": top_k, "top_q": top_q, "temperature": temperature, "last_n_tokens": last_n_tokens, "max_new_tokens": max_new_tokens, "gpu_layers": gpu_layers}


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
