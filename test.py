import cv2
import numpy as np
from PIL import Image
import math


def stroke(origin_image, threshold, stroke_size, colors):
    img = np.array(origin_image)
    h, w, _ = img.shape
    padding = stroke_size + 1
    alpha = img[:,:,2]
    rgb_img = img[:,:,0:3]
    #Adds border to the image
    bigger_img = cv2.copyMakeBorder(rgb_img, padding, padding, padding, padding, 
                                        cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))

    alpha = cv2.copyMakeBorder(alpha, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=0)

    bigger_img = cv2.merge((bigger_img, alpha))

    h, w, _ = bigger_img.shape
    
    #Next two lines makes the image binary and inverts the values
    _, alpha_without_shadow = cv2.threshold(alpha, threshold, 255, cv2.THRESH_BINARY)  # threshold=0 in photoshop
    alpha_without_shadow = 255 - alpha_without_shadow
    
    #Applies the Eulerian distance transform
    dist = cv2.distanceTransform(alpha_without_shadow, cv2.DIST_L2, cv2.DIST_MASK_3)  # dist l1 : L1 , dist l2 : l2
    stroked = change_matrix(dist, stroke_size)

    stroke_alpha = (stroked * 255).astype(np.uint8) #the filter in binary

    stroke_b = np.full((h, w), colors[0][2], np.uint8)
    stroke_g = np.full((h, w), colors[0][1], np.uint8)
    stroke_r = np.full((h, w), colors[0][0], np.uint8)

    stroke = cv2.merge((stroke_b, stroke_g, stroke_r, stroke_alpha))

    stroke = cv2pil(stroke)
    bigger_img = cv2pil(bigger_img)

    result = Image.alpha_composite(stroke, bigger_img)
    return result

def change_matrix(input_mat, stroke_size):
    stroke_size = stroke_size - 1
    mat = np.ones(input_mat.shape)
    check_size = stroke_size + 1.0
    mat[input_mat > check_size] = 0
    border = (input_mat > stroke_size) & (input_mat <= check_size)
    mat[border] = 1.0 - (input_mat[border] - stroke_size)
    return mat

def cv2pil(cv_img):
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGBA)
    pil_img = Image.fromarray(cv_img.astype("uint8"))
    return pil_img
    
def merge_filters(original_image_path, filter_path):
    with Image.open(original_image_path) as original:
        original.load()
    with Image.open(filter_path) as filter:
        filter.load()
    output = stroke(filter, threshold=0, stroke_size=1, colors=((42,102,209),))
    original = cv2pil(np.array(original))

    h, w, _ = np.array(output).shape
    original = original.resize([w, h])

    trial = Image.alpha_composite(original, output)
    trial.save("C:\\Users\\aleks\\Desktop\\image\\testing\\result.png")
    trial.show()