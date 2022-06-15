import requests

SHEETY_ENDPOINT = "https://api.sheety.co/xxx"
HEADERS = {
    'Authorization': 'xxx'
}


class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.user_name = ""
        self.user_surname = ""
        self.email = ""
        self.users_data = {}

    def get_destination_data(self):
        response = requests.get(url=f"{SHEETY_ENDPOINT}/prices", headers=HEADERS)
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def add_iata_code(self):
        for city in self.destination_data:
            new_params = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            row_endpoint = f"{SHEETY_ENDPOINT}/prices/{city['id']}"
            requests.put(url=row_endpoint, json=new_params, headers=HEADERS)

    def change_price(self, price, row_id):
        new_params = {
            "price": {
                "lowestPrice": price
            }
        }
        row_endpoint = f"{SHEETY_ENDPOINT}/prices/{row_id}"
        requests.put(url=row_endpoint, json=new_params, headers=HEADERS)

    def add_user(self):
        self.user_name = input("What is your first name?\n")
        self.user_surname = input("What is your last name?\n")

        correct_email = False
        while not correct_email:
            self.email = input("What is your email?\n")
            email_second_attempt = input("Type your email again.\n")
            if self.email == email_second_attempt:
                correct_email = True
                print("You are in the club!")
            else:
                print("There are differences in your emails. Please type your email again.")

        parameters = {
            "user": {
                "firstName": self.user_name,
                "lastName": self.user_surname,
                "email": self.email,
            }
        }
        requests.post(url=f"{SHEETY_ENDPOINT}/users", headers=HEADERS, json=parameters)

    def get_users_data(self):
        response = requests.get(url=f"{SHEETY_ENDPOINT}/users", headers=HEADERS)
        self.users_data = response.json()["users"]
        return self.users_data