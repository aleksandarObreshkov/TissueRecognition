from flask import Flask, request, Response
import main
import json

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_image():
    image_path = request.get_json()
    curr_scan_path = main.scan(image_path[0])
    curr_scan_path = curr_scan_path.split("\\")
    curr_scan_path = curr_scan_path[len(curr_scan_path)-1]
    return Response(curr_scan_path)

 
app.run()