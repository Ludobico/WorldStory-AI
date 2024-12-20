from typing import Optional, List, Mapping, Any, AsyncIterable
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate

from functools import partial
from langchain.callbacks.manager import AsyncCallbackManagerForLLMRun
from langchain.callbacks import AsyncIteratorCallbackHandler
from g4f.client import Client
import asyncio

class TestLLM(LLM):
  @property
  def _llm_type(self) -> str:
    return "custom"
  
  
  def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
    client = Client()

    out = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role" : "user", "content" : prompt}],
    )
    string_out = out.choices[0].message.content
    return string_out
  
  async def _acall(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[AsyncCallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
      text_callback = None
      client = Client()
      response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role" : "user", "content" : prompt}],
        stream=True
    )
      if run_manager:
          text_callback = partial(run_manager.on_llm_new_token)
      
      text = ""
      for token in response:
          if text_callback:
              await text_callback(token)
          text += token
      return text



if __name__ == "__main__":
  pass
