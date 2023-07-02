import requests
import utils

FRONTEND_URL = "http://127.0.0.1:5001"


def inform_ready(url, body_json, expected_status):
    try:
        response = requests.post(url, json=body_json)
        if response.status_code != expected_status:
            raise ConnectionError(f"Status code was {response.status_code}, expected {expected_status}")
        
    except ConnectionRefusedError as cre:
        print(f"Connection error: {cre}")
        utils.close_app()

    except Exception as err:
        print(f"Something went wrong: {err}")
        utils.close_app()


def inform_server_ready():
    inform_ready(f"{FRONTEND_URL}/ready", None, 200)


def inform_scan_ready(scan):
    scan = {'completedScan':scan}
    inform_ready(f"{FRONTEND_URL}/update", scan, 200)
