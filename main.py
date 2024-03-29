from __future__ import annotations
import serial
from serial.tools import list_ports
import time

modem_information = {"vid": 11388, "pid": 293}


class Modem:
    def __init__(
        self,
        port: str = None,
        baudrate: int = 15200,
        bytesize: int = serial.EIGHTBITS,
        parity: str = serial.PARITY_NONE,
        stopbits: float = serial.STOPBITS_ONE,
        timeout: float | None = None,
        xonxoff: bool = False,
        rtscts: bool = False,
        write_timeout: float | None = None,
        dsrdtr: bool = False,
        inter_byte_timeout: float | None = None,
        exclusive: float | None = None,
    ):
        if port is None:
            # Automatically finding the serial port
            ports = list_ports.comports()
            for p in ports:
                if (p.vid == modem_information["vid"]) and (
                    p.pid == modem_information["pid"]
                ):
                    port = p.device
                    break

        self.serial = serial.Serial(
            port,
            baudrate,
            bytesize,
            parity,
            stopbits,
            timeout,
            xonxoff,
            rtscts,
            write_timeout,
            dsrdtr,
            inter_byte_timeout,
            exclusive,
        )

    def open_connection(self):
        if not (self.serial and (not self.serial.is_open)):
            return {
                "status": "fail",
                "message": "The serial port is either already opened or does not exist.",
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

    def send_command(self, command: str):
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

    def read_response(self, timeout: float = 5, find: str = None):
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
                "message": "Serial port is either not open or does not exist.",
            }

        try:
            self.serial.close()
            return {
                "status": "success",
                "message": "Serial port closed successfully.",
            }
        except serial.SerialException as e:
            raise serial.SerialException(
                f"An error occurred while closing the serial port: {e}"
            )
