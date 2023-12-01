import os
from io import BytesIO
from PIL import Image
import base64
from Module.Proxy.prodia import Generation
from Module.Template.BaseTemplateForImage import base_image_generation
class MakeCharacter:
  def make_char_folder(self, name, prompt, image):
    cur_dir = os.getcwd()
    char_folder = os.path.join(cur_dir, 'Characters', name)

    if not os.path.exists(char_folder):
      os.makedirs(char_folder)

    file_name = 'prompt.txt'
    prompt_file_path = os.path.join(char_folder, file_name)
    
    # data:image/png;base64, 이런식으로 데이터가 전달되기때문에 , 다음 실질적인 데이터만 추출이 필요
    image_data = image.split(",")[1]

    image_bytes = BytesIO(base64.b64decode(image_data))
    decoded_image = Image.open(image_bytes)
    decoded_image.save(os.path.join(char_folder, f'{name}.png'))

    with open(prompt_file_path, 'w', encoding='utf-8') as f:
      f.write(prompt)

  def make_char_image(self, summary_prompt):
    comp_prompt = base_image_generation(summary_prompt)
    generator = Generation()
    return generator.create(comp_prompt)

