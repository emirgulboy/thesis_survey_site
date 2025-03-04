import os
import random
from zipfile import ZipFile
from img_classes.Fashion_MNIST.Fashion_MNIST import Fashion_MNIST
from img_classes.edge_cases.edge_cases import edge_cases
DATA_TYPES = {
    'Fashion-MNIST': Fashion_MNIST,
    'MNIST': edge_cases
}


class image_loader:
    def __init__(self, path, settings, data_type='Fashion-MNIST'):
        self.settings = settings
        self._path = path
        self.paths = {}
        self.unzip_images()
        self._load_paths(data_type)

    def _load_paths(self, data_type):
        try:
            load_class = DATA_TYPES[data_type]
        except KeyError:
            load_class = edge_cases
        loaded_class = load_class(self._path, data_type=data_type)
        self.paths = loaded_class.get_paths()
        self.classes  = loaded_class.get_classes()

    def get_image_set(self, size=None):
        if not size:
            size = len(self.paths.keys())
        return_list = []
        selected_list = []
        i = 0
        while i in range(size):
            random.seed()
            selected_class_idx = random.choice(range(len(self.paths)))
            selected_class = list(self.paths.keys())[selected_class_idx]
            selected_case_idx = random.choice(range(len(self.paths[selected_class])))
            selected_case = list(self.paths[selected_class])[selected_case_idx]
            if selected_case in selected_list:
                continue
            selected_list.append(selected_case)
            temp_dict = {
                'class_idx': selected_class_idx,
                'case_idx': selected_case_idx,
                'class': selected_class,
                'path': selected_case
            }
            return_list.append(temp_dict.copy())
            i += 1
        return return_list

    def get_classes(self):
        return self.classes

    def unzip_images(self):
        zip_file_location = os.path.join(self.settings['data_path'], 'images.zip')
        unzip_location = self.settings['data_path']
        with ZipFile(zip_file_location, 'r') as zip_ref:
            zip_ref.extractall(unzip_location)

if __name__ == '__main__':
    loader = image_loader('data/Fashion-MNIST')
    print(loader.get_image_set(5))
