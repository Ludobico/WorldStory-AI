from typing import Optional, List, Mapping, Any
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import g4f

from functools import partial
from langchain.callbacks.manager import AsyncCallbackManagerForLLMRun

class TestLLM(LLM):
  @property
  def _llm_type(self) -> str:
    return "custom"
  
  
  def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
    out = g4f.ChatCompletion.create(
      model=g4f.models.gpt_4,
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
      if run_manager:
          text_callback = partial(run_manager.on_llm_new_token)
      
      text = ""
      for token in g4f.ChatCompletion.create(model=g4f.models.gpt_4,messages=[{"role": "user", "content": prompt}], stream=True):
          if text_callback:
              await text_callback(token)
          text += token
          print(text)
      return text

llm = TestLLM()
prompt = PromptTemplate(
  input_variables=['product'],
  template="what is a good name for a company that makes {product}?",
)

chain = LLMChain(llm=llm, prompt=prompt)