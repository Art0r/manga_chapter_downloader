from dataclasses import dataclass
import logging
import os
import shutil

@dataclass
class AppConfig:
    # Folder where the generated files will be stored
    @staticmethod
    def temp_folder() -> str: return os.path.join(os.getcwd(), 'app-temp')
    
    # Where the image downloads will be stored and the data will be manipulated
    @staticmethod
    def local_downloads() -> str: return os.path.join(AppConfig.temp_folder(), 'downloads')

    @staticmethod
    def extension() -> str: return '.cbz'

    def clean_up():
        try:
            # removing folder and downloaded content
            shutil.rmtree(AppConfig.local_downloads())

        except OSError as e:
            logging.error(f"Error: {AppConfig.local_downloads()} - {e}")
