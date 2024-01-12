# Project Progress Report - Week 5

## Project Overview

This week, I functionally completed my code that sends HTTP GET and POST requests (refactoring required for clean code). I also implemented a function in my project that checks whether the PDP context is activated or not, and if not, activates the PDP context. Here is a breakdown of the tasks performed:

## Tasks Completed

### 1. Improvements

- **HTTP GET Requests:** Last week, I sent a request to a URL pre-prepared by the modem for HTTP GET requests and received a response. This week, I updated the functions to take the context ID, URL, and APN as function parameters. In this way, I obtained more dynamic functions. For details visit [http_service.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/http_service.py)

```
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
```

![Screenshot_1](https://github.com/m19yurttutar/raspberry-pi-modem-communication/assets/76749251/c5ab7498-71f7-4e91-8227-6605183adbaf)

### 2. Functional Development

- **Activating PDP Context:** I added a function to my code that checks whether the PS domain has been added, the PS domain is registered, PDP contexts are enabled, and the maximum PDP contexts have been reached. For details visit [http_service.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/http_service.py)

- **HTTP POST Requests:** A function that sends HTTP POST requests has been added to the application. As seen in the code below, before sending the POST request, it is checked whether the PDP context is active or not, and if not, it is activated. For details visit [http_service.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/http_service.py)

```
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
```

![Screenshot_2](https://github.com/m19yurttutar/raspberry-pi-modem-communication/assets/76749251/1d4e394d-4fdc-4c9b-8691-5d199ce12058)

### 3. Researches

- **MQTT:** I learned how MQTT works by doing general research on it. Then, from the Quectel_LTE_Standard_MQTT_Application_Note_V1.2 guide, I examined how MQTT configuration is done, how to send messages to the MQTT broker and receive messages by subscribing to the MQTT broker, and which AT commands are used.

## Next Steps

Looking ahead, the focus will be on:

- **Functional Development:** I will develop sample code to send messages to an MQTT broker via modem and to subscribe and read incoming messages.

- **Code Refactoring:** A general code refactoring must be done for all code written so far.

## References

1. [MQTT](https://mqtt.org)

2. Quectel_EC2xEG9xEG2x-GEM05_Series_AT_Commands_Manual_V2.0

3. Quectel_EC2x&EG9x&EG2x-G&EM05_Series_HTTP(S)\_Application_Note_V1.2

4. Quectel_LTE_Standard_MQTT_Application_Note_V1.2

## Conclusion

This week has been pretty productive for the project. I've upgraded the code for sending HTTP requests, making it more flexible. The new feature that checks and activates the PDP context is up and running, adding a solid functionality layer. Also, I took some time to dig into MQTT, learning the ropes and setting the stage for integrating it into the project.
