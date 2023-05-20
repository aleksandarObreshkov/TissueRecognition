import tensorflow as tf


dirs = ["ADI", "BACK", "DEB", "LYM", "MUC", "MUS", "NORM", "STR", "TUM"]


def get_training_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator()
    training_data_gen = image_generator.flow_from_directory(directory="TumorSamples/train",
                                                            batch_size=32, 
                                                            shuffle=True,
                                                            classes=dirs, 
                                                            class_mode="sparse")
    return training_data_gen


def get_validation_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator()
    validation_data_gen = image_generator.flow_from_directory(directory="TumorSamples/validate",
                                                            batch_size=32, 
                                                            shuffle=True,
                                                            classes=dirs, 
                                                            class_mode="sparse")
    return validation_data_gen


def get_test_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator()
    testing_data_gen = image_generator.flow_from_directory(directory="TumorSamples/test",
                                                            batch_size=32, 
                                                            shuffle=True,
                                                            classes=dirs,
                                                            class_mode="sparse")
    return testing_data_gen
