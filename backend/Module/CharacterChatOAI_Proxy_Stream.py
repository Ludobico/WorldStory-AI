import configparser
import asyncio
from typing import AsyncIterable, Optional, List, Mapping, Any

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# from langchain import PromptTemplate, LLMChain
from Module.BaseTemplate import chat_base_template
from langchain.schema import HumanMessage

import g4f
from g4f import Provider, models
from langchain.llms.base import LLM
from Module.G4FLLM import G4FLLM


async def chat_with_OAI(content: str, char_prompt_path) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    chat_base_template_result = chat_base_template(char_prompt_path)
    prompt = PromptTemplate(
        template=chat_base_template_result['chat_template'], input_variables=["char_prompt", "message"])

    llm: LLM = G4FLLM(model=models.gpt_35_turbo_16k, provider=Provider.GptGo, callbacks=[callback], verbose=True)
    model = LLMChain(prompt=prompt, llm=llm, verbose=True)

    char_prompt = chat_base_template_result['char_prompt']
    question = content
  
    task = asyncio.create_task(
        model.arun(char_prompt = char_prompt, message = question)
    )
    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task
