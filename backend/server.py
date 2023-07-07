from flask import Flask, request, Response
import main
import alexnet
import server_utils
import utils

server = Flask(__name__)
alexnet_model = alexnet.get_alexnet_model(alexnet.model_name)


@server.route('/scan', methods=['POST'])
def scan_image():
    try:
        image_path = request.get_json()
        original_image_path, curr_scan_dir = utils.make_new_dir_from_path(image_path[0])
        curr_scan_path = utils.extract_last_element_from_path(curr_scan_dir)
        main.start_scan_in_thread(original_image_path, curr_scan_dir, alexnet_model)
        return Response(curr_scan_path, status=201)
    except RuntimeError as err:
        print(f'Error ocurred while scanning the image: {err}')
        return Response(curr_scan_path, status=500)


@server.route('/quit', methods=['POST'])
def quit_app():
    utils.close_app()
    

server_utils.inform_server_ready()
server.run()
    

