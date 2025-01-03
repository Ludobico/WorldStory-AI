import configparser
import asyncio
from typing import AsyncIterable, Optional, List, Mapping, Any, Dict
import os

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from Module.CharacterCheck import CharacterConfig
from Module.LLMChain.CustomLLM import CustomLLM_GPT, CustomLLM_Llama, CustomLLM_FreeGPT
from Module.Prompt.CharacterChatPrompt import chat_base_prompt
from Module.History.HistoryUtils import HistoryMessageExtractor, InMemoryHistory

async def chat_with_OAI(content: str, char_prompt_path : str, store : Dict) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    user_config = CharacterConfig.user_config_parser()
    user_name = user_config['user_name']
    user_lang = user_config['user_lang']
    memory_limit = user_config['memory']


    prompt = chat_base_prompt(char_prompt_path, memory_limit)
    llm =  CustomLLM_GPT()

    def get_by_session_id(session_id : str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryHistory()
        return store[session_id]

    chain = prompt | llm
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_by_session_id,
        input_messages_key="message",
        history_messages_key="chat_history"
    )

    def history_chain_call(content : str, session_id : str, store : Dict):
        response = chain_with_history.ainvoke({"user_lang" : user_lang, "user_name" : user_name, "message" : content, "ai_name" : char_prompt_path}, config={"configurable" : {"session_id" : session_id}})
        return response

    response = history_chain_call(content=content, session_id=char_prompt_path, store=store)
  
    task = asyncio.create_task(response)

    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task
