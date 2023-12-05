import os
import sys
sys.path.append(r"C:\Users\aqs45\OneDrive\바탕 화면\repo\WorldStory_AI\backend")
# -----------------------------------------
# local import
from Module.LLMChain.CustomLLM import CustomLLM_FreeGPT
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# -----------------------------------------
def chat_base_template(char_prompt_path):
    cur_dir = os.getcwd()
    char_path = os.path.join(cur_dir, 'backend', 'Characters', char_prompt_path, 'prompt.txt')
    with open(char_path, 'r') as f:
        char_prompt = f.read()

    chat_template = """

    ###Previous conversation###
    {chat_history}
    ######

    {message}
    
    """

    return {"chat_template": chat_template, "char_prompt": char_prompt, "char_prompt_path": char_prompt_path}

def image_gen(question):
  llm = CustomLLM_FreeGPT()
  template = """
  당신은 사람과 대화하는 챗봇입니다.

  {history}
  Human: {human_input}
  Chatbot:
  
  """

  # prompt = PromptTemplate(
  #     input_variables=["history", "human_input"], template=template
  # )
  prompt = ChatPromptTemplate(messages = [
     SystemMessagePromptTemplate.from_template(template),
     MessagesPlaceholder(variable_name="history"),
     HumanMessagePromptTemplate.from_template("{human_input}")
  ])
  memory = ConversationBufferMemory()

  # chain = LLMChain(
  #     llm=llm, prompt=prompt, verbose=True, memory=memory
  # )
  chain = ConversationChain(llm=llm, prompt=prompt, memory=memory)


  result = chain.predict(question)
  print(result)
if __name__ == "__main__":
  while True:
    input_char_prompt = input("say : ")
    image_gen(input_char_prompt)