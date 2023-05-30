import os
import alexnet
from tensorflow import keras
import image_processing
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt


if __name__ == '__main__':
    alexnet_model: keras.models.Model

    if alexnet.model_name not in os.listdir(os.curdir):
        print("Creating Alexnet model")
        alexnet_model = alexnet.train_model()
    else:
        print("Loading Alexnet from memory")
        alexnet_model = keras.models.load_model(alexnet.model_name)

    image_path = "C:\\Users\\aleks\\Desktop\\image\\testing\\sample4.png"
    validated_image_path = "C:\\Users\\aleks\\Desktop\\image\\testing\\merged6.png"
    validated_img = image_processing.validate_large_image(alexnet_model, image_path, validated_image_path)
    print(validated_img.shape)
    print(validated_img[3].shape)
    dbscan = DBSCAN(eps=5, min_samples=4).fit(validated_img[0])
    labels = dbscan.labels_
    plt.scatter(validated_img[3][:, 0], validated_img[3][:,1], c = labels, cmap= "plasma") # plotting the clusters
    plt.xlabel("X") # X-axis label
    plt.ylabel("Y") # Y-axis label
    plt.show() # showing the plot

    