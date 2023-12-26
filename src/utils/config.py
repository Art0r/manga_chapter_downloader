from dataclasses import dataclass
import os

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