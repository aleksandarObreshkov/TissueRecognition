from flask import Flask, request, Response
import main
import utils

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_image():
    image_path = request.get_json()
    curr_scan_path = main.scan(image_path[0])
    curr_scan_path = utils.extract_last_element_from_path(curr_scan_path)
    return Response(curr_scan_path)

 
app.run()