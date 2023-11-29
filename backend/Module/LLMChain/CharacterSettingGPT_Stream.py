import asyncio
from typing import AsyncIterable

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks import AsyncIteratorCallbackHandler
from Module.Template.BaseTemplate import base_template, few_shot_base_template

from Module.LLMChain.CustomLLM_GPT import CustomLLM_GPT

async def character_setting_gpt_stream(content : str) -> AsyncIterable[str]:
  callback = AsyncIteratorCallbackHandler()
  llm = CustomLLM_GPT()
  BaseTemplateResult = base_template()
  FewShotTemplateResult = few_shot_base_template()

  prompt = PromptTemplate(template=BaseTemplateResult['template'] + FewShotTemplateResult, input_variables=["instruct"])
#   prompt = PromptTemplate(template=BaseTemplateResult['template'], input_variables=["instruct"])

  chain = LLMChain(llm=llm, prompt=prompt)
  question = BaseTemplateResult['instruct']

  task = asyncio.create_task(chain.arun(question, callbacks=[callback]))
  
  try:
      async for token in callback.aiter():
          yield token
  except Exception as e:
      print(f"Caught exception: {e}")
  finally:
      callback.done.set()

  await task