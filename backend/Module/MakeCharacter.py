import os
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

    self.make_char_for_diffusion(prompt_file_path=prompt_file_path)

  def make_char_for_diffusion(self, prompt_file_path):
    print('asd')

