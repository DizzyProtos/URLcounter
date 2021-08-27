import logging
import requests
from django import db
from bs4 import BeautifulSoup
from bs4 import Tag
from urlcounter.models import url_model
import asyncio
import pandas as pd


def get_url_count_json(url_string):
    def get_tags_df(main_elem):
        nested_count = 0
        tags_df = pd.DataFrame({'Tag': [main_elem.name], 'Nested': [0], 'Count': [1]})
        for elem in main_elem.contents:
            if type(elem) is Tag:
                nested_tags_df = get_tags_df(elem)
                nested_count += nested_tags_df['Nested'].sum() + 1
                tags_df = tags_df.append(nested_tags_df)
        tags_df.iat[0, 1] = nested_count
        return tags_df
    try:
        html_response = requests.get(url_string)
    except Exception as e:
        logging.error(f'Error when accessing: {url_string}')
        logging.error(e)
        return '{}'
    document = BeautifulSoup(html_response.text, 'html.parser')

    doc_tags_df = get_tags_df(document)
    doc_tags_df = doc_tags_df[1:]  # remove first [document] tag
    doc_tags_df = doc_tags_df.groupby('Tag').sum()
    doc_tags_df = doc_tags_df.sort_values('Nested', ascending=False)
    return doc_tags_df.to_json(orient='index').strip()


def count_and_save_url(url_string, model_id):
    try:
        count_json = get_url_count_json(url_string)
    except Exception as e:
        logging.error(f'Error when counting url tags for {url_string}')
        logging.exception(e)
        count_json = '{}'
    model_to_save = url_model.objects.get(id=model_id)
    model_to_save.counted_json = count_json
    model_to_save.save()
    db.close_old_connections()


def start_url_counter(url_string: str, model_id: int):
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, count_and_save_url, url_string, model_id)
