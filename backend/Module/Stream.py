import asyncio
import os
from typing import AsyncIterable
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain import PromptTemplate, LLMChain
from langchain.llms import CTransformers
from BaseTemplate import base_template


async def send_message(content: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    BaseTemplateResult = base_template()

    prompt = PromptTemplate(
        template=BaseTemplateResult['template'], input_variables=["instruct"])

    # llm = LlamaCpp(
    #     model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
    #     callbacks=[callback],
    #     verbose=True,
    #     streaming=True,
    #     max_tokens=25,
    # )
    testconfig = {"max_new_tokens": 25}
    llm = CTransformers(
        model="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin", model_type="llama", callbacks=[callback], verbose=True, config=testconfig)

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
