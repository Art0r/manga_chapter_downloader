import datetime
import os
import shutil
from flask import Flask, request, Response, send_file, jsonify
from src.utils.download_from_source import Urls, downloadFromSource
from src.utils.zipping import zip_folder

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

    try:

        body = request.get_json()

        urls = Urls(**body)

        files = downloadFromSource(urls=urls, i=len(urls.sources) - 1)

        result = f"result-{datetime.datetime.now()}"
        result_folder = os.path.join(os.getcwd(), result)

        if not os.path.isdir(result_folder):
            os.mkdir(result_folder)
            
        for file in files:
            
            shutil.move(file, result_folder)
            
        zipped_file = os.path.join(os.getcwd(), result) + ".zip"
        zip_folder(folder_path=result_folder, zip_path=zipped_file)

        return send_file(zipped_file), 200
    
    except Exception as e:
        return jsonify(e.args), 500
    
    finally:
        os.remove(zipped_file)
        shutil.rmtree(result_folder)
        shutil.rmtree(os.path.join(os.getcwd(), 'temp'))

if __name__ == '__main__':
    app.run(debug=True)
