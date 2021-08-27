import json
import time
from django.test import TransactionTestCase, Client
from urlcounter.url_counter_service import get_url_count_json


class URLCountingTest(TransactionTestCase):
    correct_json = '{"html":{"Nested":49,"Count":1},"body":{"Nested":34,"Count":1},"ul":{"Nested":5,"Count":1},"head":{"Nested":3,"Count":1},"p":{"Nested":2,"Count":11},"header":{"Nested":2,"Count":1},"blockquote":{"Nested":1,"Count":1},"h2":{"Nested":0,"Count":6},"h3":{"Nested":0,"Count":2},"h1":{"Nested":0,"Count":1},"aside":{"Nested":0,"Count":1},"hr":{"Nested":0,"Count":1},"br":{"Nested":0,"Count":1},"li":{"Nested":0,"Count":5},"meta":{"Nested":0,"Count":2},"script":{"Nested":0,"Count":1},"strong":{"Nested":0,"Count":1},"title":{"Nested":0,"Count":1},"a":{"Nested":0,"Count":1}}'

    def test_correct_count(self):
        url = r'https://motherfuckingwebsite.com/'
        count_json = get_url_count_json(url)
        self.assertEqual(count_json, self.correct_json)

    def test_invalid_url(self):
        data = {"url": r'http://google,ro'}
        c = Client()
        response = c.post('/add', data=json.dumps(data), content_type='application/json')
        self.assertTrue('valid' in response.content.decode())

    def get_processing_result(self, client, url_id):
        while True:
            processed_response = client.get(f'/get/{url_id}')
            response_str = processed_response.content.decode()
            self.assertFalse('error' in response_str)
            if '{' not in response_str:
                time.sleep(5)
            else:
                break
        return response_str

    def test_url_processing(self):
        c = Client()
        response = c.post('/add', data='{"url": "https://motherfuckingwebsite.com/"}', content_type='application/json')
        url_id = int(response.content.decode())
        self.assertEqual(self.get_processing_result(c, url_id), self.correct_json)

        # Test if update will return the same result
        c.get(f'/update/{url_id}')
        update_result = self.get_processing_result(c, url_id)
        self.assertEqual(update_result, self.correct_json)
