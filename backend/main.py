import uvicorn
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


from fastapi.middleware.cors import CORSMiddleware
import tracemalloc
import uvicorn
# LLM Module using langchain
# ----------------------------
from Module.LLMChain.CharacterSettingCT_Stream import send_message
from Module.LLMChain.CharacterSettingGPT_Stream import character_setting_gpt_stream, character_setting_gpt4_stream
from Module.LLMChain.CharacterChatGPT_Stream import chat_with_OAI
# ----------------------------


# Legacy
# ----------------------------
from Legacy.CharacterSettingOAI_Proxy_Stream import send_message_OAI
# ----------------------------

# History
# ----------------------------
from Module.History.ChatHistory import ChatHistory
# ----------------------------

from Config.AxiosConfig import CTransformerConfig
from Config.LLMCheck import LLMCheck

from Module.MakeCharacter import MakeCharacter
from Module.CharacterCheck import CharacterConfig
from pathlib import Path


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
    generator = send_message(ct_params)
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
    return StreamingResponse(generator, media_type="text/event-stream")

@app.post("/char_setting_OAI_beta")
def char_setting_OAI_beta(message : OAI_Message):
    generator = character_setting_gpt4_stream(message.content)
    return StreamingResponse(generator, media_type="text/event-stream")


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
    name : Optional[str] = None
    prompt : Optional[str] = None

@app.post("/make_character")
def make_character(make_character : MakeCharacterPrompt):
    MC = MakeCharacter()
    MC.make_char_folder(name=make_character.name, prompt=make_character.prompt)

@app.get("/char_list_check")
def char_list_check():
    char_list = CharacterConfig.Character_folder_check()
    return char_list

class OAI_Message_chat(BaseModel):
    content : str
    prompt : str

@app.post("/character_chat_OAI")
def character_chat_OAI(message: OAI_Message_chat):
    generator = chat_with_OAI(content=message.content, char_prompt_path=message.prompt)
    return StreamingResponse(generator, media_type="text/event-stream")

@app.post("/character_image_check")
def character_image_check(character_name_check : MakeCharacterPrompt):
    chracter_image = CharacterConfig.Character_image_parser(char_name=character_name_check.name)
    return chracter_image

@app.get("/user_name_check")
def user_name_check():
    user_name = CharacterConfig.user_config_parser()
    return user_name

@app.get("/user_image_check")
def user_image_check():
    user_image = CharacterConfig.user_image_parser()
    return user_image

class Chat_history_base(BaseModel):
    user_chat : Optional[str] = None
    user_name : Optional[str] = None
    AI_chat : Optional[str] = None
    AI_name : Optional[str] = None

@app.post("/chat_history_save")
def chat_history_save(chat_history : Chat_history_base):
    ChatHistory.save_history_to_json(user_chat=chat_history.user_chat, user_name=chat_history.user_name, AI_chat=chat_history.AI_chat, AI_name=chat_history.AI_name)

@app.post("/chat_history_import")
def chat_history_import(chat_hitory : Chat_history_base):
    json_history = ChatHistory.import_history_from_json(AI_name=chat_hitory.AI_name)
    chracter_image = CharacterConfig.Character_image_parser(char_name=chat_hitory.AI_name)
    user_image = CharacterConfig.user_image_parser()
    return {"chat_log": jsonable_encoder(json_history), "char_image": chracter_image, "user_image": user_image}


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app, loop='asyncio')
