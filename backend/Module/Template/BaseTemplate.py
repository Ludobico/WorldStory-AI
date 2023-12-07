import os
from Module.CharacterCheck import CharacterConfig
def base_template():
    user_preference = CharacterConfig.user_config_parser()
    template = """
    {instruct}
    Name: {name}

    Gender: {gender}

    Personality:

    Background:

    Appearance:

    Setting: {era}

    Ensure your responses are consistent with the world and setting of your story. Be creative and feel free to include any relevant details that will help the model generate a rich and unique character description. Provide as much information as possible to make the character come to life within the story you have in mind.
    create a character for a story set in various settings such as Fantasy, Cyberpunk, Futuristic, Steampunk, Modern, Western, Ancient, Retro, Post-Apocalyptic, etc...
    Let's think step by step.
    Feel free to elaborate on each point to create a comprehensive portrayal of your character.

"""

    instruct = "You are a talented writer creating a character for a story. Provide detailed information for the following aspects of your character:"
    return {"template": template, "instruct": instruct}

def few_shot_base_template():
    few_shot_template = """
### example1
Name: Max Maverick Raine

Gender: Male

Personality:
Maverick is a charismatic and adaptable individual, a chameleon in the vibrant chaos of the cyberpunk world. He thrives on the edge, displaying a devil-may-care attitude that conceals a razor-sharp intellect. Quick-witted and resourceful, Maverick possesses a natural charm that allows him to navigate the treacherous currents of the dystopian city with ease. Despite his roguish exterior, he harbors a sense of loyalty to those who earn his trust, making him both a reliable ally and a formidable adversary.

Background:
Maverick's origins are shrouded in mystery, his past a tapestry of shadows and neon. Born in the underbelly of the cyberpunk city, he grew up amidst the flickering holographic signs and the distant hum of machinery. His childhood was marked by survival instincts, learning to adapt to the ruthless streets where the line between legality and criminality blurred.

A former data thief and information broker, Maverick's skills caught the attention of a clandestine organization known for their manipulation of information and power plays in the city's high-tech underworld. However, a betrayal within the organization forced him to go solo, adopting the alias "Maverick" as a symbol of his defiance.

Appearance:
Maverick is a lean and agile figure, his cybernetic enhancements subtly integrated into his body to enhance speed and agility. His hair, a mix of natural and neon-dyed strands, falls messily over his forehead, framing a face adorned with a cybernetic eye that glows with a subtle red hue. He favors a mix of urban streetwear and tactical gear, with a long, weathered trench coat adorned with a multitude of pockets concealing an array of gadgets.

His cyberpunk aesthetic extends to his limbs, where synthetic fibers interweave with flesh, hinting at his past augmentations. Maverick's tattoos, glowing with bioluminescent ink, shift and pulse with the rhythm of the city, reflecting his ever-changing alliances and allegiances.

Setting: Cyberpunk

The city is a battleground for power, with rival factions vying for control of information, resources, and the hearts of the people. Maverick navigates this precarious landscape, dancing between the shadows and the neon lights, seeking both profit and a chance at redemption.

Maverick's story unfolds against the backdrop of a world where hackers, mercenaries, and rebels clash in a perpetual struggle for freedom and control. In this cyberpunk realm, where alliances are fragile and secrets are currency, Maverick's journey is a high-stakes game where the winner takes all.
###

### example2
Name: Nora Blackwood

Gender: Female

Personality: Nora is an intelligent, ambitious, and determined individual. She is confident in her abilities and has a strong sense of justice. She can be direct and assertive when needed, but also has a compassionate side that she reserves for those she cares about.

Background: Nora grew up in a working-class family in a small town on the outskirts of a bustling city. Despite limited resources, she excelled academically and was determined to create a better life for herself. She worked hard to earn a scholarship and attended a prestigious university, where she studied journalism.

Appearance: Nora is of average height and has short, dark hair that she usually wears in a ponytail. She has a sharp, angular face with prominent cheekbones, and piercing blue eyes. She often wears simple, elegant clothing that complements her features.

Setting: Modern

Additional details: Nora is a journalist who works for a major newspaper. She is passionate about uncovering the truth and exposing corruption, even if it means putting herself in harm's way. She is also an advocate for social justice and often uses her platform to shed light on important issues affecting vulnerable communities. Despite her tough exterior, she struggles with anxiety and often seeks solace in yoga and meditation. Nora's ultimate goal is to become a renowned investigative journalist and make a lasting impact on the world.
###
"""
    return few_shot_template
# char_prompt_path = character name
def chat_base_template(char_prompt_path):
    cur_dir = os.getcwd()
    char_path = os.path.join(cur_dir, 'Characters', char_prompt_path, 'prompt.txt')
    with open(char_path, 'r') as f:
        char_prompt = f.read()

    chat_template = """
    You are a Fictional Character that talks to a user through the ###character prompt### below.
    Ensure your responses are consistent with the world and setting of your story.Provide as much information as possible to make the character come to life within the story you have in mind
    ###character prompt###
    {char_prompt}
    ######

    ###Previous conversation###
    {chat_history}
    ######
    
    {user_name} : {message}
    {ai_name} : 
    
"""

    return {"chat_template": chat_template, "char_prompt": char_prompt, "char_prompt_path": char_prompt_path}