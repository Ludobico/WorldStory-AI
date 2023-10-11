import g4f
from G4FLLM import G4FLLM
from typing import AsyncIterable, Optional, List, Mapping, Any

from langchain.callbacks import AsyncIteratorCallbackHandler
# from langchain import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage

from g4f import Provider, models
from langchain.llms.base import LLM

import asyncio
async def test():
    callback = AsyncIteratorCallbackHandler()

    template = """Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm: LLM = G4FLLM(model=models.gpt_35_turbo,  provider=Provider.GptGo, verbose=True)
    model = LLMChain(prompt=prompt, llm=llm, callbacks=[callback],verbose=True)

    question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

    
    task = asyncio.create_task(
        model.arun(question)
    )
    try:
        async for token in callback.aiter():
            print(token)
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task

if __name__ == "__main__":
  test()