import os, random
def test():
  cur_dir = os.getcwd()
  user_image_path = os.path.join(cur_dir ,'backend','Characters', 'User')
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
  
  print(image_files)
  print(type(image_files))

if __name__ == "__main__":
  test()