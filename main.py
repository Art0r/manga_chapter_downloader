import datetime
import os
import shutil
import zipfile
from flask import Flask, request, Response, send_file, jsonify, make_response
from src.utils.config import AppConfig
from src.utils.download_from_source import Urls, downloadFromSource
from src.utils.zipping import zip_to_result
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

    try:

        body = request.get_json()

        urls = Urls(**body)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        final_file = os.path.join(os.getcwd(), f'result-{timestamp}{AppConfig.extension()}')

        downloadFromSource(urls=urls, i=len(urls.sources) - 1)
        
        response: Response = make_response()
        response.mimetype = 'application/zip'      

        response.headers["Content-Disposition"] = f"attachment; filename={final_file}"

        zip_to_result(final_file=final_file)

        with open(final_file, 'rb') as file:
            response.data = file.read()
            file.close()

        return response, 200
    
    except Exception as e:
        return jsonify(e.args), 500
    
    finally:
        if os.path.isfile(final_file):
            os.remove(final_file)
        if os.path.isdir(AppConfig.temp_folder()):
            shutil.rmtree(AppConfig.temp_folder())