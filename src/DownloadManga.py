import os
import shutil
import requests
import selenium.common
import zipfile
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
    final_file_name: str
    mangaData: DownloadMangaData

    def __init__(self, mangaData: DownloadMangaData) -> None:

        self.mangaData = mangaData
        
        # setting .zip file name
        self.final_file_name = os.path.join(self.mangaData.LOCAL_DOWNLOADS, 
                                            self.mangaData.manga_title + '.zip')
        
        # setting up selenium elements, opening chrome and setting wait
        self._setup_selenium()

        # getting the html element from wich the images will be extracted
        self._get_elements()

        self._handle_paths()

    def execute(self):
        self.download_files()
        self.move_files_to_destination()

    def zip_folder(self, folder_path, zip_path):
        with zipfile.ZipFile(zip_path, 'w', allowZip64=True) as zipf:
            for foldername, subfolders, filenames in os.walk(folder_path):
                zipped_size = os.path.getsize(zip_path)
                if zipped_size >= self.get_total_size(folder_path):
                    break
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zipped_size = os.path.getsize(zip_path)
                    if zipped_size >= self.get_total_size(folder_path):
                        break
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)

    def get_total_size(self, folder_path):
        total_size = 0
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                total_size += os.path.getsize(file_path)
        return total_size

    def move_files_to_destination(self) -> None:
        try:
            self.zip_folder(
                folder_path=self.mangaData.LOCAL_DOWNLOADS,  
                zip_path=os.path.join(os.getcwd(), self.mangaData.manga_title + '.zip'))
            
            shutil.move(os.path.join(os.getcwd(), self.mangaData.manga_title + '.zip'), self.mangaData.CHAPTERS_DESTINATION)
        except FileNotFoundError or FileExistsError as e:
            print("Erro ao mover para os paths: {0}".format(e.args[0]))

    def download_files(self) -> None:
        # setting progress bar
        pbar = tqdm(enumerate(self.images_element), desc='Baixando arquivos',
                    ncols=len(self.images_element), ascii=True, unit='imagens')

        for index, image in pbar:
            # getting source from image
            src: str = image.get_attribute('src')
            try:
                res = requests.get(src, allow_redirects=True)
            except requests.exceptions.RequestException as e:
                print("Erro ao fazer os downloads: {0}".format(e.args[0]))
                exit()

            extension: str = '.jpg'
            file = open(os.path.join(self.mangaData.LOCAL_DOWNLOADS, str(index) + extension), 'wb')
            file.write(res.content)
            file.close()

    
    def _handle_paths(self) -> None:
        try:
            if not os.path.isdir(self.mangaData.LOCAL_DOWNLOADS):
                os.mkdir(self.mangaData.LOCAL_DOWNLOADS)

            if not os.path.isdir(self.mangaData.CHAPTERS_DESTINATION):
                os.mkdir(self.mangaData.CHAPTERS_DESTINATION)
        except FileNotFoundError or FileExistsError as e:
            print("Erro ao obter os paths: {0}".format(e.args[0]))
            exit()


    def _get_elements(self) -> None:
        try:
            # Only executed if url is from CHAPMANGANATO
            if self.mangaData.sourceType is SourcesEnum.CHAPMANGANATO:
                # Images from CHAPMANGANATO
                self.images_element: list[WebElement] = self.wait.until(ec.presence_of_all_elements_located(
                    (By.XPATH, "//*[@class='container-chapter-reader']/img")))
            
            # Only executed if url is from MANGAREAD
            if self.mangaData.sourceType is SourcesEnum.MANGAREAD:
                # Images from MANGAREAD
                self.images_element: list[WebElement] = self.wait.until(ec.presence_of_all_elements_located(
                    (By.XPATH, "//*[@class='reading-content']/div/img")))

                # Title manga from MANGAREAD
                # self.mangaData.manga_title = self.images_element[0].accessible_name.split("page")[0].strip()

        except selenium.common.exceptions.ElementNotVisibleException as e:
            print("Ocorreu um erro ao obter os elementos html: {0}".format(e.args[0]))
            exit()

    def _setup_selenium(self) -> None:
        try:
            options = Options()

            # This option will make chrome to execute without appearing
            # options.add_argument('--headless')

            service: Service = Service(executable_path=self.mangaData.CHROMEDRIVER)

            driver: Chrome = Chrome(service=service, options=options)

            # url to be executed by the driver, will be filled. If not raise exeception
            full_url: str = None 

            # Only executed if url is from CHAPMANGANATO
            if self.mangaData.sourceType is SourcesEnum.CHAPMANGANATO:
                full_url: str = self.mangaData.sourceType.value \
                    + self.mangaData.manga_title + "/" + self.mangaData.chapter
            
            # Only executed if url is from MANGAREAD
            if self.mangaData.sourceType is SourcesEnum.MANGAREAD:
                full_url: str = self.mangaData.sourceType.value + "manga/" \
                    + self.mangaData.manga_title + "/" + self.mangaData.chapter

            # raise exception if url is not currently supported
            if full_url is None:
                raise Exception({"err": "url not supported"})

            # executing url with driver
            driver.get(full_url)

            # setting fullscreen to avoid responsive divergences 
            driver.fullscreen_window()
            driver.execute_script("document.documentElement.requestFullscreen();")
            print("Setup finalizado")
            
            # setting how much time it should wait to the component to appear until timeout  
            self.wait = WebDriverWait(driver, 10)

        except selenium.common.exceptions.WebDriverException as e:
            print("Setup do Selenium falhou: {0}".format(e.args[0]))
            exit()
