from typing import Optional, List, Any
from langchain.llms.base import LLM

from g4f.client import Client, AsyncClient
from g4f import Provider
from Module.Proxy.gpt3 import Completion

from functools import partial
from langchain.callbacks.manager import AsyncCallbackManagerForLLMRun

class CustomLLM_GPT(LLM):
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
      client = Client(provider=Provider.Airforce)
      # client = AsyncClient(provider=Provider.Copilot)
      response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role" : "user", "content" : prompt}],
        stream=True
    )
      if run_manager:
          text_callback = partial(run_manager.on_llm_new_token)
      
      text = ""
      for chunk in response:
            token = chunk.choices[0].delta.content
            if token is None:
              continue
            if text_callback:
                await text_callback(token)
            text += token
      return text

class CustomLLM_Llama(LLM):
  @property
  def _llm_type(self) -> str:
    return "custom"
  
  def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
    model = g4f.models.llama2_70b
    provider = g4f.Provider.DeepInfra
    out = g4f.ChatCompletion.create(
      model=model,
      provider=provider,
      messages=[{"role": "user", "content": prompt}],
    )

    if stop:
      stop_indexes = (out.find(s) for s in stop if s in out)
      min_stop = min(stop_indexes, default=-1)
      if min_stop > -1:
        out = out[:min_stop]
    return out
  
  async def _acall(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[AsyncCallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
    text_callback = None
    model = g4f.models.llama2_70b
    provider = g4f.Provider.DeepInfra
    if run_manager:
      text_callback = partial(run_manager.on_llm_new_token)
    
    text = ""
    for token in g4f.ChatCompletion.create(model=model,provider=provider,messages=[{"role": "user", "content": prompt}], stream=True):
      if text_callback:
        await text_callback(token)
      text += token
    return text
  
class CustomLLM_FreeGPT(LLM):
  @property
  def _llm_type(self):
    return "custom"
  
  def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
    completion_instance = Completion()
    out = completion_instance.create_non_stream(prompt)
    return out
  
  async def _acall(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[AsyncCallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
    text_callback = None
    if run_manager:
      text_callback = partial(run_manager.on_llm_new_token)
    
    text = ""
    completion_instance = Completion()
    for token in completion_instance.create(prompt=prompt):
      if text_callback:
        await text_callback(token)
      text += token
    return text