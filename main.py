# __________ Asking user data __________ #

print("Welcome to Liudmila's Flight Club!")
print("We find the best flight deals and email you.")

# __________ Main code to search flight and send message __________ #
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import datetime

ORIGINAL_CITY = "HEL"

data_manager = DataManager()
sheety_data = data_manager.get_destination_data()
flight_search = FlightSearch()
sms = NotificationManager()
users_data = data_manager.get_users_data()

# __________ Sending user data to sheety __________ #
data_manager.add_user()

# __________ Adding airport code to sheety __________ #
if sheety_data[0]["iataCode"] == "":
    for row in sheety_data:
        city = row["city"]
        row["iataCode"] = flight_search.get_iata_code(city)
        data_manager.destination_data = sheety_data
        data_manager.add_iata_code()

# __________ Searching for flights __________ #
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
six_month_from_now = datetime.date.today() + datetime.timedelta(days=180)

for destination in sheety_data:
    flights = flight_search.check_flights(ORIGINAL_CITY, destination["iataCode"],
                                          date_from=tomorrow, date_to=six_month_from_now, stop_overs=0)
    if flights is None:
        print("Trying to check flights with 1 stop over")
        flights = flight_search.check_flights(ORIGINAL_CITY, destination["iataCode"],
                                              date_from=tomorrow, date_to=six_month_from_now, stop_overs=2)
        message = f"Low price alert! Only {flights.price} euros to fly from {flights.origin_city}-{flights.origin_airport}" \
                  f" to {flights.destination_city}-{flights.destination_airport}, from {flights.out_date} " \
                  f"to {flights.return_date}.\nFlight has 1 stop over, via {flights.via_city}. \n\n{flights.deep_link}"
    else:
        message = f"Low price alert! Only {flights.price} euros to fly from {flights.origin_city}-{flights.origin_airport}" \
                  f" to {flights.destination_city}-{flights.destination_airport}, " \
                  f"from {flights.out_date} to {flights.return_date}. \n\n{flights.deep_link}"

    if flights.price < destination["lowestPrice"]:
        data_manager.change_price(flights.price, destination["id"])
        # sms.send_message(message_text=message)

        for user in users_data:
            email = user["email"]
            sms.send_email(email, message)

