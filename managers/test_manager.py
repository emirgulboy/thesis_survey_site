from copy import deepcopy
import json
import random
import streamlit as st
from managers.image_manager import image_loader
from managers.db_manager import db_manager

class test_manager:
    def __init__(self, settings, selected_data="Fashion-MNIST"):
        self.email = ""
        self.age = -1
        self.form_submitted = False
        self.dataset = selected_data
        self.settings = settings
        self.images = image_loader(self.settings['data_path'], settings, selected_data)
        self.test_images = self.images.get_image_set(self.settings["test_size"])
        self.classes = self.images.get_classes()
        del self.images
        self._save_manager = db_manager()

    @property
    def test(self):
        random.seed()
        self._question_list = []
        for image in self.test_images:
            true_class = image['class']
            possible_classes = self.classes.copy()
            possible_classes.remove(true_class)
            possible_classes = random.sample(possible_classes, self.settings["select_out_of"]-1)
            possible_classes.append(true_class)
            random.shuffle(possible_classes)
            possible_classes.append("Can't tell")
            self._question_list.append({
                "image_path": image['path'],
                'true_class': true_class,
                'possible_classes': deepcopy(possible_classes)
            })
        return self._question_list

    def save_result(self, answers, form):
        self._results = self._question_list.copy()
        for i in range(len(answers)):
            answer = answers[i]
            self._results[i]['answer'] = answer
            if self._results[i]['true_class'] == answer:
                self._results[i]['correct'] = True
            else:
                self._results[i]['correct'] = False
        self._save_manager.save_to_db(self._results, form, self.dataset)

    def show_examples(self):
        st.title('Examples')
        st.write('These are the example images that you will be asked to classify')
        examples_json = st.session_state.settings['examples']
        with open(examples_json) as f:
            examples = json.load(f)
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        for example, comlumn in zip(examples, columns):
            label = examples[example]['gt_class']
            img_path = examples[example]['img_path']
            with comlumn:
                st.image(img_path, caption=label, width=300)
                st.write('Class: ', label)
