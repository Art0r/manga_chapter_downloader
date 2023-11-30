from src.DownloadMangaData import DownloadMangaData, SourcesEnum

def verify_source(url: str) -> DownloadMangaData:

    isChapmanganato = url.find("manganato") != -1
    isMangaread = url.find("mangaread") != -1
    
    if (isChapmanganato): return DownloadMangaData(sourceType=SourcesEnum.CHAPMANGANATO)
    if (isMangaread): return DownloadMangaData(sourceType=SourcesEnum.MANGAREAD)
        