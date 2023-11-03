import asyncio
from typing import AsyncIterable

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks import AsyncIteratorCallbackHandler
from Module.BaseTemplate import base_template, few_shot_base_template

from Module.CustomLLM import CustomLLM
async def async_generate(chain, question):
  resp = await chain.arun(question)
  return resp

async def character_setting_gpt_stream(content : str) -> AsyncIterable[str]:
  callback = AsyncIteratorCallbackHandler()
  llm = CustomLLM()
  BaseTemplateResult = base_template()
  FewShotTemplateResult = few_shot_base_template()

  prompt = PromptTemplate(template=BaseTemplateResult['template'] + FewShotTemplateResult, input_variables=["instruct"])

  chain = LLMChain(llm=llm, prompt=prompt, callbacks=[callback])
  question = BaseTemplateResult['instruct']

  # task = asyncio.create_task(chain.arun(question))
  # task = chain.arun(question)

  # try:
  #     async for token in callback.aiter():
  #         yield token
  # except Exception as e:
  #     print(f"Caught exception: {e}")
  # finally:
  #     callback.done.set()

  # await task

  tasks = [async_generate(chain, question)]
  await asyncio.gather(*tasks)