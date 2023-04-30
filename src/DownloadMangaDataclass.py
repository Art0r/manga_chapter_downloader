import os
from dataclasses import dataclass


@dataclass
class DownloadMangaDataclass:
    URL: str = "https://po2scans.com"
    USER_FOLDER: str = os.path.expanduser('~')
    CHROMEDRIVER: str = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "chromedriver")
    LOCAL_DOWNLOADS: str = os.path.join(os.getcwd(), '../downloads')
    CHAPTERS_DESTINATION: str = os.path.join(USER_FOLDER, 'Documentos', 'mangás')
