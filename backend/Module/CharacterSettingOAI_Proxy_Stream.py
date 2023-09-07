import configparser
import asyncio
from typing import AsyncIterable, Optional, List, Mapping, Any

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain import PromptTemplate, LLMChain
from Module.BaseTemplate import base_template
from langchain.schema import HumanMessage

import g4f
from g4f import Provider, models
from langchain.llms.base import LLM
from Module.G4FLLM import G4FLLM


async def send_message_OAI(content: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    BaseTemplateResult = base_template()

    prompt = PromptTemplate(
        template=BaseTemplateResult['template'], input_variables=["instruct"])

    llm: LLM = G4FLLM(model=models.gpt_35_turbo, provider=Provider.DeepAi, callbacks=[callback], verbose=True)
    model = LLMChain(prompt=prompt, llm=llm, verbose=True)

    question = BaseTemplateResult['instruct']
    

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
