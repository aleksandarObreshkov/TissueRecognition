import tensorflow as tf


samples_dir = "C:\\Users\\aleks\\Projects\\Tissues\\IDC Breast Cancer Sorted"


def get_training_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rotation_range = 40, width_shift_range = 0.2, height_shift_range = 0.2, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True, rescale=1./255)
    training_data_gen = image_generator.flow_from_directory(directory=f"{samples_dir}\\train",
                                                            batch_size=20, 
                                                            shuffle=True, 
                                                            class_mode="binary",
                                                            target_size=(50, 50))
    return training_data_gen


def get_validation_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    validation_data_gen = image_generator.flow_from_directory(directory=f"{samples_dir}\\validate",
                                                            batch_size=20, 
                                                            shuffle=True, 
                                                            class_mode="binary",
                                                            target_size=(50, 50))
    return validation_data_gen


def get_test_dataset():
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    testing_data_gen = image_generator.flow_from_directory(directory=f"{samples_dir}\\test",
                                                            batch_size=20, 
                                                            shuffle=True,
                                                            class_mode="binary",
                                                            target_size=(50, 50))
    return testing_data_gen
