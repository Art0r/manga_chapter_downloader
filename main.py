from src.DownloadManga import DownloadManga

if __name__ == "__main__":
    chapter_code: str = str(input("Digite o código do capítulo:\n"))
    downloadManga = DownloadManga(chapter_code=chapter_code)
    downloadManga.execute()
    print("Download de {0} completo".format(downloadManga))
