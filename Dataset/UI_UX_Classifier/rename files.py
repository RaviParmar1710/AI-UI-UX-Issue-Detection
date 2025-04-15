import os

# Set the path to your screenshots folder
folder_path = "D:/UI UX code/Project drive all files/UI_UX_Classifier/test_screenshots"

# Make sure the folder exists
if not os.path.exists(folder_path):
    print("Folder not found!")
else:
    for count, filename in enumerate(os.listdir(folder_path)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            new_filename = f"img_{count+1}.jpg"
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)
            os.rename(old_path, new_path)

    print("Renaming completed!")
