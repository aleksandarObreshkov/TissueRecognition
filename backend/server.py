from flask import Flask, request, Response
import main
import os
import utils
import alexnet
from tensorflow import keras

app = Flask(__name__)
# add env reading and setting

alexnet_model: keras.models.Model

if alexnet.model_name not in os.listdir("C:\\Users\\aleks\\Projects\\IDC_Finder\\frontend\\dist\\server"):
    print("Creating Alexnet model")
    alexnet_model = alexnet.train_model()
else:
    print("Loading Alexnet from memory")
    alexnet_model = keras.models.load_model(f'C:\\Users\\aleks\\Projects\\IDC_Finder\\frontend\\dist\\server\\{alexnet.model_name}')

@app.route('/scan', methods=['POST'])
def scan_image():
    image_path = request.get_json()
    curr_scan_path = main.scan(image_path[0], alexnet_model)
    curr_scan_path = utils.extract_last_element_from_path(curr_scan_path)
    return Response(curr_scan_path)

 
app.run()