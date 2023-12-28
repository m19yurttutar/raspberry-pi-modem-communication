import requests
from dotenv import dotenv_values
from main import Modem

env = dotenv_values(".env")


def post_data(json):
    url = f"https://webhook.site/{env['API_KEY']}"
    headers = {"accept": "application/json", "api-key": env["API_KEY"]}

    response = requests.post(url, json=json, headers=headers)

    return response.json()


def get_last_posted_data():
    url = f"https://webhook.site/token/{env['API_KEY']}/request/latest/raw"
    headers = {"content-type": "application/json"}

    response = requests.get(url, headers=headers)

    return response.json()


modem = Modem()

modem.send_command("AT")
modem_response = modem.read_response()

modem.close_connection()

print("POST Response:", post_data(modem_response))
print("GET Response: ", get_last_posted_data())
