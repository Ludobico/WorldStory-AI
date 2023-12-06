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

class Foo:
    def __init__(self):
        self.llm_chain = self.init_llm_chain()

    def init_llm_chain(self):
        llm = CustomLLM_FreeGPT()
        template = """You are a chatbot having a conversation with a human.

        {chat_history}
        Human: {human_input}
        Chatbot:"""

        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"], template=template
        )
        memory = ConversationBufferMemory(memory_key="chat_history")
        chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)
        return chain

    def run_chat(self, question):
        print(self.llm_chain.run(question))

if __name__ == "__main__":
    while True:
        cls = Foo()
        input_char_prompt = input("say : ")
        cls.run_chat(input_char_prompt)