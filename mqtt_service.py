from main import Modem
import time

modem = Modem()


def check_connection(client_idx):
    modem.send_command("AT+QMTCONN?")
    status_response = modem.read_response()

    if not f"+QMTCONN: {client_idx},3" in status_response["data"]:
        raise Exception("The client is not connected to any MQTT server.")


def open(client_idx, hostname, port):
    modem.send_command(f'AT+QMTOPEN={client_idx},"{hostname}",{port}')
    response = modem.read_response(find="+QMTOPEN:")

    if f"+QMTOPEN: {client_idx},2" in response["data"]:
        raise Exception("MQTT identifier is occupied.")
    if not f"+QMTOPEN: {client_idx},0" in response["data"]:
        raise Exception("The network cannot opened for MQTT client.")

    return response


def connect(client_idx, hostname, port, client_id):
    modem.send_command(f"AT+QMTOPEN?")
    status_response = modem.read_response()

    if not f'+QMTOPEN: {client_idx},"{hostname}",{port}' in status_response["data"]:
        raise Exception("No MQTT client opened yet.")

    modem.send_command(f'AT+QMTCONN={client_idx},"{client_id}"')
    response = modem.read_response(find="+QMTCONN:")

    if not f"+QMTCONN: {client_idx},0,0" in response["data"]:
        raise Exception("The client cannot connect to MQTT server.")

    return response


def mqtt_configuration(client_idx, hostname, port, client_id):
    modem.send_command(f'AT+QMTCFG="recv/mode",0,0,1')

    modem.send_command(
        f'AT+QMTCFG="aliauth",0,"oyjtmPl5a5j","MQTT_TEST","wN9Y6pZSIIy7Exa5qVzcmigEGO4kAazZ"'
    )
    modem.read_response()

    network_response = open(client_idx, hostname, port)
    print("Network Response:", network_response["data"])

    server_response = connect(client_idx, hostname, port, client_id)
    print("\nServer Response:", server_response["data"])


def subscribe(client_idx, msgid, topic, qos):
    check_connection(client_idx)

    modem.send_command(f'AT+QMTSUB={client_idx},{msgid},"{topic}",{qos}')
    response = modem.read_response(find="+QMTSUB:")

    if not f"+QMTSUB: {client_idx},{msgid},0" in response["data"]:
        raise Exception(f'The client could not subscribe the "{topic}" topic.')

    return response


def publish(client_idx, msgid, qos, retain, topic, message):
    check_connection(client_idx)

    modem.send_command(
        f'AT+QMTPUBEX={client_idx},{msgid},{qos},{retain},"{topic}",{len(message)}'
    )
    time.sleep(0.5)
    modem.send_command(message)
    response = modem.read_response(find="+QMTPUBEX:")

    return response


def receive():
    response = modem.read_response(find="+QMTRECV:")

    return response


def publish_message(
    client_idx, hostname, port, client_id, msgid, qos, retain, topic, message
):
    mqtt_configuration(client_idx, hostname, port, client_id)

    response = publish(client_idx, msgid, qos, retain, topic, message)

    return response


def receive_message(
    client_idx,
    hostname,
    port,
    client_id,
    msgid_sub,
    msgid_pub,
    qos,
    retain,
    topic,
    message,
):
    mqtt_configuration(client_idx, hostname, port, client_id)

    subscribe_response = subscribe(client_idx, msgid_sub, topic, qos)
    print("\nSubscribe Response:", subscribe_response["data"])

    publish_response = publish(client_idx, msgid_pub, qos, retain, topic, message)
    print("\nPublish Response:", publish_response["data"])

    response = receive()

    return response
