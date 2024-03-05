import pdb, os, sys, pdb
import base64
def background_select():
  cur_dir = os.getcwd()
  back_path = os.path.join(cur_dir, '..', 'frontend', 'src', 'components', 'Static','chat_background')
  back_image_files = os.listdir(back_path)

  except_list = ['635b6e3b30bfeae7b713cb8162aa2c9a.jpg', 'Apocalypse.jpg', 'cyberpunk-city-buildings-art.jpg', 'fantasy_desktop.jpg', 'futuristic.jpg', 'western.jpg']
  back_image_files = [selected_files for selected_files in back_image_files if selected_files not in except_list]

  print("-"*80)
  print(back_image_files)

  return back_image_files
