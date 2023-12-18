import os
from enum import Enum

class SourcesEnum(Enum):
    CHAPMANGANATO: str = "https://chapmanganato.com/"
    MANGAREAD: str = "https://www.mangaread.org/"

class DownloadMangaData:
    # Constants

    # Root user folder. For Linux ~, for Windows C:\Users\THIS_USER
    ROOT_USER_FOLDER: str = os.path.expanduser('~')
    
    # Folder where the generated files will be stored
    TEMP_FOLDER: str = os.path.join(os.getcwd(), 'temp')
    
    # Where the image downloads will be stored and the data will be manipulated
    LOCAL_DOWNLOADS: str = os.path.join(os.getcwd(), 'temp', 'downloads')
    
    # Where the final file will be moved to
    CHAPTERS_DESTINATION: str = os.path.join(ROOT_USER_FOLDER, 'Documentos')

    # Variables 

    # Source enum, mainly used to control conditions
    sourceType: SourcesEnum

    # the manga chapter how is displayed in the url
    chapter: str

    # the manga manga title how is displayed in the url
    manga_title: str

    def __str__(self) -> str:
        return self.manga_title


    def __init__(self, sourceType: SourcesEnum) -> None:
        self.sourceType = sourceType
    