import os
import requests
import shutil
from tqdm import tqdm
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

url: str = "https://po2scans.com"
chapter_code: str = "641f3b091cd8d"# str(input("Cole aqui a código do capítulo:\n"))
manga_and_chapter: str = "Versus - chapter 5"# str(input("Digite o nome do mangá e o capítulo:\n"))

DOWNLOADS_PATH: str = os.path.join(os.getcwd(), 'downloads')
CHAPTER_PATH: str = os.path.join(DOWNLOADS_PATH, manga_and_chapter)
USER_ROOT: str = os.path.expanduser('~')
MANGAS_ROOT: str = os.path.join(USER_ROOT, 'Documentos', 'mangás')

if not os.path.isdir(MANGAS_ROOT):
    os.mkdir(MANGAS_ROOT)

if not os.path.isdir(os.path.join(DOWNLOADS_PATH)):
    os.mkdir(os.path.join(DOWNLOADS_PATH))

if not os.path.isdir(CHAPTER_PATH):
    os.mkdir(CHAPTER_PATH)

options = Options()
options.add_argument('--headless')
chromedriver_path: str = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "chromedriver")

service: Service = Service(executable_path=chromedriver_path)
driver: Chrome = Chrome(service=service, options=options)
driver.get(url + '/reader/' + chapter_code)

title: WebElement = driver.find_element(by='xpath', value="//*[@class='chap-select']/option[@selected]")
images: list[WebElement] = driver.find_elements(by='xpath', value='//*[@data-hash[contains(., "page=")]]/img')

pbar = tqdm(enumerate(images), desc='Baixando arquivos',
            ncols=len(images), ascii=True, unit='imagens')

for index, image in pbar:
    split: list[str] = image.get_attribute('src').rsplit('/', 6)
    src: str = image.get_attribute('src')
    res = requests.get(src, allow_redirects=True)
    file = open(os.path.join(CHAPTER_PATH, str(index) + '.png'), 'wb')
    file.write(res.content)
    file.close()


shutil.make_archive(CHAPTER_PATH, 'zip', CHAPTER_PATH)
shutil.move(CHAPTER_PATH + '.zip', os.path.join(USER_ROOT, 'Documentos', 'mangás'))
