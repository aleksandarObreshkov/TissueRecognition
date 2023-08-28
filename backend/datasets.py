import tensorflow as tf


samples_dir = "C:\\Users\\aleks\\Projects\\Tissues\\IDC Breast Cancer Sorted Modified"


def get_training_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(horizontal_flip=True, vertical_flip=True, rotation_range=90)
    training_data_gen = image_generator.flow_from_directory(directory=f"{samples_dir}\\train",
                                                            batch_size=32, 
                                                            shuffle=True, 
                                                            class_mode="binary")
    return training_data_gen


def get_validation_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator()
    validation_data_gen = image_generator.flow_from_directory(directory=f"{samples_dir}\\validate",
                                                            batch_size=32, 
                                                            shuffle=True, 
                                                            class_mode="binary")
    return validation_data_gen


def get_test_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator()
    testing_data_gen = image_generator.flow_from_directory(directory=f"{samples_dir}\\test",
                                                            batch_size=32, 
                                                            shuffle=True,
                                                            class_mode="binary")
    return testing_data_gen
