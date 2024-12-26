import asyncio
from typing import AsyncIterable

import os, sys, pdb
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if backend_root not in sys.path:
    sys.path.append(backend_root)

from langchain.callbacks import AsyncIteratorCallbackHandler
from Module.Prompt.CharacterSettingPrompt import character_generation_prompt
from Module.CharacterCheck import CharacterConfig
from Module.LLMChain.CustomLLM import CustomLLM_GPT

async def character_setting_gpt_stream() -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    llm = CustomLLM_GPT()
    user_preference = CharacterConfig.user_config_parser()

    # the base_template() function is deprecated -> use the character_generation_prompt() function instead base_template()
    # BaseTemplateResult = base_template()
    # prompt = PromptTemplate(template=BaseTemplateResult['template'], input_variables=["instruct", "name", "gender", "era"])

    prompt = character_generation_prompt()

    chain = prompt | llm
    name = user_preference['name']
    gender = user_preference['gender']
    era = user_preference['era']

    # method 1
    # async for chunk in chain.astream({"instruct" : question, "name" : name, "gender" : gender, "era" : era}):
    #     yield chunk

    response = chain.ainvoke({ "name" : name, "gender" : gender, "era" : era}, config={"callbacks" : [callback]})

    task = asyncio.create_task(response)
    
    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    except asyncio.CancelledError:
        raise
    finally:
        if hasattr(callback, 'done') and callback.done is not None:
            callback.done.set()

    await task


if __name__ == "__main__":
    generator = character_setting_gpt_stream()