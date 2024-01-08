# MANGA CHAPTER DOWNLOADER

## Install/Running
### Building docker image
> docker build -t art0r/manga_chapter_downloader:prod-main .

### Running docker image
>docker run \
        -p 8000:80 \
        -e FLASK_ENV=production \
        art0r/manga_chapter_downloader:prod-main

### Downloading file moving to destination
> curl -o response.zip 'http://127.0.0.1:8000/' \
--header 'Content-Type: application/json' \
--data '{
    "sources": [ < urls > ]
}' && mv ./response.zip  /mnt/c/arthu/Documents

## About
> This is a tool written in python using selenium to identify and 
download images from a website then join into a zip file
to be easier to send to kindle. The source used is: [po2scans](https://po2scans.com/).

>Please visit the original website and more than that, if you can and
if is available in your country, <b>support the author</b> buying the
<b>licensed material</b>. And please <b>do not upload the downloaded files
to other website</b>.

## Environment
- Chromedriver version: 112.0.5615.49
- Windows 11 (without WSL)
- Python 3.10.10
- Libs and its versions are described in <b>requirements.txt</b>

## What do we have for now?
> It can download the chapter images locally then zip the folder
and then move zip file to Documentos/mangás (Windows path). For
now the only source is [po2scans](https://po2scans.com/)
