import os
import sys
sys.path.append(r"C:\Users\aqs45\OneDrive\바탕 화면\repo\WorldStory_AI\backend")
# -----------------------------------------
# local import
from Module.LLMChain.CustomLLM import CustomLLM_FreeGPT
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
# -----------------------------------------

def init_llm_chain(question, memory):
    llm = CustomLLM_FreeGPT()
    template = """You are a chatbot having a conversation with a human.

    {history}
    Human: {input}
    Chatbot:"""

    prompt = PromptTemplate(
        input_variables=["history", "input"], template=template
    )
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)
    print(chain.run(question))
    print(id(chain))

if __name__ == "__main__":
    # memory = ConversationBufferMemory(memory_key="history", input_key="input")
    memory = ConversationBufferWindowMemory(memory_key="history", input_key="input", k=3)
    while True:
        input_char_prompt = input("say : ")
        init_llm_chain(input_char_prompt, memory)
        