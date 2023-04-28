import os
import requests
import shutil
from functions import get_elements, handle_paths
from tqdm import tqdm

url: str = "https://po2scans.com"
chapter_code: str = str(input("Cole aqui a código do capítulo:\n"))
chapter_path: str
destination_path: str

title_element, chapter_element, images_element = \
    get_elements(url=url, chapter_code=chapter_code)

title_text = title_element.accessible_name + " - " + chapter_element.text.split('-')[0].strip()
chapter_path, destination_path = handle_paths(title=title_text)

pbar = tqdm(enumerate(images_element), desc='Baixando arquivos',
            ncols=len(images_element), ascii=True, unit='imagens')

for index, image in pbar:
    split: list[str] = image.get_attribute('src').rsplit('/', 6)
    src: str = image.get_attribute('src')
    res = requests.get(src, allow_redirects=True)
    file = open(os.path.join(chapter_path, str(index) + '.png'), 'wb')
    file.write(res.content)
    file.close()

shutil.make_archive(chapter_path, 'zip', chapter_path)
shutil.move(chapter_path + '.zip', destination_path)
print("Finalizado")
