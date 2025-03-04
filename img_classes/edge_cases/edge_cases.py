from img_classes.img_interface import img_interface
import os
import json
SAVE_PATH = './img_classes/paths/'

class_name_dict = {
    "gtsrb": [
        "Speed limit (20km/h)",
        "Speed limit (30km/h)",
        "Speed limit (50km/h)",
        "Speed limit (60km/h)",
        "Speed limit (70km/h)",
        "Speed limit (80km/h)",
        "End of speed limit (80km/h)",
        "Speed limit (100km/h)",
        "Speed limit (120km/h)",
        "No passing",
        "No passing for vehicles over 3.5 metric tons",
        "Right-of-way at the next intersection",
        "Priority road",
        "Yield",
        "Stop",
        "No vehicles",
        "Vehicles over 3.5 metric tons prohibited",
        "No entry",
        "General caution",
        "Dangerous curve to the left",
        "Dangerous curve to the right",
        "Double curve",
        "Bumpy road",
        "Slippery road",
        "Road narrows on the right",
        "Road work",
        "Traffic signals",
        "Pedestrians",
        "Children crossing",
        "Bicycles crossing",
        "Beware of ice/snow",
        "Wild animals crossing",
        "End of all speed and passing limits",
        "Turn right ahead",
        "Turn left ahead",
        "Ahead only",
        "Go straight or right",
        "Go straight or left",
        "Keep right",
        "Keep left",
        "Roundabout mandatory",
        "End of no passing",
        "End of no passing by vehicles over 3.5 metric tons",
    ],
    "svhn": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "mnist": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}


class edge_cases(img_interface):
    def __init__(self, path, data_type='MNIST'):
        self.paths = {}
        self._data_type = data_type
        self._path = path
        self.get_data()

    def get_data(self):
        if not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)
            self._create_info()
            self._save_info()
        else:
            if not os.path.exists(os.path.join(SAVE_PATH, self._data_type + '.json')):
                self._create_info()
                self._save_info()
            else:
                self._read_info()

    def get_classes(self):
        if "mnist" in self._data_type.lower():
            return class_name_dict['mnist']
        elif "svhn" in self._data_type.lower():
            return class_name_dict['svhn']
        elif "gtsrb" in self._data_type.lower():
            return class_name_dict['gtsrb']
        else:
            raise ValueError("Invalid data type")

    def get_paths(self):
        return self.paths

    def _save_info(self):
        with open(os.path.join(SAVE_PATH, self._data_type + '.json'), 'w') as f:
            json.dump(self.paths, f)

    def _read_info(self):
        with open(os.path.join(SAVE_PATH, self._data_type + '.json'), 'r') as f:
            self.paths = json.load(f)

    def _create_info(self):
        for file in os.listdir(self._path):
            if file.endswith(".json") and file != 'examples.json':
                file_path = self._path + "/" + file
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    true_class = data['__gt_labels__'][0]['__gt_class__']
                    if true_class not in self.paths:
                        self.paths[true_class] = [file_path.replace('.json', '.png')]
                    else:
                        self.paths[true_class].append(file_path.replace('.json', '.png'))
