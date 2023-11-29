import os
from enum import Enum

class SourcesEnum(Enum):
    CHAPMANGANATO: str = "https://chapmanganato.com/"
    MANGAREAD: str = "https://www.mangaread.org/"

class Source:
    sourceType: SourcesEnum
    chapter: str
    manga_name: str
    manga: str

    def __init__(self, sourceType: SourcesEnum) -> None:
        self.sourceType = sourceType
    

class DownloadMangaData:
    USER_FOLDER: str = os.path.expanduser('~')
    CHROMEDRIVER: str = os.path.join(os.getcwd(), "chromedriver")
    LOCAL_DOWNLOADS: str = os.path.join(os.getcwd(), 'downloads')
    CHAPTERS_DESTINATION: str = os.path.join(os.getcwd(), 'documentos')
    source: Source

    def __init__(self, source: Source) -> None:
        self.source = source