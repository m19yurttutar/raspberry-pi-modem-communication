from main import Modem
import time


class ModemHTTPClient:
    def __init__(self, modem: Modem):
        self.modem = modem

    def check_ps_domain_attached(self):
        self.modem.send_command("AT+CGATT?")
        response = self.modem.read_response()
        return "+CGATT: 1" in response["data"]

    def check_ps_domain_registered(self):
        self.modem.send_command("AT+CGREG?")
        response = self.modem.read_response()
        return "+CGREG: 0,5" in response["data"]

    def check_pdp_context_parameters(self, context_id: int, apn: str):
        self.modem.send_command(f'AT+CGDCONT={context_id},"IP","{apn}"')
        response = self.modem.read_response()
        return "OK" in response["data"]

    def check_pdp_context_activated(self, context_id: int):
        self.modem.send_command("AT+CGACT?")
        response = self.modem.read_response()
        return f"+CGACT: {context_id},1" in response["data"]

    def check_max_pdp_contexts_reached(self):
        self.modem.send_command("AT+CGACT?")
        response = self.modem.read_response()
        return response["data"].count(",1") >= 3

    def activate_pdp_context(self, context_id: int, apn: str):
        if self.check_pdp_context_activated(context_id):
            return True

        # Check preconditions
        if not self.check_ps_domain_attached():
            raise Exception("PS domain not attached")
        if not self.check_ps_domain_registered():
            raise Exception("PS domain not registered")
        if not self.check_pdp_context_parameters(context_id, apn):
            raise Exception("Invalid PDP context parameters")
        if self.check_max_pdp_contexts_reached():
            raise Exception("Maximum PDP contexts reached")

        # Configure PDP Context
        self.modem.send_command(f'AT+CGDCONT={context_id},"IP","{apn}"')
        response = self.modem.read_response()
        if not "OK" in response["data"]:
            raise Exception(f'AT+CGDCONT failed: {response["data"]}')

        # Activate PDP context
        self.modem.send_command(f"AT+CGACT=1,{context_id}")
        response = self.modem.read_response()
        if not "OK" in response["data"]:
            raise Exception(f'AT+CGACT failed: {response["data"]}')

        if not self.check_pdp_context_activated(context_id):
            raise Exception("PDP context activation failed")

        return True

    # Sends requests based on preset url information(to be improved)
    def send_http_get(self, context_id: int, apn: str, url: str):
        if self.activate_pdp_context(context_id, apn):
            self.modem.send_command(f"AT+QHTTPURL={len(url)},80")
            response = self.modem.read_response(find="CONNECT")

            time.sleep(1)

            if not "CONNECT" in response["data"]:
                raise Exception(
                    "The URL length and timeout value could not be set properly."
                )

            self.modem.send_command(url)
            response = self.modem.read_response()

            if not "OK" in response["data"]:
                raise Exception("The URL could not be set properly.")

            self.modem.send_command("AT+QHTTPGET=80")
            response = self.modem.read_response(find="+QHTTPGET:")

            if not "+QHTTPGET: 0,200" in response["data"]:
                raise Exception(
                    "The timeout value could not be set properly for the GET request."
                )

            time.sleep(2)

            self.modem.send_command("AT+QHTTPREAD=80")
            response = self.modem.read_response(find="+QHTTPREAD:")

            if not "+QHTTPREAD: 0" in response["data"]:
                raise Exception("The data could not be read properly.")

            return response

    # Sends requests based on preset url information(to be improved)
    def send_http_post(self, context_id: int, apn: str, url: str, data):
        if self.activate_pdp_context(context_id, apn):
            self.modem.send_command(f"AT+QHTTPURL={len(url)},80")
            response = self.modem.read_response(find="CONNECT")

            time.sleep(1)

            if not "CONNECT" in response["data"]:
                raise Exception(
                    "The URL length and timeout value could not be set properly."
                )

            self.modem.send_command(url)
            response = self.modem.read_response()

            if not "OK" in response["data"]:
                raise Exception("The URL could not be set properly.")

            self.modem.send_command(f"AT+QHTTPPOST={len(data)},80,80")
            response = self.modem.read_response(find="CONNECT")

            time.sleep(1)

            if not "CONNECT" in response["data"]:
                raise Exception(
                    "The data length and timeout value could not be set properly."
                )

            self.modem.send_command(data)
            response = self.modem.read_response(find="+QHTTPPOST:")

            if not "+QHTTPPOST: 0,200" in response["data"]:
                raise Exception("The data could not be set properly.")

            time.sleep(2)

            self.modem.send_command("AT+QHTTPREAD=80")
            response = self.modem.read_response(find="+QHTTPREAD:")

            if not "+QHTTPREAD: 0" in response["data"]:
                raise Exception("The data could not be read properly.")

            return response
