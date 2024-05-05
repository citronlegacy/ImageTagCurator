import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
import tkinter as tk
from tkinter import StringVar, filedialog
from collections import Counter
from image_charter import create_tag_chart

class FileTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Image Tag Curator')
        self.setGeometry(100, 100, 300, 200)

        # Create buttons
        self.selectDirButton = QPushButton('Select Directory', self)
        self.selectDirButton.clicked.connect(self.selectDirectory)

# Global variables to store the input values
directory_path = ""
trigger_value = ""
absorb_tags_value = ""
extra_tags_value = ""
top_tags = ""
text_field_width = 100

def clean_tags(tags_list):
    cleaned_tags = [t.strip() for t in tags_list.split(",")]
    cleaned_tags = [t.replace("_", " ") if len(t) > 3 else t for t in cleaned_tags]
    # Check if the list contains only an empty string
    if len(cleaned_tags) == 1 and cleaned_tags[0] == '':
        return []
    return cleaned_tags


def curate_tags():
  global directory_path, trigger_value, absorb_tags_value, extra_tags_value, top_tags
  images_folder = directory_path

  blacklisted_tags = clean_tags(extra_tags_value)
  absorbed_these_tags_into_trigger = clean_tags(absorb_tags_value)
  trigger_tags = clean_tags(trigger_value)

  top_tags = Counter()
  for txt in [f for f in os.listdir(images_folder) if f.lower().endswith(".txt")]:
    with open(os.path.join(images_folder, txt), 'r') as f:
      tags = [t.strip() for t in f.read().split(",")]
      tags = [t.replace("_", " ") if len(t) > 3 else t for t in tags]

      # Remove tags if they are in blacklisted_tags or absorbed_these_tags_into_trigger
      tags = [t for t in tags if t not in blacklisted_tags]
      tags = [t for t in tags if t not in absorbed_these_tags_into_trigger]

      # Add Triggers to beginning of tags

      for trigger_tag in trigger_tags:
        if trigger_tag in tags:
          tags.remove(trigger_tag)
        tags.insert(0, trigger_tag)

    top_tags.update(tags)
    with open(os.path.join(images_folder, txt), 'w') as f:
      f.write(", ".join(tags))

  #print("\n".join(f"{k}," for k, v in top_tags.most_common(50)))



def select_directory():
    global directory_path
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)
        directory_path = directory

def update_and_process_directory():
    global directory_path, trigger_value, absorb_tags_value, extra_tags_value, top_tags
    # Update input values
    directory_path = directory_entry.get()
    trigger_value = trigger_entry.get()
    absorb_tags_value = absorb_tags_entry.get()
    extra_tags_value = extra_tags_entry.get()
    
    if directory_path:
        # Perform actions on the files in the selected directory
        print(f"Processing directory: {directory_path}")
        print(f"Trigger: {trigger_value}")
        print(f"Absorb these tags: {absorb_tags_value}")
        print(f"Extra absorbed tags: {extra_tags_value}")
    else:
        print("Please enter a directory path.")

    curate_tags()
    create_tag_chart(directory_path, top_tags)
    

# Create the main window
root = tk.Tk()
root.title("Directory Processing Tool")

# Create a label and entry for entering the directory path
directory_label = tk.Label(root, text="Directory Path:")
directory_label.grid(row=0, column=0, padx=5, pady=5)

directory_entry = tk.Entry(root, width=text_field_width)
directory_entry.grid(row=0, column=1, padx=5, pady=5)

# Create a button to select the directory
select_button = tk.Button(root, text="Select Directory", command=select_directory)
select_button.grid(row=0, column=2, padx=5, pady=5)

# Create labels and entries for additional fields
trigger_label = tk.Label(root, text="Trigger:")
trigger_label.grid(row=1, column=0, padx=5, pady=5)

trigger_entry = tk.Entry(root, width=text_field_width)
trigger_entry.grid(row=1, column=1, padx=5, pady=5)

absorb_tags_label = tk.Label(root, text="Absorb these tags:")
absorb_tags_label.grid(row=2, column=0, padx=5, pady=5)

absorb_tags_entry = tk.Entry(root, width=text_field_width)
absorb_tags_entry.grid(row=2, column=1, padx=5, pady=5)

extra_tags_label = tk.Label(root, text="Extra absorbed tags:")
extra_tags_label.grid(row=3, column=0, padx=5, pady=5)

extra_tags_default = "absurdres, highres, bangs, breasts, nintendo, pokemon, 1girl, solo"

extra_tags_var = StringVar(root)
extra_tags_entry = tk.Entry(root, textvariable=extra_tags_var, width=text_field_width)
extra_tags_var.set(extra_tags_default)
extra_tags_entry.grid(row=3, column=1, padx=5, pady=5)

# Create a button to process the directory
process_button = tk.Button(root, text="Process Directory", command=update_and_process_directory)
process_button.grid(row=4, column=1, padx=5, pady=5)



# Run the main event loop
root.mainloop()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileTool()
    ex.show()
    sys.exit(app.exec_())
