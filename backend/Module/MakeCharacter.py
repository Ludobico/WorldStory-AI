import os

def make_char_folder(name, prompt):
  cur_dir = os.getcwd()
  char_folder = os.path.join(cur_dir, 'Characters')
  print('name test : {0}'.format(name))
  print('prompt test : {0}'.format(prompt))

  file_name = name + '.txt'
  file_path = os.path.join(char_folder, file_name)

  with open(file_path, 'w', encoding='utf-8') as f:
    f.write(prompt)
    