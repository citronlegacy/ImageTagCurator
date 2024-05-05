import os
def count_images_in_folder(folder):
  count = 0
  # Iterate directory
  for f in os.listdir(folder):
      # check if current path is a file and also not a .txt file
      if (os.path.isfile(os.path.join(folder, f)) and not f.lower().endswith(".txt")):
          count += 1
  return count