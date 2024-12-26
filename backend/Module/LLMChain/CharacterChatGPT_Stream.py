import configparser
import asyncio
from typing import AsyncIterable, Optional, List, Mapping, Any

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnablePassthrough
from Module.CharacterCheck import CharacterConfig
from Module.LLMChain.CustomLLM import CustomLLM_GPT, CustomLLM_Llama, CustomLLM_FreeGPT
from Module.Prompt.CharacterChatPrompt import chat_base_prompt

async def chat_with_OAI(content: str, char_prompt_path, memory) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    user_config = CharacterConfig.user_config_parser()
    user_name = user_config['user_name']
    user_lang = user_config['user_lang']
    memory_limit = user_config['memory']

    # prompt = PromptTemplate(
    #     template=chat_base_template_result['chat_template'], input_variables=["char_prompt", "message", "chat_history", "user_name", "ai_name", "user_lang"])

    prompt = chat_base_prompt(char_prompt_path)
    llm =  CustomLLM_GPT()
    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=int(memory_limit))
    chain = (
        RunnablePassthrough.assign(
            chat_history = lambda x : memory.chat_memory.messages
        )
        | prompt
        | llm
    )

    def invoke_with_memory(input_text):
        result = chain.astream({"user_lang" : user_lang, "user_name" : user_name, "message" : input_text, "ai_name" : char_prompt_path}, {'callbacks' : [callback]})
        memory.save_context({"input" : input_text}, {"output" : result.content})
  
    task = asyncio.create_task(
        invoke_with_memory(content)
    )
    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task
