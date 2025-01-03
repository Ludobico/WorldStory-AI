from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, AIMessagePromptTemplate
import os

def chat_base_prompt(char_prompt_path, memory_limit : int):
    cur_dir = os.getcwd()
    char_path = os.path.join(cur_dir, 'Characters', char_prompt_path, 'prompt.txt')
    with open(char_path, 'r', encoding='utf-8') as f:
        char_prompt = f.read()

    system_template = """
    [[[Always talk in {user_lang}]]]
    You are a Fictional Character that talks to a user through the ###character prompt### below.
    Ensure your responses are consistent with the world and setting of your story.Provide as much information as possible to make the character come to life within the story you have in mind
    ###character prompt###
    {char_prompt}
    ######
"""

    human_template = """
{user_name} : {message}
"""

    ai_template = """
{ai_name} : 
"""

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        MessagesPlaceholder(variable_name="chat_history", n_messages = memory_limit),
        HumanMessagePromptTemplate.from_template(human_template),
        AIMessagePromptTemplate.from_template(ai_template)
    ]
    prompt = ChatPromptTemplate(messages=messages, input_variables=['user_lang', 'user_name', 'message', 'ai_name'], partial_variables={"char_prompt" : char_prompt})
    return prompt