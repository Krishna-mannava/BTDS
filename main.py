import tensorflow as tf
import cv2
import os
import numpy as np
import imutils
from keras.applications.vgg16 import preprocess_input
IMG_SIZE = (224,224)
def preprocess_imgs(set_name, img_size):
    """
    Resize and apply VGG-15 preprocessing
    """
    set_new = []
    for img in set_name:
        img = cv2.resize(
            img,
            dsize=img_size,
            interpolation=cv2.INTER_CUBIC
        )
# we use preprocess_input inorder to set the images to train the model  in keras
        set_new.append(preprocess_input(img))
    return np.array(set_new)
def crop_imgs(set_name, add_pixels_value=0):
    """
    Finds the extreme points on the image and crops the rectangular out of them
    """
    set_new = []
    for img in set_name:
#         cvtcolor for changing to gray images
# gaussian blur to make the surface smooth
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

#remove the noises by thresholding.......which seperates regions.. ....
#erode which makes partial '0' to full
# dilate which makes patial '1' to full
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours in thresholded image, then grab the largest one
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        # find the extreme points
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        ADD_PIXELS = add_pixels_value
        new_img = img[extTop[1]-ADD_PIXELS:extBot[1]+ADD_PIXELS, extLeft[0]-ADD_PIXELS:extRight[0]+ADD_PIXELS].copy()
        new_img = cv2.resize(new_img, IMG_SIZE)
        set_new.append(new_img)

    return np.array(set_new)


def load_data(dir_path):
    X = []
    labels = dict()       
    img = cv2.imread(dir_path)
    img = cv2.resize(img, IMG_SIZE)
    X.append(img)
#     print(f'{len(X)} images loaded from {dir_path} directory.')
    return X

def getPrediction(filename):

    model = tf.keras.models.load_model('u.h5')
    TRAIN_DIR = '../BTDS/static/'+filename
    print(TRAIN_DIR)
    u = load_data(TRAIN_DIR)
    u = crop_imgs(set_name=u)
    IMG_SIZE = (224,224)
    u = preprocess_imgs(set_name=u, img_size=IMG_SIZE)
    predictions = model.predict(u)
    for i in predictions:
        if i<0.5 and i>=0:
           k=str(np.round((1-i)*80.3,2))
           return 'Hurray!!!  No need to worry!',TRAIN_DIR,'You\'re chances of Not having Brain Tumor  is ' + k[1:len(k)-1] + '%'
        if(i<=1 and i>=0.5):
           k=str(np.round(i*80.3,2))
           return 'Oops !!!  I’m very sorry!!!',TRAIN_DIR,'You\'re chance of being affected by  Brain Tumor '+k[1:len(k)-1] + '%'