import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_elements(url: str, chapter_code: str) -> (WebElement, WebElement, WebElement):
    wait = _setup_selenium(url=url, chapter_code=chapter_code)
    chapter_element: WebElement = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[@class='chap-select']/option[@selected]")))
    images_element: list[WebElement] = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//*[@data-hash[contains(., 'page=')]]/img")))
    title_element: WebElement = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[@class='series-title']")))
    return title_element, chapter_element, images_element


def _setup_selenium(url: str, chapter_code: str) -> WebDriverWait:
    options = Options()
    # options.add_argument('--headless')
    chromedriver_path: str = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "chromedriver")

    service: Service = Service(executable_path=chromedriver_path)
    driver: Chrome = Chrome(service=service, options=options)
    driver.get(url + '/reader/' + chapter_code)
    driver.fullscreen_window()
    driver.execute_script("document.documentElement.requestFullscreen();")
    wait = WebDriverWait(driver, 10)
    return wait


def handle_paths(title: str) -> (str, str):
    user_root: str = os.path.expanduser('~')
    downloads_path: str = os.path.join(os.getcwd(), 'downloads')
    mangas_path: str = os.path.join(user_root, 'Documentos', 'mangás')
    destination_path: str = os.path.join(user_root, 'Documentos', 'mangás')

    if not os.path.isdir(mangas_path):
        os.mkdir(mangas_path)

    if not os.path.isdir(os.path.join(downloads_path)):
        os.mkdir(os.path.join(downloads_path))

    if not os.path.isdir(title):
        os.mkdir(title)

    return os.path.join(downloads_path, title), destination_path
