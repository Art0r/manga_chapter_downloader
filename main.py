import requests
import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

root: str = "https://po2scans.com"
chapter_code: str = str(input("Cole aqui a código do capítulo:\n"))
manga_and_chapter: str = str(input("Digite o nome do mangá e o capítulo:\n"))

options = Options()
options.add_argument('--headless')
chromedriver_path: str = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "chromedriver")

service: Service = Service(executable_path=chromedriver_path)
driver: Chrome = Chrome(service=service, options=options)
driver.get(root + '/reader/' + chapter_code)

images: list[WebElement] = driver.find_elements(by='xpath', value='//*[@data-hash[contains(., "page=")]]/img')

for image in images:
    splitted_url: list[str] = image.get_attribute('src').rsplit('/', 6)
    page: str = splitted_url[6]
    src: str = image.get_attribute('src')
    res = requests.get(src, allow_redirects=True)
    if not os.path.isdir(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), manga_and_chapter)):
        os.mkdir(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), manga_and_chapter))
    file = open(os.path.join(manga_and_chapter, page), 'wb')
    file.write(res.content)
    file.close()
