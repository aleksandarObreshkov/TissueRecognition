import threading
from os import curdir
from subprocess import run
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=2)

frontend_logs = open('../logs/frontend_logs.txt', 'w')
backend_logs = open('../logs/backend_logs.txt', 'w')

frontend = threading.Thread(target=run('electron .',shell=True, stdout=frontend_logs))
backend = threading.Thread(target=run('cd ../backend && python server.py',shell=True, stdout=backend_logs))
frontend.start()
backend.start()

frontend.join()
backend.join()


