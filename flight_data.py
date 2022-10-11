# This class is responsible for structuring the flight data


from datetime import date
from datetime import timedelta
from data_manager import DataManager
from notification_manager import NotificationManager
import requests


class FlightData:
    def __init__(self):
        self.datamanager = DataManager()
        self.notificationmanager = NotificationManager()
        self.price = 0
        self.price_len = 0
        self.price_list = []
        self.local_departure_list = []
        self.local_arrival_list = []
        self.min_value = None
        self.search_params = {}
        self.today = date.today()
        self.tomorrow = (self.today + timedelta(days=1)).strftime("%d/%m/%Y")
        self.sixmonthslater = (self.today + timedelta(days=60)).strftime("%d/%m/%Y")

    def get_search(self, departure_airport_code, start, city):
        url = self.datamanager.search_endpoint
        self.search_params = {
            "fly_from": "ESB",
            "fly_to": f"{departure_airport_code}",
            "date_from": f"{self.tomorrow}",
            "date_to": f"{self.sixmonthslater}",
            "flight_type": "oneway",
            "adults": 1,
            "curr": "GBP",
        }
        get_search = requests.get(url=url, headers=self.datamanager.location_header, params=self.search_params)
        get_search.raise_for_status()
        data = get_search.json()

        self.price_len = [item for item in data['data']]

        for n in range(len(self.price_len)):
            self.price_list.append(data['data'][n]['price'])
            self.local_departure_list.append(data['data'][n]['local_departure'].split("T")[0])
            self.local_arrival_list.append(data['data'][n]['local_arrival'].split("T")[0])
        self.price = min(self.price_list)
        self.min_value = self.price_list.index(self.price)
        url = f"{self.datamanager.sheety_put_endpoint}/{start}"
        response = requests.get(url=url)
        response.raise_for_status()
        getting = response.json()['sayfa1']['lowestPrice']
        if int(self.price) < int(getting):
            params = {
                "sayfa1": {
                    "lowestPrice": f"{self.price}"
                }
            }
            put = requests.put(url=url, json=params)
            put.raise_for_status()

# --------------------------------------If you want to send sms, you can activate it here.------------------------------------------
            # self.notificationmanager.send_message(self.price, city, departure_airport_code
            #                                       , self.local_departure_list[self.min_value]
            #                                       , self.local_arrival_list[self.min_value])

            self.notificationmanager.send_emails(self.min_value, self.price, city, departure_airport_code
                                                 , self.local_departure_list[self.min_value]
                                                 , self.local_arrival_list[self.min_value])

        elif self.price == getting:
            pass

        self.price_list = []
        self.local_departure_list = []
        self.local_arrival_list = []
