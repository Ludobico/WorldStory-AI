import configparser
import asyncio
from typing import AsyncIterable, Optional, List, Mapping, Any

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from Module.Template.BaseTemplate import chat_base_template
from langchain.schema import HumanMessage

import g4f
from g4f import Provider, models
from langchain.llms.base import LLM
from Module.LLMChain.CustomLLM import CustomLLM_GPT, CustomLLM_Llama


async def chat_with_OAI(content: str, char_prompt_path) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    chat_base_template_result = chat_base_template(char_prompt_path)
    prompt = PromptTemplate(
        template=chat_base_template_result['chat_template'], input_variables=["char_prompt", "message"])

    llm =  CustomLLM_Llama()
    model = LLMChain(prompt=prompt, llm=llm)

    char_prompt = chat_base_template_result['char_prompt']
    question = content
  
    task = asyncio.create_task(
        model.arun(char_prompt = char_prompt, message = question, callbacks=[callback])
    )
    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task
