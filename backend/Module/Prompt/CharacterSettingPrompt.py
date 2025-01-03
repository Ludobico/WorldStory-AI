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

NAME GENERATION RULES

Create a distinctive name by combining unusual elements
Draw from multiple cultural backgrounds
Consider the character's era and setting
Mix different naming conventions:

Ancient mythological elements
Nature-inspired names
Compound names with unique combinations
Modified traditional names
Abstract concepts or emotions
Astronomical terms
Musical terms
Ancient languages (Latin, Greek, Sanskrit, etc.)
Cultural fusion names
Made-up names that follow linguistic patterns


Avoid common or overused character names
The name should reflect the character's background and setting

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

## INPUT ANALYSIS

Scan the provided character description
Focus specifically on visual and physical attributes
Identify key appearance elements: body type, facial features, hair, eyes, clothing, accessories, notable visual characteristics
Include gender-specific visual cues

```
{{main physical descriptors}}, {{key features}}, {{distinctive elements}},
{{main clothing items}}, {{accessories}}, {{material details}}
{{aesthetic type}}, {{style influences}}, {{atmosphere elements}}
({{important feature:1.2}}), ({{defining characteristic:1.3}}), ({{unique element:1.1}})
```

Use plain English keywords
Separate elements with commas
Include weighting for important elements (1.1 to 1.4)
Keep descriptions concise but comprehensive
Focus on visual elements only
Avoid non-visual personality traits
Include style and atmosphere context

## IMPORTANT
Provide ONLY the formatted keywords without any introduction, explanation, or confirmation phrases
Do not include phrases like "Keywords for [name]:", "Sure!", "Let me help", "Here's", etc.
Start directly with the formatted output
Do not include any meta-commentary or explanatory text
Output should begin immediately with the keywords in the specified format
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