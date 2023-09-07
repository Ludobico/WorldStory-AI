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
Name: Luna

Gender : Female

Personality:  Luna is an introverted and enigmatic individual.
She possesses a deep curiosity about the world around her and tends to be introspective.
Luna is observant, intelligent, and often lost in her own thoughts.

Background: Luna works as a librarian in a small town. She has a passion for books and spends her free time exploring ancient legends and folklore.
She possesses a unique ability to see and communicate with supernatural entities.
###
"""
    return few_shot_template