import asyncio
import os
from typing import AsyncIterable
import g4f

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
from Module.CharacterSettingGPT_Stream import character_setting_gpt_stream

# Legacy
from Legacy.CharacterSettingOAI_Proxy_Stream import send_message_OAI

from Config.AxiosConfig import CTransformerConfig
from Config.LLMCheck import LLMCheck
from Module.MakeCharacter import MakeCharacter
from Module.CharacterCheck import Character_folder_check
from Module.CharacterChatOAI_Proxy_Stream import chat_with_OAI

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
    model_name : str

class OAI_Message(BaseModel):
    content : str


@app.post("/stream_chat")
async def stream_chat(ct_params: CT_parameters):
    # Generate a stream of messages based on the content of the input message
    generator = send_message(ct_params)
    # Return a streaming response with the generated messages
    return StreamingResponse(generator, media_type="text/event-stream")

# Legacy
# @app.post("/char_setting_OAI")
# async def stream_chat_OAI(message: OAI_Message):
#     generator = send_message_OAI(message.content)
#     return StreamingResponse(generator, media_type="text/event-stream")

# token별 스트리밍
# @app.post("/char_setting_OAI")
# async def char_setting_OAI(message : OAI_Message):
#     generator = character_setting_gpt_stream(message.content)
#     # return asyncio.run(generator)
#     return StreamingResponse(generator, media_type="text/event-stream")
    # return await StreamingResponse(character_setting_gpt_stream(message.content), media_type="text/event-stream")

@app.post("/char_setting_OAI")
def char_setting_OAI(message : OAI_Message):
    generator = character_setting_gpt_stream(message.content)
    return asyncio.run(generator)


@app.get("/generate_setting_config")
def generate_setting_config():
    config_instance = CTransformerConfig()
    top_k, top_q, temperature, last_n_tokens, max_new_tokens, gpu_layers = config_instance.get_config()
    return {"top_k": top_k, "top_q": top_q, "temperature": temperature, "last_n_tokens": last_n_tokens, "max_new_tokens": max_new_tokens, "gpu_layers": gpu_layers}

@app.get("/LLM_model_list")
def LLM_model_list():
    LC = LLMCheck()
    model_list = LC.json_read()
    return model_list

class MakeCharacterPrompt(BaseModel):
    name : str
    prompt : str

@app.post("/make_character")
def make_character(make_character : MakeCharacterPrompt):
    MC = MakeCharacter()
    MC.make_char_folder(name=make_character.name, prompt=make_character.prompt)

@app.get("/char_list_check")
def char_list_check():
    char_list = Character_folder_check()
    print(char_list)
    return char_list

class OAI_Message_chat(BaseModel):
    content : str
    prompt : str

@app.post("/character_chat_OAI")
def character_chat_OAI(message: OAI_Message_chat):
    generator = chat_with_OAI(content=message.content, char_prompt_path=message.prompt)
    return StreamingResponse(generator, media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app, loop='asyncio')
