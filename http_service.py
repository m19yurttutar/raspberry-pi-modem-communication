from dotenv import dotenv_values
from main import Modem
import time

env = dotenv_values(".env")

modem = Modem()


def check_ps_domain_attached():
    modem.send_command("AT+CGATT?")
    response = modem.read_response()
    return "+CGATT: 1" in response["data"]


def check_ps_domain_registered():
    modem.send_command("AT+CGREG?")
    response = modem.read_response()
    return "+CGREG: 0,5" in response["data"]


def check_pdp_context_parameters(pdp_context_id, apn):
    modem.send_command(f'AT+CGDCONT={pdp_context_id},"IP","{apn}"')
    response = modem.read_response()
    return response["data"] == "OK"


def check_pdp_context_activated(pdp_context_id):
    modem.send_command("AT+CGACT?")
    response = modem.read_response()
    return f"+CGACT: 1,{pdp_context_id}" in response["data"]


def check_max_pdp_contexts_reached():
    modem.send_command("AT+CGACT?")
    response = modem.read_response()
    return response["data"].count(",1") >= 3


def activate_pdp_context(pdp_context_id, apn):
    if check_pdp_context_activated(pdp_context_id):
        return True

    # Check preconditions
    if not check_ps_domain_attached():
        raise Exception("PS domain not attached")
    if not check_ps_domain_registered():
        raise Exception("PS domain not registered")
    if not check_pdp_context_parameters(pdp_context_id, apn):
        raise Exception("Invalid PDP context parameters")
    if check_max_pdp_contexts_reached():
        raise Exception("Maximum PDP contexts reached")

    # Configure PDP Context
    modem.send_command(f'AT+CGDCONT={pdp_context_id},"IP","{apn}"')
    response = modem.read_response()
    if response["data"] != "OK":
        raise Exception(f'AT+CGDCONT failed: {response["data"]}')

    time.sleep(2)

    # Activate PDP context
    modem.send_command(f"AT+CGACT=1,{pdp_context_id}")
    response = modem.read_response()
    if response["data"] != "OK":
        raise Exception(f'AT+CGACT failed: {response["data"]}')

    time.sleep(2)

    if not check_pdp_context_activated(pdp_context_id):
        raise Exception("PDP context activation failed")

    return True


# Sends requests based on preset url information(to be improved)
def send_http_get(pdp_context_id, apn, url):
    if activate_pdp_context(pdp_context_id, apn):
        modem.send_command(f"AT+QHTTPURL={len(url)},80")

        time.sleep(1)

        modem.send_command(url)
        modem.read_response()

        time.sleep(1)

        modem.send_command("AT+QHTTPGET=80")
        modem.read_response()

        time.sleep(3)

        modem.send_command("AT+QHTTPREAD=80")
        response = modem.read_response()
        return response


# Sends requests based on preset url information(to be improved)
def send_http_post(pdp_context_id, apn, url, data):
    if activate_pdp_context(pdp_context_id, apn):
        modem.send_command(f"AT+QHTTPURL={len(url)},80")

        time.sleep(1)

        modem.send_command(url)
        modem.read_response()

        time.sleep(1)

        modem.send_command(f"AT+QHTTPPOST={len(data)},80,80")

        time.sleep(1)

        modem.send_command(data)
        modem.read_response()

        time.sleep(3)

        modem.send_command("AT+QHTTPREAD=80")
        response = modem.read_response()
        return response
