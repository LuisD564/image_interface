import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from get_images import GetImages


class MLModel:
    NUMBER_OF_SAMPLES = 1000
    def __init__(self):
        self.image_getter = GetImages()
        self.model = None
        self.train_model()


    def train_model(self):
        X, y = self.create_dataset()
        self.model = self.create_cnn_model()
        self.model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)

        loss, accuracy = self.model.evaluate(X, y)
        print(f'Accuracy: {accuracy * 100:.2f}%')

    def create_dataset(self):
        X, y = self.image_getter.create_dataset(self.image_getter.width, self.image_getter.height,
                                                MLModel.NUMBER_OF_SAMPLES)
        X = X / 255.0
        return X, y

    @staticmethod
    def create_cnn_model():
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        return model

    def predict_circle(self, img):
        img = cv2.resize(img, (64, 64))
        img = img.reshape((1, 64, 64, 1)) / 255.0
        prediction = self.model.predict(img)
        return prediction[0][0] > 0.5


