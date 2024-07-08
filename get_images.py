import cv2
import random
from datetime import datetime
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from typing import List, Tuple


class GetImages:
    IMAGE_PATH = "./generated_images/"

    def __init__(self, number_of_epochs, batch_size, validation_split):
        self.number_of_images = 8
        self.width = 320
        self.height = 320
        self.image_size = (self.height, self.width)
        self.number_of_epochs = number_of_epochs
        self.batch_size = batch_size
        self.validation_split = validation_split
        self.train_model()

    @staticmethod
    def generate_circle_image(image_size, with_circle=True) -> np.array:
        img = np.zeros(image_size + (1,), dtype=np.uint8)
        if with_circle:
            center = (np.random.randint(10, image_size[0] - 10), np.random.randint(10, image_size[1] - 10))
            radius = np.random.randint(5, min(image_size) // 2)
            cv2.circle(img, center, radius, (255), -1)
        return img

    def loop(self, probability_of_circle) -> Tuple[List[str], str]:
        try:
            images_paths = []
            time_now = None
            for i in range(self.number_of_images):
                image_path = GetImages.IMAGE_PATH + f"{i}.png"
                random_number = random.randint(0, 100)
                if random_number < probability_of_circle:
                    image = self.generate_circle_image(self.image_size, with_circle=True)
                else:
                    image = self.generate_circle_image(self.image_size, with_circle=False)

                if self.predict_circle(image, self.image_size):
                    image = self.draw_green_circle(image)

                cv2.imwrite(image_path, image)
                now = datetime.now()
                time_now = now.strftime(f'd_%d_%m_t_%H_%M_%S')
                images_paths.append(image_path)

            return images_paths, time_now

        except Exception as ex:
            print(f"Got an error when generating the images: {type(ex)}: {ex}")

    def train_model(self):
        X, y = self.create_dataset(self.image_size)
        X = X / 255.0

        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.height, self.width, 1)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(1, activation='sigmoid')
        ])

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        print(f"NUmber of epochs: {self.number_of_epochs}")
        self.model.fit(X, y, epochs=self.number_of_epochs, batch_size=self.batch_size,
                       validation_split=self.validation_split)

        # Evaluate the model
        loss, accuracy = self.model.evaluate(X, y)
        print(f'Accuracy: {accuracy * 100:.2f}%')

    def create_dataset(self, image_size, num_samples=1000) -> Tuple[np.array, np.array]:
        X, y = [], []
        for _ in range(num_samples // 2):
            X.append(self.generate_circle_image(image_size, with_circle=True))
            y.append(1)
            X.append(self.generate_circle_image(image_size, with_circle=False))
            y.append(0)
        return np.array(X), np.array(y)

    def draw_green_circle(self, image) -> np.array:
        image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        center = (self.width - 10, self.height - 10)
        radius = 5
        color = (0, 255, 0)
        thickness = -1
        cv2.circle(image_bgr, center, radius, color, thickness)

        return image_bgr

    def predict_circle(self, img, image_size) -> bool:
        img = cv2.resize(img, image_size)
        img = img.reshape((1, self.height, self.width, 1)) / 255.0
        prediction = self.model.predict(img)
        return prediction[0][0] > 0.5
