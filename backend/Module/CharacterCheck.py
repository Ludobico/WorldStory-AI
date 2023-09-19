import os
import json

def Character_folder_check():
  cur_dir = os.getcwd()
  char_path = os.path.join(cur_dir ,'Characters')
  char_folder_names = []

  if os.path.exists(char_path) and os.path.isdir(char_path):
    for folder_name in os.listdir(char_path):
      folder_path = os.path.join(char_path, folder_name)
      if os.path.isdir(folder_path):
        char_folder_names.append(folder_name)
  return char_folder_names



