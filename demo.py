from main import Modem
from http_client import ModemHTTPClient
from mqtt_client import ModemMQTTClient
from dotenv import dotenv_values

env = dotenv_values()

# MODEM DEMOS
modem = Modem()  # modem = Modem("/dev/ttyUSB3", 15200, 8, "N")


def modem_demo(command):
    response = modem.open_connection()
    print(f"OPEN RESPONSE:\n{response}")

    response = modem.send_command(command)
    print(f"\nWRITE RESPONSE:\n{response}")

    response = modem.read_response()
    print(f"\nREAD RESPONSE:\n{response}")
    print(f"\nREAD RESPONSE DATA:\n{response['data']}")

    response = modem.close_connection()
    print(f"\nCLOSE RESPONSE:\n{response}")


# modem_demo("ATI")


# HTTP DEMOS
http_client = ModemHTTPClient(modem)


def http_demo_1(context_id, apn):
    response = http_client.activate_pdp_context(context_id, apn)
    print(f"PDP ACTIVATION:\n{response}")


# http_demo_1(1, "super")


def http_demo_2(context_id, apn, url, data):
    response = http_client.send_http_post(context_id, apn, url, data)
    print(f"POST RESPONSE:\n{response}")
    print(f"\nPOST RESPONSE DATA:\n{response['data']}")


# http_demo_2(1, "super", f"https://webhook.site/{env['API_KEY']}", "HTTP Demo")


def http_demo_3(context_id, apn, url):
    response = http_client.send_http_get(context_id, apn, url)
    print(f"GET RESPONSE:\n{response}")
    print(f"\nGET RESPONSE DATA:\n{response['data']}")


# http_demo_3(1, "super", f"https://webhook.site/token/{env['API_KEY']}/request/latest/raw")


# MQTT DEMOS
mqtt_client = ModemMQTTClient(modem)

def mqtt_demo_1(client_idx, hostname, port, client_id, msgid, qos, retain, topic, message):
    response = mqtt_client.publish_message(client_idx, hostname, port, client_id, msgid, qos, retain, topic, message)
    print(f"\nPUBLISH RESPONSE:\n{response}")
    print(f"\nPUBLISH RESPONSE DATA:\n{response['data']}")

    response = mqtt_client.disconnect(client_idx)
    print(f"\nDISCONNECT RESPONSE:\n{response}")
    print(f"\nDISCONNECT RESPONSE DATA:\n{response['data']}")

# mqtt_demo_1(1, "broker.hivemq.com", 1883, "clientExample", 0, 0, 0, "topic/pub", "Hello Quectel!!!")

def mqtt_demo_2(client_idx, hostname, port, client_id, sub_msgid, pub_msgid, qos, retain, topic, message):
    response = mqtt_client.receive_message(client_idx, hostname, port, client_id, sub_msgid, pub_msgid, qos, retain, topic, message)
    print(f"\nRECEIVE RESPONSE:\n{response}")
    print(f"\nRECEIVE RESPONSE DATA:\n{response['data']}")

    response = mqtt_client.disconnect(client_idx)
    print(f"\nDISCONNECT RESPONSE:\n{response}")
    print(f"\nDISCONNECT RESPONSE DATA:\n{response['data']}")


mqtt_demo_2(1, "broker.hivemq.com", 1883, "clientExample", 1, 0, 0, 0, "topic/pub", "Hello Quectel!")
