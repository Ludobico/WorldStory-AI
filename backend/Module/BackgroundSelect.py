import pdb, os, sys, pdb
import base64
def background_select():
  cur_dir = os.getcwd()
  back_path = os.path.join(cur_dir, '..', 'frontend', 'src', 'components', 'Static','chat_background')
  split_back_image_files = []
  back_image_files = os.listdir(back_path)

  for i in back_image_files:
    split_back_image_files.append(i.split('.')[0])

  except_list = ['635b6e3b30bfeae7b713cb8162aa2c9a', 'Apocalypse', 'cyberpunk-city-buildings-art', 'fantasy_desktop', 'futuristic', 'western']
  split_back_image_files = [selected_files for selected_files in split_back_image_files if selected_files not in except_list]

  return split_back_image_files
