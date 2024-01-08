import asyncio
from src.DownloadManga import DownloadManga
from src.DownloadMangaData import SourcesEnum
from src.utils.verify_source import verify_source


class Urls:
    sources: list[str]

    def __init__(self, sources: list[str]) -> None:
        self.sources = sources


def downloadFromSource(urls: Urls, i: int):
    if i < 0:
        return

    thisSource = urls.sources[i]
    downloadMangaData = verify_source(url=thisSource)
    if (downloadMangaData.sourceType is SourcesEnum.MANGAREAD):
        splitUrl: list[str] = thisSource.split('/')
        downloadMangaData.chapter = splitUrl[5]
        downloadMangaData.manga_title = splitUrl[4]

    downloadManga = DownloadManga(mangaData=downloadMangaData)

    asyncio.run(downloadManga.setup())
    asyncio.run(downloadManga.execute())

    return downloadFromSource(urls=urls, i=i - 1)
