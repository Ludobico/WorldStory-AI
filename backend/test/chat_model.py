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

def init_llm_chain(question, chain):
    print(chain.run(question))

if __name__ == "__main__":
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
    while True:
        input_char_prompt = input("say : ")
        init_llm_chain(input_char_prompt, chain)
        