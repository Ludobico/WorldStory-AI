import os, sys, pdb
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if backend_root not in sys.path:
    sys.path.append(backend_root)

from Module.LLMChain.CustomLLM import CustomLLM_GPT
from Module.Prompt.CharacterSettingPrompt import character_to_CLIP_keywords_conversion_prompt
class CharacterImageGeneration:
  @staticmethod
  def image_gen(input_char_prompt):
    llm = CustomLLM_GPT()
    prompt = character_to_CLIP_keywords_conversion_prompt()
    chain = prompt | llm
    desc = input_char_prompt
    result = chain.invoke({"description" : desc})
    print(result)
    return result

if __name__ == "__main__":
    example_description = """
**Name:** Aria Thornfield

**Gender:** Female

**Personality:**  
Aria is an enigmatic and fiercely independent spirit, characterized by her insatiable curiosity and resourcefulness. She possesses a clever wit that often serves as both her shield and her charm, allowing her to navigate the complexities of her environment with ease. While she can be sardonic and a bit aloof, her loyalty to her chosen friends runs deep, and she is always willing to lend a helping hand to those in need. Aria is driven by a desire for truth and justice, often putting herself in precarious situations to uncover hidden realities. Her motivations are rooted in a childhood marked by deception, leading her to seek transparency in a world full of shadows.

**Background:**  
Aria grew up in the industrial heart of a sprawling steampunk city known as Cogsworth, where the air is thick with the scent of oil and iron. The daughter of a renowned inventor, she was raised in a workshop filled with whirring gears and the glow of gas lamps. However, her idyllic childhood was shattered when her father was accused of treason against the ruling elite and disappeared under mysterious circumstances. This event ignited Aria's quest for justice, propelling her into the underground world of espionage and rebellion. A defining moment came when she discovered a hidden journal belonging to her father, filled with blueprints for a powerful invention that could shift the balance of power in the city. This discovery fueled her determination to clear his name and expose the corruption that plagues Cogsworth.

**Appearance:**  
Aria stands at an average height, with an athletic build honed from years of navigating the rooftops and alleys of her city. Her fiery red hair is often tied back in a practical braid, with loose strands framing her sharp, angular face. She has striking green eyes that seem to sparkle with mischief and intelligence. Aria's attire blends functionality with style; she typically wears a fitted leather vest over a billowy white blouse and sturdy trousers, adorned with an intricate brass belt that holds her various tools and gadgets. She dons fingerless gloves and knee-high boots, allowing her to move freely while exuding an air of confidence. A small, intricate mechanical bird, crafted by her father, perches on her shoulder as both a companion and a tool for surveillance.

**Setting:**  
The story unfolds in Cogsworth, a bustling steampunk city characterized by towering clockwork buildings, steam-powered machinery, and a complex network of airships and trains. The streets are alive with the sounds of hissing steam and clanking metal, while the sky is often shrouded in an industrial haze. Beneath the surface, a stark divide exists between the wealthy elite and the struggling working class, creating an atmosphere ripe for rebellion. The city is a maze of hidden passages, underground factories, and secret societies, where the line between friend and foe is often blurred. In this world, Aria's journey intertwines with a cast of rebels, inventors, and spies, as they work to dismantle a corrupt regime and reclaim their city’s future.
"""  
    CharacterImageGeneration.image_gen(example_description)