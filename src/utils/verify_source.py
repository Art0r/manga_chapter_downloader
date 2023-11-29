from src.DownloadMangaData import Source, DownloadMangaData, SourcesEnum

def verify_source(url: str) -> Source:

    isChapmanganato = url.find("manganato") != -1
    isMangaread = url.find("mangaread") != -1
    
    if (isChapmanganato): return Source(SourcesEnum.CHAPMANGANATO)
    if (isMangaread): return Source(SourcesEnum.MANGAREAD)
        