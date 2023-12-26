import os
import zipfile
from src.utils.config import AppConfig

def list_files(directory: str):
    with os.scandir(directory) as entries:
        files = [entry.name for entry in entries if entry.is_file()]
    return files

def zip_to_result(final_file: str):

    with zipfile.ZipFile(final_file, 'w', allowZip64=True) as zipf:

        for file in list_files(AppConfig.temp_folder()):
            
            file_path = os.path.join(AppConfig.temp_folder(), file)
            
            arcname = os.path.relpath(file_path, AppConfig.temp_folder())
            
            zipf.write(file_path, arcname)

def zip_folder(folder_path: str, zip_path: str):
    with zipfile.ZipFile(zip_path, 'w', allowZip64=True) as zipf:
        for foldername, subfolders, filenames in os.walk(folder_path):
            zipped_size = os.path.getsize(zip_path)
            if zipped_size >= get_total_size(folder_path):
                break
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipped_size = os.path.getsize(zip_path)
                if zipped_size >= get_total_size(folder_path):
                    break
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def get_total_size(folder_path: str):
    total_size = 0
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            total_size += os.path.getsize(file_path)

    return total_size