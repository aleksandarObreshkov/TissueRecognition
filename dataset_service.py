import tensorflow as tf
import tf_records_repository as tf_repo


#This method returns all images and all labels as a tuple, and we need to separate them into test and training data
def create_train_test_validation_dataset_arrays() -> tuple[tuple[list, list], tuple[list, list], tuple[list, list]]:
    (images_array,labels_array) = tf_repo.get_image_label_pairs_by_label()

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
        
        validation_images.extend(images[last_index_test:all_images_size-1]) #was -30
        validation_labels.extend(labels[last_index_test:all_images_size-1]) #was -30

    return (train_images, train_labels), (test_images, test_labels), (validation_images, validation_labels)


def get_datasets() -> tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
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