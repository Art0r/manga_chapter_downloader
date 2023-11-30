from src.DownloadManga import DownloadManga
from src.DownloadMangaData import DownloadMangaData, SourcesEnum
from src.utils.verify_source import verify_source

if __name__ == "__main__":
    url: str = str(input("Digite o código do capítulo:\n"))
    downloadMangaData = verify_source(url=url)
    if (downloadMangaData.sourceType is SourcesEnum.CHAPMANGANATO):
        splitUrl: list[str] = url.split('/')
        downloadMangaData.chapter = splitUrl[4]
        downloadMangaData.manga_title = splitUrl[3]
    if (downloadMangaData.sourceType is SourcesEnum.MANGAREAD):
        splitUrl: list[str] = url.split('/')
        downloadMangaData.chapter = splitUrl[5]
        downloadMangaData.manga_title = splitUrl[4]
    downloadManga = DownloadManga(mangaData=downloadMangaData)
    downloadManga.execute()
    print("Download de {0} completo".format(downloadManga))
