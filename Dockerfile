FROM selenium/standalone-chrome:latest

FROM python:3.10

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

COPY requirements.txt /
RUN pip install -r /requirements.txt

EXPOSE 80

CMD ["gunicorn", "main:app"]