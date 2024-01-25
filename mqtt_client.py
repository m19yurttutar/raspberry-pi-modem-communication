from main import Modem
import time


class ModemMQTTClient:
    def __init__(self, modem: Modem):
        self.modem = modem

    def check_connection(self, client_idx: int):
        self.modem.send_command("AT+QMTCONN?")
        status_response = self.modem.read_response()

        if not f"+QMTCONN: {client_idx},3" in status_response["data"]:
            raise Exception("The client is not connected to any MQTT server.")

    def open(self, client_idx: int, hostname: str, port: int):
        self.modem.send_command(f'AT+QMTOPEN={client_idx},"{hostname}",{port}')
        response = self.modem.read_response(find="+QMTOPEN:")
        print(response)

        if f"+QMTOPEN: {client_idx},2" in response["data"]:
            raise Exception("MQTT identifier is occupied.")
        if not f"+QMTOPEN: {client_idx},0" in response["data"]:
            raise Exception("The network cannot opened for MQTT client.")

        return response

    def connect(self, client_idx: int, hostname: str, port: int, client_id: str):
        self.modem.send_command(f"AT+QMTOPEN?")
        status_response = self.modem.read_response()

        if not f'+QMTOPEN: {client_idx},"{hostname}",{port}' in status_response["data"]:
            raise Exception("No MQTT client opened yet.")

        self.modem.send_command(f'AT+QMTCONN={client_idx},"{client_id}"')
        response = self.modem.read_response(find="+QMTCONN:")

        if not f"+QMTCONN: {client_idx},0,0" in response["data"]:
            raise Exception("The client cannot connect to MQTT server.")

        return response
    
    def disconnect(self, client_idx: int):
        self.modem.send_command(f"AT+QMTCONN?")
        status_response = self.modem.read_response()

        if not f'+QMTCONN: {client_idx},3' in status_response["data"]:
            raise Exception("There is no connection.")

        self.modem.send_command(f'AT+QMTDISC={client_idx}')
        response = self.modem.read_response()

        if not "OK" in response["data"]:
            raise Exception("The connection could not be closed.")

        return response

    def mqtt_configuration(
        self, client_idx: int, hostname: str, port: int, client_id: str
    ):
        self.modem.send_command(f'AT+QMTCFG="recv/mode",0,0,1')

        self.modem.send_command(
            f'AT+QMTCFG="aliauth",0,"oyjtmPl5a5j","MQTT_TEST","wN9Y6pZSIIy7Exa5qVzcmigEGO4kAazZ"'
        )
        self.modem.read_response()

        network_response = self.open(client_idx, hostname, port)
        print(f"\nNETWORK RESPONSE:\n{network_response['data']}")

        server_response = self.connect(client_idx, hostname, port, client_id)
        print(f"\nSERVER RESPONSE:\n{server_response['data']}")

    def subscribe(self, client_idx: int, msgid: int, topic: str, qos: int):
        self.check_connection(client_idx)

        self.modem.send_command(f'AT+QMTSUB={client_idx},{msgid},"{topic}",{qos}')
        response = self.modem.read_response(find="+QMTSUB:")

        if not f"+QMTSUB: {client_idx},{msgid},0" in response["data"]:
            raise Exception(f'The client could not subscribe the "{topic}" topic.')

        return response

    def publish(
        self,
        client_idx: int,
        msgid: int,
        qos: int,
        retain: int,
        topic: str,
        message: str,
    ):
        self.check_connection(client_idx)

        self.modem.send_command(
            f'AT+QMTPUBEX={client_idx},{msgid},{qos},{retain},"{topic}",{len(message)}'
        )

        time.sleep(1)

        self.modem.send_command(message)
        response = self.modem.read_response(find="+QMTPUBEX:")

        return response

    def receive(self):
        response = self.modem.read_response(find="+QMTRECV:")

        return response

    def publish_message(
        self,
        client_idx: int,
        hostname: str,
        port: int,
        client_id: str,
        msgid: int,
        qos: int,
        retain: int,
        topic: str,
        message: str,
    ):
        self.mqtt_configuration(client_idx, hostname, port, client_id)

        response = self.publish(client_idx, msgid, qos, retain, topic, message)

        return response

    def receive_message(
        self,
        client_idx: int,
        hostname: str,
        port: int,
        client_id: str,
        sub_msgid: int,
        pub_msgid: int,
        qos: int,
        retain: int,
        topic: str,
        message: str,
    ):
        self.mqtt_configuration(client_idx, hostname, port, client_id)

        subscribe_response = self.subscribe(client_idx, sub_msgid, topic, qos)
        print("\nSubscribe Response:", subscribe_response["data"])

        publish_response = self.publish(client_idx, pub_msgid, qos, retain, topic, message)
        print("\nPublish Response:", publish_response["data"])

        response = self.receive()

        return response
