import cv2
from datetime import datetime
import numpy as np


class GetImages:
    IMAGE_PATH = "./generated_images/"

    def __init__(self):
        self.number_of_cameras = 8
        self.width = 1920
        self.height = 1080

    @staticmethod
    def generate_circle_image(width, height, with_circle=True):
        size = (height, width)
        img = np.zeros(size + (1,), dtype=np.uint8)
        if with_circle:
            center = (np.random.randint(10, size[0] - 10), np.random.randint(10, size[1] - 10))
            radius = np.random.randint(5, min(size) // 2)
            cv2.circle(img, center, radius, 255, -1)
        return img

    def create_dataset(self, width, height, num_samples=1000):
        X, y = [], []
        for _ in range(num_samples // 2):
            X.append(self.generate_circle_image(width, height, with_circle=True))
            y.append(1)
            X.append(self.generate_circle_image(width, height, with_circle=False))
            y.append(0)
        return np.array(X), np.array(y)

    def loop(self):
        try:
            images_paths = []
            time_now = None
            for i in range(self.number_of_cameras):
                image_path = GetImages.IMAGE_PATH + f"{i}.png"
                image = self.generate_circle_image(self.width, self.height, image_path)
                cv2.imwrite(image_path, image)
                now = datetime.now()
                time_now = now.strftime(f'd_%d_%m_t_%H_%M_%S')
                images_paths.append(image_path)

            return images_paths, time_now

        except Exception as ex:
            print(f"Got an error when generating the images: {type(ex)}: {ex}")
