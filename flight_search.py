# This class is responsible for talking to the Flight Search API.

import requests
from data_manager import DataManager
from flight_data import FlightData


class FlightSearch(DataManager):
    def __init__(self):
        super().__init__()
        self.put_sheety_params = {}
        self.get_tequila_params = {}
        self.city = None
        self.iatacode = None
        self.start_for_loop = 0
        self.flightdata = FlightData()

    def control_iata_code(self):
        for self.start_for_loop in range(self.how_much):
            if self.preview[self.start_for_loop]['iataCode'] == '':
                self.city = self.preview[self.start_for_loop]['city'].lower()
                self.get_tequila_params = {
                    "term": f"{self.city}",
                    "location_types": "city",
                }
                get_data = requests.get(url=f"{self.location_endpoint}", headers=self.location_header
                                        , params=self.get_tequila_params)
                get_data.raise_for_status()
                self.iatacode = get_data.json()['locations'][0]['code']
                self.start_for_loop += 2
                self.put_sheety_params = {
                    'sayfa1': {
                        'iataCode': f'{self.iatacode}'
                    }
                }
                self.flightdata.get_search(self.iatacode, self.start_for_loop, self.city)
                url = f"{self.sheety_put_endpoint}/{self.start_for_loop}"
                response = requests.put(url=url, json=self.put_sheety_params)
                response.raise_for_status()
            else:
                self.start_for_loop += 2
                url = f"{self.sheety_get_endpoint}/{self.start_for_loop}"
                response = requests.get(url=url)
                response.raise_for_status()
                self.iatacode = response.json()['sayfa1']['iataCode']
                self.city = response.json()['sayfa1']['city']
                self.flightdata.get_search(self.iatacode, self.start_for_loop, self.city)
