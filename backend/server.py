from flask import Flask, request, Response
import main
import alexnet
import server_utils
import utils

server = Flask(__name__)
alexnet_model = alexnet.get_alexnet_model(alexnet.model_name)


@server.route('/scan', methods=['POST'])
def scan_image():
    image_path = request.get_json()
    curr_scan_path = main.start_scan(image_path[0], alexnet_model)
    return Response(curr_scan_path, status=201)


@server.route('/quit', methods=['POST'])
def quit_app():
    utils.close_app()
    

server_utils.inform_server_ready()
server.run()
    

