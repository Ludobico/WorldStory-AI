import os, sys, pdb
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if backend_root not in sys.path:
    sys.path.append(backend_root)

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

def character_generation_prompt():
    """
    Prompt for generating a character
    """
    system_templte = """
You are a talented writer creating a character for a story. Provide detailed information for the following aspects of your character

Generate a character for a story:

Name: {name}

Gender: {gender}

Personality: Describe the character's key traits, behaviors, and motivations.

Background: Outline the character's history, significant experiences, or defining moments.

Appearance: Detail the character's physical attributes, style, and any distinctive features.

Setting: {era}

Guidelines:

Avoid repeating information across sections.
Include creative, varied details that make the character distinct and memorable.
Ensure all elements are consistent with the chosen setting.
Example settings to choose from: Fantasy, Cyberpunk, Futuristic, Steampunk, Modern, Western, Ancient, Retro, Post-Apocalyptic.

"""

    messages = [
        SystemMessagePromptTemplate.from_template(system_templte)
    ]

    prompt = ChatPromptTemplate(messages=messages, input_variables = ["name", "gender", "era"])
    return prompt

def character_to_CLIP_keywords_conversion_prompt():
    """
    Transform sentences into keywords for CLIP Text Encoding
    """

    system_template = """
You are a specialized prompt engineer focusing on converting character descriptions into optimized CLIP text encoding keywords for AI image generation. Follow these steps to convert character appearance descriptions into structured keywords:

INPUT ANALYSIS

Scan the provided character description
Focus specifically on visual and physical attributes
Identify key appearance elements: body type, facial features, hair, eyes, clothing, accessories, notable visual characteristics

KEYWORD EXTRACTION
Extract and categorize visual elements into these categories:

Physical Traits: height, build, face shape
Features: eye color, hair style/color, distinctive marks
Attire: clothing, accessories, equipment
Style Elements: overall aesthetic, time period influences
Notable Visual Characteristics: unique or defining visual elements

```
{main physical descriptors}, {key features}, {distinctive elements}
{main clothing items}, {accessories}, {material details}
{aesthetic type}, {style influences}, {atmosphere elements}
({important feature:1.2}), ({defining characteristic:1.3}), ({unique element:1.1})
```

Use plain English keywords
Separate elements with commas
Include weighting for important elements (1.1 to 1.4)
Keep descriptions concise but comprehensive
Focus on visual elements only
Avoid non-visual personality traits
Include style and atmosphere context
"""

    human_template = """
{description}
"""
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ]

    prompt = ChatPromptTemplate(messages=messages, input_variables = ["description"])
    return prompt