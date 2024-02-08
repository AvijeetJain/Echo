import os
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path

def list_files_and_empty_folders(folder_path):
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        # Add files to list
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(str(file_path))
        
        # Check if folder is empty
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            # if not os.listdir(folder_path):
            file_list.append(str(folder_path))

    return file_list

# # Example usage:
# folder_path = ".\public"
# files = list_files_and_empty_folders(folder_path)

# Files = ''
# print("Files:")
# for file_path in files:
#     # print(file_path)
#     Files += file_path + '\n'

# print(Files)

# A = Files.split('\n')

# for i in range(len(A)):
#     print(A[i])

# from pathlib import Path

# RECV_FOLDER_PATH = Path.home() / Path("downloads")
# print(RECV_FOLDER_PATH)

# SHARE_COMPRESSED_PATH = Path.home() / Path(".Drizzle/compressed")
# print(SHARE_COMPRESSED_PATH)

# SHARE_FOLDER_PATH = Path.home() / Path("./public")