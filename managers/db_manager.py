
import json
import supabase
import streamlit as st


class db_manager:
    def __init__(self):
        self.__url = st.secrets['url']
        self.__key = st.secrets['authtoken']
        return

    def save_to_db(self, return_data, session_data, dataset):
        self.parse_return(return_data, session_data)
       
        supabase_client = supabase.create_client(self.__url, self.__key)

        response = supabase_client.table('session_data').insert({"dataset": dataset, "session_details": self._parsed}).execute()

    def save_to_file(self, return_data):
        with open('results.jsonl', 'a') as f:
            f.write(json.dumps(return_data) + '\n')

    def parse_return(self, return_data, session_data):
        self._parsed = {}
        self._parsed['session_data'] = session_data
        self._parsed['results'] = return_data
        return

    @staticmethod
    def get_settings(dataset):
        url = st.secrets['url']
        key = st.secrets['authtoken']
        supabase_client = supabase.create_client(url, key)
        response = supabase_client.table('settings').select().eq('name', dataset).execute()
        return response.data[0]['json']

    @staticmethod
    def get_options():
        url = st.secrets['url']
        key = st.secrets['authtoken']
        supabase_client = supabase.create_client(url, key)
        response = supabase_client.table('settings').select('name').eq('Enable', True).execute()
        return [x['name'] for x in response.data]
