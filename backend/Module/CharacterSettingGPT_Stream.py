import asyncio
from typing import AsyncIterable

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from Module.BaseTemplate import base_template, few_shot_base_template

from CustomLLM import CustomLLM
async def async_generate(chain, question):
  resp = await chain.arun(question)
  return resp

async def character_setting_gpt_stream(content : str):
  llm = CustomLLM()
  BaseTemplateResult = base_template()
  FewShotTemplateResult = few_shot_base_template()

  prompt = PromptTemplate(template=BaseTemplateResult['template'] + FewShotTemplateResult, input_variables=["instruct"])

  chain = LLMChain(llm=llm, prompt=prompt)
  question = BaseTemplateResult['instruct']
  tasks = [async_generate(chain, question)]
  await asyncio.gather(*tasks)
