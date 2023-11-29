from src.DownloadManga import DownloadManga
from src.DownloadMangaData import DownloadMangaData, SourcesEnum
from src.utils.verify_source import verify_source

if __name__ == "__main__":
    url: str = str(input("Digite o código do capítulo:\n"))
    downloadMangaData = DownloadMangaData(source=verify_source(url=url))
    if (downloadMangaData.source.sourceType is SourcesEnum.CHAPMANGANATO):
        splitUrl: list[str] = url.split('/')
        downloadMangaData.source.chapter = splitUrl[4]
        downloadMangaData.source.manga = splitUrl[3]
    if (downloadMangaData.source.sourceType is SourcesEnum.MANGAREAD):
        splitUrl: list[str] = url.split('/')
        downloadMangaData.source.manga = splitUrl[4]
        downloadMangaData.source.chapter = splitUrl[5]
    downloadManga = DownloadManga(mangaData=downloadMangaData)
    downloadManga.execute()
    print("Download de {0} completo".format(downloadManga))
