import os
import base64
from Module.Proxy.prodia import Generation
from Module.Template.BaseTemplateForImage import base_image_generation
class MakeCharacter:
  def make_char_folder(self, name, prompt):
    cur_dir = os.getcwd()
    char_folder = os.path.join(cur_dir, 'Characters', name)

    if not os.path.exists(char_folder):
      os.makedirs(char_folder)

    file_name = 'prompt.txt'
    prompt_file_path = os.path.join(char_folder, file_name)

    with open(prompt_file_path, 'w', encoding='utf-8') as f:
      f.write(prompt)

  def make_char_image(self, summary_prompt):
    comp_prompt = base_image_generation(summary_prompt)
    generator = Generation()
    return generator.create(comp_prompt)

