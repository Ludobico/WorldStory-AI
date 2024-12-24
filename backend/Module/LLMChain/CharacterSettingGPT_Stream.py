import asyncio
from typing import AsyncIterable

import os, sys, pdb
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if backend_root not in sys.path:
    sys.path.append(backend_root)

from langchain.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.callbacks import AsyncIteratorCallbackHandler
from Module.Template.BaseTemplate import base_template, few_shot_base_template
from Module.Template.FewShotPromptForCharSetting import character_setting_examples
from Module.CharacterCheck import CharacterConfig
from Module.LLMChain.CustomLLM import CustomLLM_GPT, CustomLLM_Llama, CustomLLM_FreeGPT

async def character_setting_gpt_stream() -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    llm = CustomLLM_GPT()
    BaseTemplateResult = base_template()
    user_preference = CharacterConfig.user_config_parser()

    # prompt = PromptTemplate(template=BaseTemplateResult['template'] + FewShotTemplateResult, input_variables=["instruct"])
    prompt = PromptTemplate(template=BaseTemplateResult['template'], input_variables=["instruct", "name", "gender", "era"])

    chain = prompt | llm
    question = BaseTemplateResult['instruct']
    name = user_preference['name']
    gender = user_preference['gender']
    era = user_preference['era']

    # method 1
    # async for chunk in chain.astream({"instruct" : question, "name" : name, "gender" : gender, "era" : era}):
    #     yield chunk

    response = chain.ainvoke({"instruct" : question, "name" : name, "gender" : gender, "era" : era}, config={"callbacks" : [callback]})

    task = asyncio.create_task(response)
    
    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task


if __name__ == "__main__":
    generator = character_setting_gpt_stream()