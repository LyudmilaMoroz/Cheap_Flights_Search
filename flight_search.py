import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
API_KEY = "xxx"


class FlightSearch:
    def get_iata_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        header = {"apikey": API_KEY}
        parameters = {
            "term": city_name,
            "locale": "en-US",
            "location_types": "city",
        }
        response = requests.get(url=location_endpoint, params=parameters, headers=header)
        location_list = response.json()["locations"]
        city_code = location_list[0]["code"]
        return city_code

    def check_flights(self, origin_city_code, destination_city_code, date_from, date_to, stop_overs):
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        header = {"apikey": API_KEY}
        parameters = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 14,
            "flight_type": "round",
            "max_stopovers": stop_overs,
            "curr": "EUR",
            "sort": "price"
        }
        response = requests.get(url=search_endpoint, params=parameters, headers=header)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"There are no direct flights to {destination_city_code} for your dates.")
            return None
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["cityFrom"],
                origin_airport=data["flyFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["flyTo"],
                out_date=data["local_departure"].split("T")[0],
                return_date=data["route"][-1]["local_departure"].split("T")[0],
                stop_overs = stop_overs,
                via_city = data["route"][0]["cityTo"],
                deep_link = data["deep_link"]
            )
            print(f"{flight_data.destination_city}: €{flight_data.price}")
            return flight_data




