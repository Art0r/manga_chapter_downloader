from flask import Flask, request, Response
from src.utils.download_from_source import Urls, downloadFromSource

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

    body = request.get_json()

    urls = Urls(**body)

    downloadFromSource(urls=urls, i=len(urls.sources) - 1)

    return Response(status=204)

if __name__ == '__main__':
    app.run(debug=True)
