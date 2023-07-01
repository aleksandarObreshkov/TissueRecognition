from flask import Flask, request, Response
import main
import os, signal
import utils
import alexnet
from tensorflow import keras
from threading import Thread
import requests

def close_app():
    process_id = os.getpid()
    os.kill(process_id, signal.SIGTERM) #find a better way to do this

def inform_ready():
    try:
        response = requests.post("http://127.0.0.1:5001/ready")
        if response.status_code!=200:
            raise ConnectionError(f"Status code was {response.status_code}, expected 200")
    except ConnectionRefusedError as cre:
        print(f"Connection error: {cre}")
        close_app()
    except Exception as err:
        print(f"Something went wrong: {err}")
        close_app()


running_scans = []

app = Flask(__name__)

alexnet_model: keras.models.Model

if alexnet.model_name not in os.listdir("C:\\Users\\aleks\\Projects\\IDC_Finder\\frontend\\dist\\server"):
    print("Creating Alexnet model")
    alexnet_model = alexnet.train_model()
else:
    print("Loading Alexnet from memory")
    alexnet_model = keras.models.load_model(f'C:\\Users\\aleks\\Projects\\IDC_Finder\\frontend\\dist\\server\\{alexnet.model_name}')

inform_ready()


@app.route('/scan', methods=['POST'])
def scan_image():
    image_path = request.get_json()
    original_image_path, curr_scan_dir = main.make_new_dir(image_path[0])
    curr_scan_path = utils.extract_last_element_from_path(curr_scan_dir)
    
    executor_thread = Thread(target=main.scan, args=(original_image_path, curr_scan_dir, alexnet_model))
    executor_thread.daemon = True
    running_scans.append(executor_thread)
    executor_thread.start()
    return Response(curr_scan_path, status=202)


@app.route('/quit', methods=['POST'])
def quit_app():
    close_app()
    

app.run()
    

