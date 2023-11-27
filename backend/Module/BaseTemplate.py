import os
def base_template():
    template = """
    {instruct}
    Name:
    Gender:
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

Personality: Nora is an intelligent, ambitious, and determined individual. She is confident in her abilities and has a strong sense of justice. She can be direct and assertive when needed, but also has a compassionate side that she reserves for those she cares about.

Background: Nora grew up in a working-class family in a small town on the outskirts of a bustling city. Despite limited resources, she excelled academically and was determined to create a better life for herself. She worked hard to earn a scholarship and attended a prestigious university, where she studied journalism.

Appearance: Nora is of average height and has short, dark hair that she usually wears in a ponytail. She has a sharp, angular face with prominent cheekbones, and piercing blue eyes. She often wears simple, elegant clothing that complements her features.

Setting: Modern

Additional details: Nora is a journalist who works for a major newspaper. She is passionate about uncovering the truth and exposing corruption, even if it means putting herself in harm's way. She is also an advocate for social justice and often uses her platform to shed light on important issues affecting vulnerable communities. Despite her tough exterior, she struggles with anxiety and often seeks solace in yoga and meditation. Nora's ultimate goal is to become a renowned investigative journalist and make a lasting impact on the world.
###
### example2

Name: Seraphina Emberthorn

Gender: Female

Personality: Seraphina is a complex character, a blend of determination and mystery. She possesses an unwavering sense of justice, fueled by a tragic event in her past. Beneath her stoic exterior lies a wellspring of compassion for the downtrodden and a burning desire for a world free from oppression. Despite her serious demeanor, she harbors a dry wit that surfaces in moments of camaraderie. Seraphina is fiercely loyal to those she deems worthy of trust, and her resilience in the face of adversity makes her both a formidable ally and a daunting adversary. Her sense of duty sometimes leads her to make difficult decisions, showcasing the depth of her character.

Background: Seraphina hails from a realm where magic and technology coexist, creating a unique fusion of the fantastical and the futuristic. Born into a lineage of renowned magic wielders, the Emberthorns, her childhood was shattered when a malevolent force targeted her family. The traumatic event left her orphaned, but it also awakened a latent magical ability within her. As she grew, Seraphina dedicated herself to honing her newfound powers and vowed to eradicate the darkness that had befallen her family.

Trained by a clandestine order of mystical warriors, Seraphina became a skilled mage-knight, blending her innate magical prowess with masterful swordsmanship. Her quest for justice led her to become a defender of the innocent, navigating through a world rife with political intrigue, ancient mysteries, and technological wonders.

Appearance: Seraphina cuts a striking figure with her long, flowing ebony hair and piercing cerulean eyes that seem to hold the weight of her past. She wears a set of enchanted armor adorned with intricate runes, a testament to her magical heritage. The armor seamlessly integrates technology and mysticism, providing both protection and enhanced capabilities. Her slender frame belies the strength she possesses, and the scars on her hands and arms tell a silent tale of battles fought and won.

In her travels through different settings, Seraphina adapts her appearance to blend into each environment. In the futuristic cityscapes, she dons a sleek, high-tech cloak that conceals her armor's ethereal glow. In the medieval realms, her attire transforms into the attire of a skilled sorceress, complete with a cloak that billows with an otherworldly breeze.

Seraphina's visage reflects the duality of her character, a warrior with a haunted past and an unyielding commitment to forging a brighter future.
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
    Ensure your responses are consistent with the world and setting of your story. Be creative and feel free to include any relevant details that will help the model generate a rich and unique character description. Provide as much information as possible to make the character come to life within the story you have in mind
    ###character prompt###
    {char_prompt}
    ######
    Ensure your responses are consistent with the world and setting of your story
    Let's think step by step.
    
    {message}
    
"""

    return {"chat_template": chat_template, "char_prompt": char_prompt, "char_prompt_path": char_prompt_path}

def image_generate_prompt(text_gen_prompt):
    image_gen_template = """
    
"""