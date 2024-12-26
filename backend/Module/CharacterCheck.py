import os
import json
import configparser
import random
import base64

class CharacterConfig:
  def Character_folder_check():
    cur_dir = os.getcwd()
    char_path = os.path.join(cur_dir ,'Characters')
    char_folder_names = []

    if os.path.exists(char_path) and os.path.isdir(char_path):
      for folder_name in os.listdir(char_path):
        folder_path = os.path.join(char_path, folder_name)
        if os.path.isdir(folder_path):
            if folder_name != 'User':
              char_folder_names.append(folder_name)
    return char_folder_names

  def Character_image_parser(char_name):
    cur_dir = os.getcwd()
    character_image_path = os.path.join(cur_dir, 'Characters', char_name)
    image_files = []
    valid_extention = ['.jpg', '.png', '.jpeg', '.gif']

    for filename in os.listdir(character_image_path):
      if any(filename.lower().endswith(ext) for ext in valid_extention):
        image_files.append(os.path.join(character_image_path, filename))

    if len(image_files) > 1:
      image_files = str(random.choice(image_files))
    elif len(image_files) == 1:
      image_files = str(image_files[0])
    else:
      image_files = None
    if image_files != None:
      with open(image_files, 'rb') as f:
        base64image = base64.b64encode(f.read())
        return base64image

  def user_config_parser():
    cur_dir = os.getcwd()
    user_config_path = os.path.join(cur_dir ,'Characters', 'User', 'UserConfig.ini')
    user_config = configparser.ConfigParser()
    user_config.read(user_config_path, encoding='UTF-8')

    default = user_config['DEFAULT']
    preference = user_config['PREFERENCE']

    # default config
    user_name = default['user_name']
    user_lang = default['language']
    memory_limit = default['memory']

    # preference config
    era = preference['era']
    gender = preference['gender']
    name = preference['name']


    return {"user_name" : user_name,"user_lang" : user_lang, "era" : era, "gender" : gender, "name" : name, "memory" : memory_limit}

  def user_image_parser():
    cur_dir = os.getcwd()
    user_image_path = os.path.join(cur_dir ,'Characters', 'User')
    image_files = []
    valid_extention = ['.jpg', '.png', '.jpeg', '.gif']
    
    for filename in os.listdir(user_image_path):
      if any(filename.lower().endswith(ext) for ext in valid_extention):
        image_files.append(os.path.join(user_image_path, filename))

    if len(image_files) > 1:
      image_files = str(random.choice(image_files))
    elif len(image_files) == 1:
      image_files = str(image_files[0])
    else:
      image_files = None
    if image_files != None:
      with open(image_files, 'rb') as f:
        base64image = base64.b64encode(f.read())
    
        return base64image



