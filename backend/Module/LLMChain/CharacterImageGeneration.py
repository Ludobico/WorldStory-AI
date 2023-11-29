from Module.LLMChain.CustomLLM import CustomLLM_GPT, CustomLLM_Llama, CustomLLM_FreeGPT
from Module.Proxy.gpt3 import Completion
from Module.Template.BaseTemplate import image_generate_prompt
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class CharacterImageGeneration:
  def image_gen(character_prompt):
    # llm = CustomLLM_GPT()
    llm = Completion()
    image_generate_prompt_result = image_generate_prompt()
    result = llm.create(prompt=image_generate_prompt_result, stream=False)
    # prompt = PromptTemplate(template=image_generate_prompt_result, input_variables=["description"])
    # chain = LLMChain(llm=llm, prompt=prompt)
    # question = character_prompt
    # result = chain.run(question)
    print(result)
    return result