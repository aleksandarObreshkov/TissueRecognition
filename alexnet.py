import tensorflow as tf
from tensorflow import keras
import tf_records_repository as tf_repo
import metrics


model_name = "tissue_recogniser_1"


def get_alexnet_model():
    return keras.models.Sequential([
        keras.layers.Conv2D(filters=96, kernel_size=(11,11), strides=(4,4), activation='relu', input_shape=(227,227,3)),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
        keras.layers.Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), activation='relu', padding="same"),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
        keras.layers.Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
        keras.layers.BatchNormalization(),
        keras.layers.Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
        keras.layers.BatchNormalization(),
        keras.layers.Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
        keras.layers.Flatten(),
        keras.layers.Dense(4096, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(4096, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(10, activation='softmax')
    ])


def create_model():
    alexnet_model = get_alexnet_model()

    alexnet_model.summary()
    alexnet_model.compile(loss='sparse_categorical_crossentropy', 
                        optimizer=tf.optimizers.SGD(learning_rate=0.001), 
                        metrics=['accuracy'])
    return alexnet_model
    

def load_model():
    return keras.models.load_model(model_name)


def train_model():
    run_logdir = metrics.get_run_logdir()
    tensorboard_cb = keras.callbacks.TensorBoard(run_logdir)

    alexnet_model = create_model()
    alexnet_model.fit(tf_repo.get_training_dataset(),
                epochs=100,
                validation_data=tf_repo.get_validation_dataset(),
                validation_freq=1,
                callbacks=[tensorboard_cb])
    alexnet_model.evaluate(tf_repo.get_test_dataset())
    alexnet_model.save(model_name)
    return alexnet_model
