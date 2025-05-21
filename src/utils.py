import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
from scipy.ndimage import label
from skimage.filters import threshold_otsu
import random
import os

def accuracy(prediction, maskfr):
    prediction = (prediction > 127).astype(np.uint8)
    maskfr = (maskfr > 127).astype(np.uint8)

    sM = np.sum(maskfr == 1)

    # Compute values
    TP = np.sum((prediction == 1) & (maskfr == 1)) 
    TN = np.sum((prediction == 0) & (maskfr == 0))
    FP = np.sum((prediction == 1) & (maskfr == 0))
    FN = np.sum((prediction == 0) & (maskfr == 1))

    total = prediction.size
    return FP / total, FN / total, TP / sM, TN / total

def DOSPredict(img_path) :
    img = cv2.imread(img_path)  
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = threshold_otsu(gray_image)*0.8
    bw_img1 = np.copy(gray_image)
    bw_img1[bw_img1 < thresh] = 0
    bw_img1[bw_img1 >= thresh] = 255
    img_eq = cv2.equalizeHist(img)
    thresh, bw_img = cv2.threshold(img_eq, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    thresh, _ = cv2.threshold(img_eq, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    adjusted_thresh = thresh + 120 # add some offset
    _, bw_img = cv2.threshold(img_eq, adjusted_thresh, 255, cv2.THRESH_BINARY)
    bw_img2 = cv2.dilate(bw_img, np.ones((6, 6), np.uint8), iterations=1)
    num_labels, labels = cv2.connectedComponents(bw_img2)

    clusters = []
    label_sizes = []
    for label in range(1, num_labels):
        ys, xs = np.where(labels == label)
        cluster = list(zip(xs, ys))
        clusters.append(cluster)
        label_sizes.append(len(cluster))
    sorted_indices = np.argsort(label_sizes)  # ascending
    try:
        second_largest_label = 1 + sorted_indices[-2]  
        labels_only_second = np.where(labels == second_largest_label, 255, 0).astype(np.uint8)
        binary_only_second_largest = labels_only_second
    except Exception as e:
        print(f"Error: {e} - {img_path}")
        return None
    

    return binary_only_second_largest