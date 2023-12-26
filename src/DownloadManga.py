import os
import shutil
import requests
import selenium.common
import datetime
from tqdm import tqdm
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager import chrome
from src.utils.config import AppConfig
from src.utils.slugify import slugify
from src.DownloadMangaData import DownloadMangaData, SourcesEnum
from src.utils.zipping import zip_folder

class DownloadManga:
    wait: WebDriverWait
    images_element: list[WebElement]
    mangaData: DownloadMangaData

    def __init__(self, mangaData: DownloadMangaData) -> None:

        self.mangaData = mangaData
        
        # setting up selenium elements, opening chrome and setting wait
        self._setup_selenium()

        # getting the html element from wich the images will be extracted
        self._get_elements()

        # creating/removing folders to avoid path errors while processing files
        self._handle_paths()

    def execute(self):
        # fetch image resource from gotten from src then writtting it into a file 
        self.download_files()

        # zipping images into one file then moving it to its destination
        self.move_files_to_destination()

        # # wiping all the remaining data
        # self.clean_up()

    def clean_up(self):
        try:
            # removing folder and downloaded content
            shutil.rmtree(AppConfig.local_downloads())

        except OSError as e:
            print(f"Error: {AppConfig.local_downloads()} - {e}")


    def move_files_to_destination(self) -> None | str:

        self.mangaData.manga_title = slugify(self.mangaData.manga_title)

        # setting file destination 
        zip_file: str = os.path.join(AppConfig.temp_folder(), 
                                     f"{self.mangaData.manga_title}{AppConfig.extension()}")

        if os.path.isfile(zip_file): os.remove(zip_file)

        try:

            # zipping content from folder where the images were downloaded  
            zip_folder(
                folder_path=AppConfig.local_downloads(),  
                zip_path=zip_file)

            # wiping all the remaining data
            self.clean_up()
            
            return zip_file
        
        except FileNotFoundError or FileExistsError as e:
            print("Erro ao mover para os paths: {0}".format(e.args[0]))

    def download_files(self) -> None:

        # setting progress bar
        pbar = tqdm(enumerate(self.images_element), desc='Baixando arquivos',
                    ncols=len(self.images_element), ascii=True, unit='imagens')

        for index, image in pbar:
        
            # getting source from html current image element 
            src: str = image.get_attribute('src')
            try:

                # making request for image data
                res = requests.get(src, allow_redirects=True)

            except requests.exceptions.RequestException as e:
                print("Erro ao fazer os downloads: {0}".format(e.args[0]))
                exit()

            extension: str = '.jpg'
            
            # writing image data to file
            file = open(os.path.join(AppConfig.local_downloads(), str(index) + extension), 'wb')
            file.write(res.content)
            file.close()

    
    def _handle_paths(self) -> None:
        try:

            # To avoid errors with path, creating the local folder if not exists
            if not os.path.isdir(AppConfig.temp_folder()):
                os.mkdir(AppConfig.temp_folder())

            if not os.path.isdir(AppConfig.local_downloads()):
                os.mkdir(AppConfig.local_downloads())


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
                
                # Element from where we're extracting the title
                title_element: WebElement = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, "//*[@class='panel-chapter-info-top']/h1")))

                # Assigning title to its variable
                self.mangaData.manga_title = title_element.text
            
            # Only executed if url is from MANGAREAD
            if self.mangaData.sourceType is SourcesEnum.MANGAREAD:

                # Images from MANGAREAD
                self.images_element: list[WebElement] = self.wait.until(ec.presence_of_all_elements_located(
                    (By.XPATH, "//*[@class='reading-content']/div/img")))
                
                # Element from where we're extracting the title
                title_element: WebElement = self.wait.until(ec.presence_of_element_located(
                    (By.XPATH, "//*[@id='chapter-heading']")))

                # Assigning title to its variable
                self.mangaData.manga_title = title_element.text

                # Title manga from MANGAREAD
                # self.mangaData.manga_title = self.images_element[0].accessible_name.split("page")[0].strip()

        except selenium.common.exceptions.ElementNotVisibleException as e:
            print("Ocorreu um erro ao obter os elementos html: {0}".format(e.args[0]))
            exit()

    def _setup_selenium(self) -> None:
        try:
            options = Options()

            # This option will make chrome to execute without appearing
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            service: Service = Service(executable_path=chrome.ChromeDriverManager().install())

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
            if full_url is None or len(full_url) == 0:
                raise Exception("url not supported")
  
            # executing url with driver
            driver.get(full_url)

            # setting fullscreen to avoid responsive divergences 
            driver.fullscreen_window()
            driver.execute_script("document.documentElement.requestFullscreen();")
            print("Setup finalizado")

            # setting how much time it should wait to the component to appear until timeout  
            self.wait = WebDriverWait(driver, 10)

        except selenium.common.exceptions.WebDriverException as e:
            print("Setup do Selenium falhou: {0}".format(e.args))
            exit()
