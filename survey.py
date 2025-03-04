import json
import streamlit as st
from managers.test_manager import test_manager
from managers.db_manager import db_manager


st.title('Survey on Human Recognizable Images in Image Classification')

PROFFESSION_LIST = [
    "Employed (Full-Time)",
    "Employed (Part-Time)",
    "Self-Employed / Freelancer",
    "Unemployed / Job Seeking",
    "Student",
    "Retired / Not in the Workforce"
]

if "email" not in st.session_state:
    st.session_state.email = ""
if "age" not in st.session_state:
    st.session_state.age = -1

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if "dataset" not in st.session_state:
    st.session_state.dataset = False

if "results" not in st.session_state:
    st.session_state.results = []

if "options" not in st.session_state:
    st.session_state.options = db_manager.get_options()

submit_button = False

if not st.session_state.form_submitted:
    with st.form(key='meta_form'):
        st.write('Please enter your name and age')
        st.write('If you want to stay anonymous, just click submit')
        age = st.number_input('Age', value=st.session_state.age)
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        job = st.selectbox("Profession", PROFFESSION_LIST)
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.session_state.form_submitted = True

if submit_button:
    st.session_state.age = age
    st.session_state.form_submitted = True
    st.session_state.gender = gender
    st.session_state.job = job
    print(st.session_state.email, st.session_state.age, st.session_state.form_submitted)
    st.rerun()

if st.session_state.form_submitted and not st.session_state.dataset:

    selected_data = st.selectbox('Select Dataset', st.session_state.options)
    dataset_selected = st.button('Select Dataset')
    if dataset_selected and selected_data in st.session_state.options:
        st.session_state.settings = db_manager.get_settings(selected_data)
        st.session_state.dataset = selected_data
        testManager = test_manager(st.session_state.settings, selected_data)
        st.session_state.results = [0 for i in range(st.session_state.settings["test_size"])]
        st.session_state.test_manager = testManager
        st.session_state.test = testManager.test
        st.session_state.examples_read = False
        st.rerun()
    else:
        st.error('Please select a dataset')

if st.session_state.dataset and not st.session_state.examples_read:
    test_manager.show_examples(st.session_state.test_manager)
    bt = st.button('Continue')
    if bt:
        st.session_state.examples_read = True
        st.rerun()

if st.session_state.dataset and st.session_state.examples_read:

    if "image_index" not in st.session_state:
        st.session_state.image_index = 0

    if st.session_state.image_index < st.session_state.settings["test_size"]:
        st.image(st.session_state.test[st.session_state.image_index]["image_path"], caption=f"Image {st.session_state.image_index + 1}", width=300)
        st.write("Please select the class of the image. If you are not certaion please select the option (Can't tell)")
        answer = st.segmented_control("Select the class of the image", st.session_state.test[st.session_state.image_index]["possible_classes"], selection_mode='single')
        previous = False
        if st.session_state.image_index > 0:
            previous = st.button('Previous Image')
        button_text = 'Submit' if st.session_state.image_index == st.session_state.settings["test_size"] - 1 else 'Next Image'
        selected = st.button(button_text)
        if selected:
            st.session_state.results[st.session_state.image_index] = answer
            st.session_state.image_index += 1
            st.rerun()
        if previous:
            st.session_state.image_index -= 1
            st.rerun()
    else:
        st.write("Thank you for submitting your information!")
        st.write("All images have been shown.")
        form = {'job': st.session_state.job, 'age': st.session_state.age, 'gender': st.session_state.gender}
        results = st.session_state.test_manager.save_result(st.session_state.results,form)
