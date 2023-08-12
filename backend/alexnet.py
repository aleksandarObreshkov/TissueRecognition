from tensorflow import keras
import datasets
import metrics
from os import listdir

model_name = "tissue_recogniser_idc"


def get_alexnet_network_model():
    return keras.models.Sequential([
        keras.layers.Resizing(50, 50),
        keras.layers.Rescaling(1./255),

        keras.layers.Conv2D(filters=96, kernel_size=(5,5), strides=(2,2), activation='relu', data_format="channels_last"),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),

        keras.layers.Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), activation='relu', padding="same", data_format="channels_last"),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),

        keras.layers.Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same", data_format="channels_last"),
        keras.layers.BatchNormalization(),

        keras.layers.Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same", data_format="channels_last"),
        keras.layers.BatchNormalization(),

        keras.layers.Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same", data_format="channels_last"),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),

        keras.layers.Flatten(),

        keras.layers.Dense(2048, activation='relu'),
        keras.layers.Dropout(0.5),

        keras.layers.Dense(2048, activation='relu'),
        keras.layers.Dropout(0.5),

        keras.layers.Dense(1, activation='sigmoid')
    ])


def create_model():
    alexnet_model = get_alexnet_network_model()
    alexnet_model.build((1, 50, 50, 3))
    alexnet_model.summary()
    alexnet_model.compile(loss='binary_crossentropy', 
                        optimizer=keras.optimizers.Adam(learning_rate=0.001), 
                        metrics=['accuracy'])
    
    return alexnet_model
    

def load_model():
    return keras.models.load_model(model_name)


def train_model():
    run_logdir = metrics.get_run_logdir()
    tensorboard_cb = keras.callbacks.TensorBoard(run_logdir)
    callback = metrics.accuracy_callback()

    alexnet_model = create_model()
    alexnet_model.fit(datasets.get_training_dataset(),
                epochs=100,
                validation_data=datasets.get_validation_dataset(),
                validation_freq=1,
                callbacks=[callback, tensorboard_cb])
    alexnet_model.evaluate(datasets.get_test_dataset())
    alexnet_model.save(model_name)
    return alexnet_model


def get_alexnet_model(cnn_model_name):
    m: keras.models.Model
    if cnn_model_name not in listdir("C:\\Users\\aleks\\Projects\\IDC_Finder\\frontend\\dist\\server"):
        print("Creating Alexnet model")
        m = train_model()
    else:
        print("Loading Alexnet from memory")
        m = keras.models.load_model(f'C:\\Users\\aleks\\Projects\\IDC_Finder\\frontend\\dist\\server\\{cnn_model_name}')
    return m