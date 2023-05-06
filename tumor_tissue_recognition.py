import tensorflow as tf
import keras
import dataset_service as datasets
import os
import metrics
import alexnet


if __name__ == '__main__':
    run_logdir = metrics.get_run_logdir()
    tensorboard_cb = keras.callbacks.TensorBoard(run_logdir)
    alexnet_model: tf.keras.Model
    (train_ds, test_ds, validation_ds) = datasets.get_datasets()

    if alexnet.model_name not in os.listdir(os.curdir):
        alexnet_model = alexnet.create_model()
        alexnet_model.fit(train_ds,
                    epochs=100,
                    validation_data=validation_ds,
                    validation_freq=1,
                    callbacks=[tensorboard_cb])
    else:
        alexnet_model = tf.keras.models.load_model(alexnet.model_name)
    
    alexnet_model.evaluate(test_ds)
    alexnet_model.save(alexnet.model_name)
