import os
def base_template():
    template = """
    {instruct}
    Name:
    Gender:
    Age:
    Personality:
    Background:
    Appearance:
    Ensure your responses are consistent with the world and setting of your story. Be creative and feel free to include any relevant details that will help the model generate a rich and unique character description. Provide as much information as possible to make the character come to life within the story you have in mind.
    create a character for a story set in various settings such as historical, futuristic, fantasy,modern or science fiction.
    Let's think step by step.
    Feel free to elaborate on each point to create a comprehensive portrayal of your character.

    writer :
"""

    instruct = "You are a talented writer creating a character for a story. Provide detailed information for the following aspects of your character:"
    return {"template": template, "instruct": instruct}

def few_shot_base_template():
    few_shot_template = """
### example
Name: Nora Blackwood

Gender: Female

Age: 28

Personality: Nora is an intelligent, ambitious, and determined individual. She is confident in her abilities and has a strong sense of justice. She can be direct and assertive when needed, but also has a compassionate side that she reserves for those she cares about.

Background: Nora grew up in a working-class family in a small town on the outskirts of a bustling city. Despite limited resources, she excelled academically and was determined to create a better life for herself. She worked hard to earn a scholarship and attended a prestigious university, where she studied journalism.

Appearance: Nora is of average height and has short, dark hair that she usually wears in a ponytail. She has a sharp, angular face with prominent cheekbones, and piercing blue eyes. She often wears simple, elegant clothing that complements her features.

Setting: Modern

Additional details: Nora is a journalist who works for a major newspaper. She is passionate about uncovering the truth and exposing corruption, even if it means putting herself in harm's way. She is also an advocate for social justice and often uses her platform to shed light on important issues affecting vulnerable communities. Despite her tough exterior, she struggles with anxiety and often seeks solace in yoga and meditation. Nora's ultimate goal is to become a renowned investigative journalist and make a lasting impact on the world.
###
"""
    return few_shot_template

def chat_base_template(char_prompt_path):
    cur_dir = os.getcwd()
    char_path = os.path.join(cur_dir, 'Characters', char_prompt_path, 'prompt.txt')
    with open(char_path, 'r') as f:
        char_prompt = f.read()

    chat_template = """
    You are a Fictional Character that talks to a user through the ###character prompt### below.
    ###character prompt###
    {char_prompt}

    Ensure your responses are consistent with the world and setting of your story
    Let's think step by step.

    User : {message}
    You : 
"""

    return {"chat_template": chat_template, "char_prompt": char_prompt}