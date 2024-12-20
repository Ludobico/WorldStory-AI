import os, sys
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if backend_root not in sys.path:
    sys.path.append(backend_root)
# -----------------------------------------
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import  ConversationBufferWindowMemory
from g4f.client import Client
from langchain_with_g4f import TestLLM
# -----------------------------------------

def init_llm_chain(question):
    system_template = """You are a chatbot having a conversation with a human.
    """

    human_template = """
{question}
"""
    memory_key = "chat_history"

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ]

    prompt = ChatPromptTemplate(
        messages=messages,
        input_variables=['question']
    )

    client = Client()
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role" : "user", "content" : question}],
        stream=True
    )

    llm = TestLLM()

    chain = prompt | llm

    result = chain.invoke({"question" : question})
    print(result)



if __name__ == "__main__":
    while True:
        input_char_prompt = input("say : ")
        init_llm_chain(input_char_prompt)
        