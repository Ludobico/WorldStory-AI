import pdb, os, sys, pdb
import base64
def background_select():
  def encode_image_to_base64(image_name, back_path):
    image_path = os.path.join(back_path, image_name)

    if os.path.exists(image_path):
      with open(image_path, 'rb') as img_file:
        encoded_image = base64.b64encode(img_file.read())

        return {
          "image_name" : image_name.split('.')[0],
          "image_base64" : encoded_image
        }

  cur_dir = os.getcwd()
  back_path = os.path.join(cur_dir, '..', 'frontend', 'src', 'components', 'Static','chat_background')
  back_image_files = os.listdir(back_path)
  except_list = ['635b6e3b30bfeae7b713cb8162aa2c9a.jpg', 'Apocalypse.jpg', 'cyberpunk-city-buildings-art.jpg', 'fantasy_desktop.jpg', 'futuristic.jpg', 'western.jpg']
  back_image_files = [file for file in back_image_files if file not in except_list]

  encoded_images = [encode_image_to_base64(image_name, back_path) for image_name in back_image_files if encode_image_to_base64(image_name, back_path) is not None]

  return encoded_images
