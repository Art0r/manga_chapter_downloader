import os
import shutil
import requests
from tqdm import tqdm
from dataclasses import dataclass
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement


@dataclass
class DownloadMangaDataclass:
    URL: str = "https://po2scans.com"
    USER_FOLDER: str = os.path.expanduser('~')
    CHROMEDRIVER: str = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "chromedriver")
    LOCAL_DOWNLOADS: str = os.path.join(os.getcwd(), 'downloads')
    CHAPTERS_DESTINATION: str = os.path.join(USER_FOLDER, 'Documentos', 'mangás')


class DownloadManga:
    wait: WebDriverWait
    chapter_element: WebElement
    images_element: list[WebElement]
    title_element: WebElement
    title_text: str
    local_downloads_chapter: str
    chapters_destination_file: str

    def __init__(self, chapter_code: str) -> None:

        self._setup_selenium(chapter_code=chapter_code)
        self._get_elements()
        self._set_variables()
        self._handle_paths()

    def __str__(self) -> str:
        return self.title_text

    def execute(self):
        self.download_files()
        self.move_files_to_destination()

    def move_files_to_destination(self) -> None:

        shutil.make_archive(self.local_downloads_chapter, 'zip', self.local_downloads_chapter)
        shutil.move(self.local_downloads_chapter + '.zip', DownloadMangaDataclass.CHAPTERS_DESTINATION)

    def download_files(self) -> None:
        pbar = tqdm(enumerate(self.images_element), desc='Baixando arquivos',
                    ncols=len(self.images_element), ascii=True, unit='imagens')

        for index, image in pbar:
            src: str = image.get_attribute('src')
            try:
                res = requests.get(src, allow_redirects=True)
            except requests.exceptions.RequestException as e:
                print(e.args)
                exit()
            file = open(os.path.join(self.local_downloads_chapter, str(index) + '.png'), 'wb')
            file.write(res.content)
            file.close()

    def _handle_paths(self) -> None:
        if not os.path.isdir(DownloadMangaDataclass.LOCAL_DOWNLOADS):
            os.mkdir(DownloadMangaDataclass.LOCAL_DOWNLOADS)

        if os.path.isdir(self.local_downloads_chapter):
            shutil.rmtree(self.local_downloads_chapter)

        os.mkdir(self.local_downloads_chapter)

        if os.path.isfile(self.chapters_destination_file):
            os.remove(self.chapters_destination_file)

    def _set_variables(self) -> None:
        self.title_text = self.title_element.accessible_name + " - " + self.chapter_element.text.split('-')[0].strip()

        self.local_downloads_chapter = os.path.join(DownloadMangaDataclass.LOCAL_DOWNLOADS, self.title_text)
        self.chapters_destination_file = os.path.join(DownloadMangaDataclass.CHAPTERS_DESTINATION,
                                                      self.title_text + '.zip')

    def _get_elements(self) -> None:
        self.chapter_element: WebElement = self.wait.until(ec.presence_of_element_located(
            (By.XPATH, "//*[@class='chap-select']/option[@selected]")))
        self.images_element: list[WebElement] = self.wait.until(ec.presence_of_all_elements_located(
            (By.XPATH, "//*[@data-hash[contains(., 'page=')]]/img")))
        self.title_element: WebElement = self.wait.until(ec.presence_of_element_located(
            (By.XPATH, "//*[@class='series-title']")))

    def _setup_selenium(self, chapter_code: str) -> None:
        options = Options()
        # options.add_argument('--headless')
        service: Service = Service(executable_path=DownloadMangaDataclass.CHROMEDRIVER)
        driver: Chrome = Chrome(service=service, options=options)
        driver.get(DownloadMangaDataclass.URL + '/reader/' + chapter_code)
        driver.fullscreen_window()
        driver.execute_script("document.documentElement.requestFullscreen();")
        self.wait = WebDriverWait(driver, 10)
