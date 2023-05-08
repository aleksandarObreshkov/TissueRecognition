import tensorflow as tf
import tif_to_nii
import os
import SimpleITK as sitk

small_train_filepath = f'{os.curdir}/Tumor samples/train.tfrecords' # A smaller file

def get_all_nii_images() -> list[str]:
    all_filenames = []
    root_dir = tif_to_nii.nii_dir
    for dir in os.listdir(root_dir):
        for image in os.listdir(f'{root_dir}/{dir}'):
            all_filenames.append(f'{root_dir}/{dir}/{image}')
    return all_filenames


#get the first 500 of each type so that debugging is faster
def get_nii_images() -> list[str]:
    all_filenames = []
    counter = 0
    root_dir = tif_to_nii.nii_dir
    for dir in os.listdir(root_dir):
        for image in os.listdir(f'{root_dir}/{dir}'):
            counter += 1
            if(counter == 200): break
            all_filenames.append(f'{root_dir}/{dir}/{image}')
        counter = 0
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


def make_record():

    print("Starting saving of TFRecords...")

    # open the file
    writer = tf.io.TFRecordWriter(small_train_filepath)

    all_filenames = get_nii_images()

    # iterate through all .nii files:
    for meta_data in all_filenames:
        image_object = sitk.ReadImage(meta_data)

        # Load the image and label
        img = sitk.GetArrayFromImage(image_object)
        label = get_proper_label(meta_data)
        
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


def get_image_label_pairs_by_label() -> tuple[list[tf.io.FixedLenFeature], list[tf.io.FixedLenFeature]]:
    adi_images = []
    adi_labels = []

    back_images = []
    back_labels = []

    deb_images = []
    deb_labels = []

    lym_images = []
    lym_labels = []

    muc_images = []
    muc_labels = []

    mus_images = []
    mus_labels = []

    norm_images = []
    norm_labels = []

    str_images = []
    str_labels = []

    tum_images = []
    tum_labels = []

    for data in  tf.data.TFRecordDataset([small_train_filepath]).map(decode):
        label = data[1][0].numpy()
        print(label)
        match label:
            case 1:
                adi_images.append(data[0])
                adi_labels.append(data[1])
            case 2:
                back_images.append(data[0])
                back_labels.append(data[1])
            case 3:
                deb_images.append(data[0])
                deb_labels.append(data[1])
            case 4:
                lym_images.append(data[0])
                lym_labels.append(data[1])
            case 5:
                muc_images.append(data[0])
                muc_labels.append(data[1])
            case 6:
                mus_images.append(data[0])
                mus_labels.append(data[1])
            case 7:
                norm_images.append(data[0])
                norm_labels.append(data[1])
            case 8:
                str_images.append(data[0])
                str_labels.append(data[1])
            case 9:
                tum_images.append(data[0])
                tum_labels.append(data[1])

    # These arrays are stored into memory -> find a way to load this info directly into the model
    return ([adi_images, back_images, deb_images, lym_images, muc_images, mus_images, norm_images, str_images, tum_images],
    [adi_labels, back_labels, deb_labels, lym_labels, muc_labels, mus_labels, norm_labels, str_labels, tum_labels])

def decode_single(bytes):
    return tf.io.parse_single_example(
      # Data
      bytes,

      # Schema
     {'image': tf.io.FixedLenFeature([150528], tf.float32),
                  'label': tf.io.FixedLenFeature([1], tf.int64)}
  )

if __name__=="__main__":
    get_image_label_pairs_by_label()
    for batch in tf.data.TFRecordDataset([small_train_filepath]).map(decode_single):
        print(batch)