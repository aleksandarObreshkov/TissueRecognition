import time
import os


root_logdir = root_logdir = os.path.join(os.curdir, "logs/fit/")


def get_run_logdir():
    run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return os.path.join(root_logdir, run_id)
