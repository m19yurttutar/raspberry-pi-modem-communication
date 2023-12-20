import serial
from serial.tools import list_ports


class Modem:
    def __init__(self, port=None, baudrate=15200, parity=serial.PARITY_NONE):
        if port is None:
            # Automatically finding the serial port
            ports = list_ports.comports()
            for p in ports:
                if "EG25-G" in p.description:
                    port = p.device
                    break

        self.ser = serial.Serial(port, baudrate, parity=parity)

    def open_connection(self):
        try:
            self.ser.open()
            if self.ser.is_open:
                print("Modem connection opened.")
        except Exception as e:
            print("An error occurred while opening the modem connection:", str(e))

    def send_command(self, command):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(command.encode() + b"\r\n")
            except serial.SerialException as e:
                print(f"Serial communication error: {e}")
        else:
            print("Serial port is not open.")

    def read_response(self):
        if self.ser and self.ser.is_open:
            try:
                response = self.ser.read_until(b"OK\r\n").decode().split("\r\n")[1]
                return response
            except serial.SerialException as e:
                print(f"Serial communication error: {e}")
                return None
        else:
            print("Serial port is not open.")
            return None

    def close_connection(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial port closed.")
        else:
            print("Serial port is not open.")


modem = Modem()

AT_COMAMNDS = [
    "AT",
    "AT+CGMI",
    "AT+CGMM",
    "AT+CPIN?",
    "AT+CSQ",
    "AT+CMGL",
]

for command in AT_COMAMNDS:
    modem.send_command(command)
    response = modem.read_response()
    print(f"Modem response({command}):", response)

modem.close_connection()
