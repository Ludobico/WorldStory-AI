import os
import json

class LLMCheck:
  def __init__(self) -> None:
    self.cur_dir = os.getcwd()
    self.model_config_list_file_path = os.path.join(self.cur_dir , 'Config', 'CTransformersModelList.json')
    self.model_list_file_path = os.path.join(self.cur_dir, 'Models')
  def json_read(self):
    model_config_list_file_path = self.model_config_list_file_path
    model_list_file_path = self.model_list_file_path
    if os.path.exists(model_list_file_path):
      model_list_files = os.listdir(model_list_file_path)
      bin_files = [file for file in model_list_files if file.endswith(".bin")]

      model_list = []

      with open(model_config_list_file_path, 'r') as config_file:
        config_data = json.load(config_file)

        for model_config in config_data:
          for bin_file in bin_files:
              if bin_file in model_config['model_name']:
                  model_list.append({'label' : model_config['model_name'], 'value' : model_config['model_name'], 'RAM' : model_config['Max RAM required']})
    return model_list






