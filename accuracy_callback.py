import tensorflow as tf

class accuracy_callback(tf.keras.callbacks.Callback):
    def on_epoch_end(self,epoch,logs={}):
        if (logs.get("accuracy")>0.90):
            print("\nReached desired accuracy so stopping training")
            self.model.stop_training =True
