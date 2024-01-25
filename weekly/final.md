# Project Final Report

## 1. Introduction
This project aimed to develop a Python library for communicating with a modem, allowing for configuration changes, data transmission, and reception. Additionally, the project included the implementation of sample codes for sending HTTP GET and POST requests to [webhook.site](http://webhook.site) and publishing MQTT messages to a topic on the [HiveMQ](https://www.hivemq.com/mqtt/public-mqtt-broker/) broker via the modem. Furthermore, the Raspberry Pi's internet connectivity through the modem was established using three different protocols: PPP, QMI/RMNET, and ECM. The project also involved measuring the speeds of connections established with these three protocols and conducting a general comparison.

## 2. Modem Communication Library
The developed Python library enables communication with the modem by sending AT commands and processing the responses received. It includes features such as automatic detection of the modem's serial port. The library provides a modular and flexible interface for interacting with modems. For details visit [main.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/main.py).

### 2.1. Features
- **AT Command Handling:** The library allows the transmission of AT commands to the modem and processes the corresponding responses.

- **Serial Port Autodetection:** Extra functionality for automatically detecting the modem's serial port is implemented.

### 2.2. Usage
```
from main import Modem

# Automatic port detection is available
modem = Modem()

# Open the serial port
open_response = modem.open_connection()

# Output the given command as a byte array over the serial port
write_reponse = modem.send_command(command)

# Reading the byte array on the serial port by converting it to string
read_response = modem.read_response(timeout, find)

# Close the serial port
close_response = modem.close_conection()
```

## 3. HTTP Client
A sample code was developed to send HTTP GET and POST requests to [webhook.site](http://webhook.site) using the previously implemented modem communication library. For details visit [http_client.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/http_client.py).

### 3.1. Features
- **PDP Context Activation:** HTTP Client contains a function that checks whether PDP content is enabled and if not, enables PDP content.

- **HTTP GET and POST Requests:** HTTP Client sends HTTP GET and POST requests to the entered url and reads the incoming response successfully.

### 3.2. Usage
In addition to the code shown as an example below, the HTTP client also contains a function that queries whether the PDP context is active or not and activates it if it is not, and functions for the verifications required to activate the PDP context.

```
from main import Modem
from http_client import ModemHTTPClient

modem = Modem() # Automatic port detection is available
http_client = ModemHTTPClient()

get_response = http_client.send_http_get(context_id, apn, url)

post_response = http_client.send_http_post(context_id, apn, url, data)
```

## 4. MQTT Client
Another sample code was developed to send MQTT messages to a topic on the [HiveMQ](https://www.hivemq.com/mqtt/public-mqtt-broker) broker and subscribe to the same topic to read messages using the modem communication library. For details visit [mqtt_client.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/mqtt_client.py).

### 4.1. Features
- **Main MQTT Functions:** There are two main functions in MQTT Client. These are the subscribe function, which allows subscribing to the mqtt broker, and the publish functions, which allow a message to be published on a topic.

- **Auxiliary MQTT Functions:** Other functions such as open, connect, and disconnect, which are not included in the main functions, help perform main functions such as publishing messages and subscribing.

### 4.2. Usage
The MQTT client, like the HTTP client, includes functions in addition to the code shown as an example below. These are various functions that perform the functions of connecting to the network, connecting to the server, disconnecting from the server, subscribing to a topic, publishing to the topic, and receiving from the subscribed topic.

```
from main import Modem
from mqtt_client import ModemMQTTClient

modem = Modem() # Automatic port detection is available
mqtt_client = ModemMQTTClient()

receive_message_response = mqtt_client.receive_message(
    client_idx,
    hostname,
    port,
    client_id,
    sub_msgid,
    pub_msgid,
    qos,
    retain,
    topic,
    message
)

publish_message_reponse = mqtt_client.publish_message(
    client_idx,
    hostname,
    port,
    client_id,
    msgid,
    qos,
    retain,
    topic,
    message
)
```

## 5. Raspberry Pi Internet Connectivity
By using the three different protocols mentioned, Raspberry Pi was successfully enabled to access the internet via modem: PPP, QMI/RMNET and ECM.

### 5.1 Speed Tests of Protocols
The connection speeds of protocols were measured separately using the speedtest-cli library.

#### 5.1.1 PPP (Point-to-Point Protocol)



#### 5.1.2 QMI (Quelcom MSM Interface)



#### 5.1.3 ECM (Ethernet Control Model)



### 5.2 Comparison of Protocols
- **PPP:** PPP's performance typically depends on the type of connection and the physical environment. For example, it provides low bandwidth in dial-up connections but can achieve higher performance in DSL or faster connections. PPP can support various types of connections but is more suitable for point-to-point connections.

- **QMI:** QMI generally supports high-speed mobile data transmission. It performs well in devices using Qualcomm chipsets for data, voice, and GPS communication. Optimized for communication between mobile devices and is commonly used in such devices.

- **ECM:** ECM carries Ethernet traffic over USB. This allows a computer to connect to an Ethernet network through its USB port. Performance depends on the USB version used and the connection speed. Designed for computer-to-computer USB Ethernet connections.