import serial
from serial.tools import list_ports

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

    def read_response(self):
        if not (self.serial and self.serial.is_open):
            return {
                "status": "fail",
                "message": "Serial port is either not open or does not exist.",
            }

        try:
            response = b""
            while True:
                chunk = self.serial.read(1)
                response += chunk
                if response.endswith(b"OK\r\n"):
                    response = (
                        response.decode("utf-8")
                        .replace("OK\r\n", "OK")
                        .split("\r\r\n")[1]
                        .split("\r\n\r\n")[0]
                    )
                    return {
                        "status": "success",
                        "data": response,
                        "message": "The response was read successfully.",
                    }
                elif response.endswith(b"ERROR"):
                    response = response.decode("utf-8").split("\r\r\n")[1]
                    return {
                        "status": "fail",
                        "data": response,
                        "message": "Invalid command syntax or format.",
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
