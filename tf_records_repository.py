import tensorflow as tf
import tif_to_nii
import os
import SimpleITK as sitk


train_record_filename = f'{os.curdir}/records/training.tfrecords'
validation_record_filename = f'{os.curdir}/records/validate.tfrecords'
test_record_filename = f'{os.curdir}/records/test.tfrecords'


def get_all_nii_images(root_dir) -> list[str]:
    all_filenames = []
    for dir in os.listdir(root_dir):
        for image in os.listdir(f'{root_dir}/{dir}'):
            all_filenames.append(f'{root_dir}/{dir}/{image}')
    return all_filenames


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def get_proper_label(filename) -> int:
    label_map = {
        "ADI":1, 
        "BACK":2,
        "DEB":3,
        "LYM":4,
        "MUC":5,
        "MUS":6,
        "NORM":7,
        "STR":8,
        "TUM":9
    }

    for key, value in label_map.items():
        if key in filename:
            return value
    return -1


def make_record(all_filenames, record_path):

    print(f"Starting saving of TFRecord at '{record_path}'")

    # open the file
    writer = tf.io.TFRecordWriter(record_path)

    # iterate through all .nii files:
    for filename in all_filenames:
        image_object = sitk.ReadImage(filename)

        # Load the image and label
        img = sitk.GetArrayFromImage(image_object)
        label = get_proper_label(filename)
        
        # Create a feature
        feature = {'label': _int64_feature(label),
                'image': _float_feature(img.ravel())}
                
        # Create an example protocol buffer
        example = tf.train.Example(features=tf.train.Features(feature=feature))

        # Serialize to string and write on the file
        writer.write(example.SerializeToString())
        
    writer.close()


def decode(serialized_example) -> tuple[tf.io.FixedLenFeature, tf.io.FixedLenFeature]:
    features = tf.io.parse_single_example(
        serialized_example,
        features={'image': tf.io.FixedLenFeature([150528], tf.float32),
                  'label': tf.io.FixedLenFeature([1], tf.int64)})

    features['image'] = tf.reshape(features['image'], [224, 224, 3])

    # NOTE: No need to cast these features, as they are already `tf.float32` values.
    return features['image'], features['label']


def resize_images(image, label):
    # Normalize images to have a mean of 0 and standard deviation of 1
    image = tf.image.per_image_standardization(image)
    image = tf.image.resize(image, (227, 227))
    return image, label


def get_training_dataset():
    return tf.data.TFRecordDataset([train_record_filename]).map(decode).map(resize_images).batch(10, drop_remainder=True)


def get_validation_dataset():
    return tf.data.TFRecordDataset([validation_record_filename]).map(decode).map(resize_images).batch(10, drop_remainder=True)


def get_test_dataset():
    return tf.data.TFRecordDataset([test_record_filename]).map(decode).map(resize_images).batch(10, drop_remainder=True)


# if __name__=="__main__":
  
#     train_path = f'{os.curdir}/records/train'
#     train_filenames = get_all_nii_images(train_path)
#     make_record(train_filenames, train_record_filename)

#     validation_path = f'{os.curdir}/records/validate'
#     validation_filenames = get_all_nii_images(validation_path)
#     make_record(validation_filenames, validation_record_filename)

#     test_path = f'{os.curdir}/records/test'
#     test_filenames = get_all_nii_images(test_path)
#     make_record(test_filenames, test_record_filename)