from dotenv import dotenv_values
from main import Modem
import time

env = dotenv_values(".env")

modem = Modem()


# Sends requests based on preset url information(to be improved)
def send_http_get():
    modem.send_command("AT+QHTTPGET=80")
    modem.read_response()
    time.sleep(3)
    modem.send_command("AT+QHTTPREAD=80")
    response = modem.read_response()
    print(response["data"])


send_http_get()
