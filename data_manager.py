import requests
import os


class DataManager:
    def __init__(self):
        self.sheety_get_endpoint = os.environ['self.sheety_get_endpoint']
        self.sheety_put_endpoint = os.environ['self.sheety_put_endpoint']
        self.sheety_users_put_get_endpoint = os.environ['self.sheety_users_put_get_endpoint']
        self.location_endpoint = os.environ['self.location_endpoint']
        self.search_endpoint = os.environ['self.search_endpoint']
        self.location_header = {
            "apikey": os.environ['"apikey"']
        }

        self.sheety_get = requests.get(url=self.sheety_get_endpoint)
        self.sheety_get.raise_for_status()
        self.page_data = self.sheety_get.json()
        self.preview = [item for item in self.page_data['sayfa1']]
        self.how_much = len(self.preview)
