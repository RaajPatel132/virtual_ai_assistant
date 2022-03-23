from typing import Counter
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import os

class Train:
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path

    def train(self):
        onlyfiles = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]

        # Create arrays for training data and labels
        Training_Data, Labels = [], []

        # Open training images in our datapath
        # Create a numpy array for training data
        for i, files in enumerate(onlyfiles):
            image_path = self.data_path + onlyfiles[i]
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)

        # Create a numpy array for both training data and labels
        Labels = np.asarray(Labels, dtype=np.int32)

        # Initialize facial recognizer
        model = cv2.face.LBPHFaceRecognizer_create()

        # NOTE: For OpenCV 3.0 use cv2.face.createLBPHFaceRecognizer()

        # Let's train our model
        model.train(np.asarray(Training_Data), np.asarray(Labels))

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

        model.save(f'{self.model_path}model.yml')

        print("Model trained sucessefully")