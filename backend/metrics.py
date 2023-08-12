import time
import os
from tensorflow import keras


root_logdir = root_logdir = os.path.join(os.curdir, "logs/fit/")


def get_run_logdir():
    run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return os.path.join(root_logdir, run_id)

class accuracy_callback(keras.callbacks.Callback):
    def on_epoch_end(self,epoch,logs={}):
        if (logs.get("accuracy")>0.97):
            print("\nReached desired accuracy so stopping training")
            self.model.stop_training = True
