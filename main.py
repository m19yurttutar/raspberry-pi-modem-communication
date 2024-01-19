import serial
from serial.tools import list_ports
import time

modem_information = {"vid": 11388, "pid": 293}


class Modem:
    def __init__(self, port=None, baudrate=15200, parity=serial.PARITY_NONE):
        if port is None:
            # Automatically finding the serial port
            ports = list_ports.comports()
            for p in ports:
                if (p.vid == modem_information["vid"]) and (
                    p.pid == modem_information["pid"]
                ):
                    port = p.device
                    break

        self.serial = serial.Serial(port, baudrate, parity=parity)

    def open_connection(self):
        if not (self.serial and (not self.serial.is_open)):
            return {
                "status": "fail",
                "message": "Serial port is either already open or does not exist.",
            }

        try:
            self.serial.open()
            return {
                "status": "success",
                "message": "The serial port opened successfully.",
            }
        except serial.SerialException as e:
            raise serial.SerialException(
                f"An error occurred while opening the serial port: {e}"
            )

    def send_command(self, command):
        if not (self.serial and self.serial.is_open):
            return {
                "status": "fail",
                "message": "Serial port is either not open or does not exist.",
            }

        try:
            self.serial.write(command.encode() + b"\r\n")
            return {
                "status": "success",
                "message": "The command was sent successfully.",
            }
        except serial.SerialException as e:
            raise serial.SerialException(
                f"An error occurred while sending the command: {e}"
            )

    def read_response(self, timeout=5, find=None):
        if not (self.serial and self.serial.is_open):
            return {
                "status": "fail",
                "message": "Serial port is either not open or does not exist.",
            }

        try:
            response = ""
            start_time = time.time()
            while time.time() - start_time < timeout:
                chunk = self.serial.read().decode("utf-8")
                response += chunk
                if not find == None:
                    if (find in response) and (response.endswith("\r\n")):
                        response = response.strip()
                        return {
                            "status": "success",
                            "data": response,
                            "message": "The response was read successfully.",
                        }
                else:
                    if response.endswith("OK\r\n"):
                        response = response.strip()
                        return {
                            "status": "success",
                            "data": response,
                            "message": "The response was read successfully.",
                        }
                    elif response.endswith("ERROR"):
                        response = response.strip()
                        return {
                            "status": "fail",
                            "data": response,
                            "message": "Invalid command syntax or format.",
                        }

            return {
                "status": "fail",
                "data": response,
                "message": "Timeout occurred while reading serial port.",
            }
        except serial.SerialException as e:
            raise serial.SerialException(
                f"An error occurred while reading the serial port: {e}"
            )

    def close_connection(self):
        if not (self.serial and self.serial.is_open):
            return {
                "status": "fail",
                "data": None,
                "message": "Serial port is either not open or does not exist.",
            }

        try:
            self.serial.close()
            return {
                "status": "success",
                "data": None,
                "message": "Serial port closed successfully.",
            }
        except serial.SerialException as e:
            raise serial.SerialException(
                f"An error occurred while closing the serial port: {e}"
            )
