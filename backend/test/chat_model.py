import os
import sys
sys.path.append(r"C:\Users\aqs45\OneDrive\바탕 화면\repo\WorldStory_AI\backend")
# -----------------------------------------
# local import
from Module.LLMChain.CustomLLM import CustomLLM_FreeGPT
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
# -----------------------------------------
def chat_base_template(char_prompt_path):
    cur_dir = os.getcwd()
    char_path = os.path.join(cur_dir, 'backend', 'Characters', char_prompt_path, 'prompt.txt')
    with open(char_path, 'r') as f:
        char_prompt = f.read()

    chat_template = """
    You are a Fictional Character that talks to a user through the ###character prompt### below.
    Ensure your responses are consistent with the world and setting of your story. Be creative and feel free to include any relevant details that will help the model generate a rich and unique character description. Provide as much information as possible to make the character come to life within the story you have in mind
    ###character prompt###
    {char_prompt}
    ######
    Ensure your responses are consistent with the world and setting of your story
    Let's think step by step.

    ###Previous conversation###
    {chat_history}
    ######

    {message}
    
"""

    return {"chat_template": chat_template, "char_prompt": char_prompt, "char_prompt_path": char_prompt_path}

def image_gen(message):
  llm = CustomLLM_FreeGPT()
  chat_base_template_result = chat_base_template('Lyra Silvermist')
  input_char_prompt = chat_base_template_result['char_prompt']
  question = message
  
  memory = ConversationBufferMemory(memory_key="chat_history")
  prompt = PromptTemplate(template=chat_base_template_result['chat_template'], input_variables=["char_prompt", "message", 'chat_history'])
  chain = LLMChain(llm=llm, prompt=prompt, memory=memory)


  result = chain.run(char_prompt=input_char_prompt, message=question)
  print(result)
if __name__ == "__main__":
  while True:
    input_char_prompt = input("say : ")
    image_gen(input_char_prompt)