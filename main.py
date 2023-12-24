import datetime
import os
import shutil
import zipfile
from flask import Flask, request, Response, send_file, jsonify, make_response
from src.utils.download_from_source import Urls, downloadFromSource
from src.utils.zipping import zip_to_result
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

    try:

        body = request.get_json()

        urls = Urls(**body)

        downloadFromSource(urls=urls, i=len(urls.sources) - 1)
        
        response: Response = make_response()
        response.mimetype = 'application/zip'      
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        final_file = os.path.join(os.getcwd(), f'result-{timestamp}.zip')

        response.headers["Content-Disposition"] = f"attachment; filename={final_file}"

        zip_to_result(final_file=final_file)

        with open(final_file, 'rb') as file:
            response.data = file.read()
            file.close()

        return response, 200
    
    except Exception as e:
        return jsonify(e.args[0]), 500
    
    finally:
        os.remove(final_file)
        shutil.rmtree(os.path.join(os.getcwd(), 'temp'))

if __name__ == "__main__":
    app.run(debug=True)