import os
import shutil
import requests
import selenium.common
from tqdm import tqdm
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from src.DownloadMangaData import DownloadMangaData, SourcesEnum

class DownloadManga:
    wait: WebDriverWait
    images_element: list[WebElement]
    title_text: str
    local_downloads_chapter: str
    chapters_destination_file: str
    mangaData: DownloadMangaData

    def __init__(self, mangaData: DownloadMangaData) -> None:

        self.mangaData = mangaData
        self._setup_selenium()
        self._get_elements()
        self._set_variables()
        self._handle_paths()

    def __str__(self) -> str:
        return self.title_text

    def execute(self):
        self.download_files()
        self.move_files_to_destination()

    def move_files_to_destination(self) -> None:
        try:
            shutil.make_archive(self.local_downloads_chapter, 'zip', self.local_downloads_chapter)
            shutil.move(self.local_downloads_chapter + '.zip', self.chapters_destination_file)
        except FileNotFoundError or FileExistsError as e:
            print("Erro ao mover para os paths: {0}".format(e.args[0]))

    def download_files(self) -> None:
        pbar = tqdm(enumerate(self.images_element), desc='Baixando arquivos',
                    ncols=len(self.images_element), ascii=True, unit='imagens')

        for index, image in pbar:
            src: str = image.get_attribute('src')
            try:
                res = requests.get(src, allow_redirects=True)
            except requests.exceptions.RequestException as e:
                print("Erro ao fazer os downloads: {0}".format(e.args[0]))
                exit()
            extension: str = '.jpg'
            file = open(os.path.join(self.local_downloads_chapter, str(index) + extension), 'wb')
            file.write(res.content)
            file.close()

    def _handle_paths(self) -> None:
        try:
            if not os.path.isdir(self.mangaData.LOCAL_DOWNLOADS):
                os.mkdir(self.mangaData.LOCAL_DOWNLOADS)

            if not os.path.isdir(self.mangaData.CHAPTERS_DESTINATION):
                os.mkdir(self.mangaData.CHAPTERS_DESTINATION)

            if os.path.isdir(self.local_downloads_chapter):
                shutil.rmtree(self.local_downloads_chapter)

            os.mkdir(self.local_downloads_chapter)

            if os.path.isfile(self.chapters_destination_file):
                os.remove(self.chapters_destination_file)
        except FileNotFoundError or FileExistsError as e:
            print("Erro ao obter os paths: {0}".format(e.args[0]))
            exit()

    def _set_variables(self) -> None:
        try:
            self.local_downloads_chapter = os.path.join(self.mangaData.LOCAL_DOWNLOADS, self.title_text)
            self.chapters_destination_file = os.path.join(self.mangaData.CHAPTERS_DESTINATION,
                                                          self.title_text + '.zip')
        except FileNotFoundError or FileExistsError as e:
            print("Erro ao obter os paths: {0}".format(e.args[0]))
            exit()

    def _get_elements(self) -> None:
        try:
            if self.mangaData.source.sourceType is SourcesEnum.CHAPMANGANATO:
                self.images_element: list[WebElement] = self.wait.until(ec.presence_of_all_elements_located(
                    (By.XPATH, "//*[@class='container-chapter-reader']/img")))
            if self.mangaData.source.sourceType is SourcesEnum.MANGAREAD:
                self.images_element: list[WebElement] = self.wait.until(ec.presence_of_all_elements_located(
                    (By.XPATH, "//*[@class='reading-content']/div/img")))
                self.title_text = self.images_element[0].accessible_name.split("page")[0].strip()
                print(self.title_text)
        except selenium.common.exceptions.ElementNotVisibleException as e:
            print("Ocorreu um erro ao obter os elementos html: {0}".format(e.args[0]))
            exit()

    def _setup_selenium(self) -> None:
        try:
            options = Options()
            options.add_argument('--headless')
            service: Service = Service(executable_path=self.mangaData.CHROMEDRIVER)
            driver: Chrome = Chrome(service=service, options=options)
            if self.mangaData.source.sourceType is SourcesEnum.CHAPMANGANATO:
                full_url: str = self.mangaData.source.sourceType.value + self.mangaData.source.manga + "/" + self.mangaData.source.chapter
                driver.get(full_url)
            if self.mangaData.source.sourceType is SourcesEnum.MANGAREAD:
                full_url: str = self.mangaData.source.sourceType.value + "manga/" + self.mangaData.source.manga + "/" + self.mangaData.source.chapter
                driver.get(full_url)
            driver.fullscreen_window()
            driver.execute_script("document.documentElement.requestFullscreen();")
            print("Setup finalizado")
            self.wait = WebDriverWait(driver, 10)
        except selenium.common.exceptions.WebDriverException as e:
            print("Setup do Selenium falhou: {0}".format(e.args[0]))
            exit()
