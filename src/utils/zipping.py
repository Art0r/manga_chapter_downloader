import os
import zipfile


def zip_folder(folder_path, zip_path):
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

def get_total_size(folder_path):
    total_size = 0
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            total_size += os.path.getsize(file_path)

    return total_size