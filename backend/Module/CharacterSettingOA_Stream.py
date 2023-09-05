import configparser
import asyncio
from typing import AsyncIterable

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain import PromptTemplate, LLMChain
from Module.BaseTemplate import base_template


async def send_message_open_ai(content: str) -> AsyncIterable[str]:
    configapi = configparser.ConfigParser()
    configapi.read('config.ini', encoding='UTF-8')
    callback = AsyncIteratorCallbackHandler()
    BaseTemplateResult = base_template()

    prompt = PromptTemplate(
        template=BaseTemplateResult['template'], input_variables=["instruct"])

    llm = ChatOpenAI(streaming=True, verbose=True, callbacks=[
                     callback], openai_api_key=configapi['DEFAULT']['apikey'])

    model = LLMChain(prompt=prompt, llm=llm, verbose=True)

    question = BaseTemplateResult['instruct']

    task = asyncio.create_task(
        model.agenerate(question)
    )

    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task
