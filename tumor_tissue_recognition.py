import tensorflow as tf
import keras
import tf_records_repository as tf_repo
import os
import time
import sys

class_names = ["ADI", "BACK", "DEB", "LYM", "MUC", "MUS", "NORM", "STR", "TUM"]
model_name = "tissue_recogniser"
root_logdir = os.path.join(os.curdir, "logs/fit/")

#This method returns all images and all labels as a tuple, and we need to separate them into test and training data
def create_train_test_validation_dataset_arrays():
    (images_array,labels_array) = tf_repo.get_image_label_pairs_by_label(tf_repo.small_train_filename)

    train_images = []
    train_labels = []
    
    test_images = []
    test_labels = []

    validation_images = []
    validation_labels = []

    for images, labels in zip(images_array, labels_array):
        all_images_size = len(images)

        last_index_train = int(len(images)*0.7)
        train_images.extend(images[:last_index_train])
        train_labels.extend(labels[:last_index_train])
        
        last_index_test = int(len(images)*0.9)
        test_images.extend(images[last_index_train:last_index_test])
        test_labels.extend(labels[last_index_train:last_index_test])
        
        validation_images.extend(images[last_index_test:all_images_size-1])
        validation_labels.extend(labels[last_index_test:all_images_size-1])

    return (train_images, train_labels), (test_images, test_labels), (validation_images, validation_labels)


def get_datasets():
    (train_images, train_labels), (test_images, test_labels), (validation_images, validation_labels) = create_train_test_validation_dataset_arrays()

    train_ds = tf.data.Dataset.from_tensor_slices((train_images, train_labels))
    test_ds = tf.data.Dataset.from_tensor_slices((test_images, test_labels))
    validation_ds = tf.data.Dataset.from_tensor_slices((validation_images, validation_labels))

    train_ds_size = tf.data.experimental.cardinality(train_ds).numpy()
    test_ds_size = tf.data.experimental.cardinality(test_ds).numpy()
    validation_ds_size = tf.data.experimental.cardinality(validation_ds).numpy()
    print("Training data size:", train_ds_size)
    print("Test data size:", test_ds_size)
    print("Validation data size:", validation_ds_size)

    train_ds = (train_ds
                    .map(resize_images)
                    .shuffle(buffer_size=train_ds_size)
                    .batch(10, drop_remainder=True))
    test_ds = (test_ds
                    .map(resize_images)
                    .shuffle(buffer_size=test_ds_size)
                    .batch(10, drop_remainder=True))
    validation_ds = (validation_ds
                    .map(resize_images)
                    .shuffle(buffer_size=validation_ds_size)
                    .batch(10, drop_remainder=True))
    return (train_ds, test_ds, validation_ds) 


def resize_images(image, label):
    # Normalize images to have a mean of 0 and standard deviation of 1
    image = tf.image.per_image_standardization(image)
    image = tf.image.resize(image, (227, 227))
    return image, label


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


def get_run_logdir():
    run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return os.path.join(root_logdir, run_id)


def create_model():
    alexnet_model = get_alexnet_model()

    #alexnet_model.summary()
    alexnet_model.compile(loss='sparse_categorical_crossentropy', 
                        optimizer=tf.optimizers.SGD(learning_rate=0.001), 
                        metrics=['accuracy'])
    return alexnet_model
    

def load_model():
    return tf.keras.models.load_model(model_name)


def get_tensorboard_callback():
    run_logdir = get_run_logdir()
    return keras.callbacks.TensorBoard(run_logdir)


if __name__ == '__main__':
    tensorboard_callback = get_tensorboard_callback()
    alexnet_model: tf.keras.Model

    file_name = "STR-LTKLMSCL.tif.nii"
    record_filename = tf_repo.make_record_from_file(file_name)

    (image, label) = tf_repo.get_image_label_pairs_by_label(record_filename)
    file_dataset = tf.data.Dataset.from_tensor_slices((image, label))
    file_dataset = (file_dataset
                    .map(resize_images)
                    .batch(10, drop_remainder=True))

    if model_name not in os.listdir(os.curdir):
        (train_ds, test_ds, validation_ds) = get_datasets()
        alexnet_model = create_model()
        alexnet_model.fit(train_ds,
                    epochs=100,
                    validation_data=validation_ds,
                    validation_freq=1,
                    callbacks=[tensorboard_callback])

        alexnet_model.evaluate(test_ds)
        alexnet_model.save(model_name)

    else:
        alexnet_model = tf.keras.models.load_model(model_name)
    
    alexnet_model.evaluate(file_dataset)
