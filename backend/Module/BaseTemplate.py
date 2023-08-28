def base_template():
    template = """
    {instruct}

    Character Name:
    Gender:
    Age:
    Personality:
    Background:
    Dialogue Style:
    Appearance:

    Ensure your responses are consistent with the world and setting of your story. Be creative and feel free to include any relevant details that will help the model generate a rich and unique character description. Provide as much information as possible to make the character come to life within the story you have in mind.
    create a character for a story set in various settings such as historical, futuristic, fantasy,modern or science fiction.
    Let's think step by step.

    Provide a JSON-formatted response with information about a person. Include the following fields: Character Name, Gender, Age, Personality, Background, Dialogue Style and Appearance. Do not create any keys except for the 7 keys above

    writer : 
    """

    instruct = "You are a talented writer creating a character for a story. Provide detailed information for the following aspects of your character:"
    return {"template": template, "instruct": instruct}
