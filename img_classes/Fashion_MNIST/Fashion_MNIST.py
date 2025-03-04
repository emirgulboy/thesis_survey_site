import os
# from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from PIL import Image
import numpy as np
from img_classes.img_interface import img_interface


class Fashion_MNIST(img_interface):
    def __init__(self, path):
        self.test_paths = {}
        self.train_paths = {}
        self._path = path
        self.get_data()

    def get_data(self):
        for folder in os.listdir(self._path):
            if os.path.isdir(os.path.join(self._path, folder)):
                if 'train' in folder:
                    self.train_paths = self._load_classes(os.path.join(self._path, folder))
                elif 'test' in folder:
                    self.test_paths = self._load_classes(os.path.join(self._path, folder))

    def _load_classes(self, folder):
        classes = {}
        for cls in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, cls)):
                for img in os.listdir(os.path.join(folder, cls)):
                    if cls not in classes:
                        classes[cls] = []
                    classes[cls].append(os.path.join(folder, cls, img))
        return classes

    def get_classes(self):
        return list(self.test_paths.keys())

    def get_paths(self):
        return self.test_paths

    def set_up_dir(self, enable_training=False):
        # if not any(file.endswith('.csv') for file in os.listdir('data/mnist')):
            # api = KaggleApi()
            # api.authenticate()
            # Download the MNIST dataset
            # api.dataset_download_files('zalando-research/fashionmnist', path='data/mnist', unzip=True)

        # Create directories for each class
        types = ['train', 'test']
        classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for cls in classes:
            for t in types:
                os.makedirs(os.path.join('data/mnist', t, cls), exist_ok=True)

        # Move images to respective class directories
        for file_name in os.listdir('data/mnist'):
            if file_name.endswith('.csv'):
                label = file_name.split('_')[1].split('.')[0]
                if 'train' in file_name:
                    folder = 'train'
                else:
                    folder = 'test'
                    if not enable_training:
                        continue
                df = pd.read_csv(os.path.join('data/mnist', file_name))
                for index, row in df.iterrows():
                        label = str(row[0])
                        image_array = np.array(row[1:]).reshape(28, 28).astype(np.uint8)
                        image = Image.fromarray(image_array)
                        image.save(os.path.join("data\\Fashion-MNIST", folder, label, f'{index}.png'))
