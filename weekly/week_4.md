# Project Progress Report - Week 4

## Project Overview

This week, I delved into the specifics of AT commands necessary for configuring parameters and establishing connections to facilitate HTTP requests through the modem. Within my Python library, I included a code snippet responsible for transmitting a GET request from the modem to [webhook.site](https://webhook.site). This addition was made possible through the integration of AT commands into the project.

## Tasks Completed

### 1. Research

- **HTTP Requests with AT Commands:** I researched which AT commands should be used to enter the necessary parameters and connections for HTTP requests via the modem and how to read the responses. Some AT commands I learned as a result of my research are as follows:

```
AT+QICSGP=1,1,"Turkcell Twilio","","",1 //Configure PDP context 1.
AT+QIACT=1 //Activate PDP context 1.
AT+QHTTPURL=23,80 //Set the URL which will be accessed and the timeout value is 80 seconds.
AT+QHTTPGET=80 //Send HTTP GET request and the maximum response time is 80 seconds.
AT+QHTTPREAD=80 //Read HTTP response information.
```

### 2. Functional Development

- **HTTP GET Requests:** I wrote a code block where we can send a get request to a pre-prepared url. While working on this task, I noticed a few deficiencies in the library I had already written. I will start my work next week by correcting these deficiencies. For details visit [service.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/service.py)

```
def send_http_get():
    modem.send_command("AT+QHTTPGET=80")
    modem.read_response()
    time.sleep(3)
    modem.send_command("AT+QHTTPREAD=80")
    response = modem.read_response()
    print(response["data"])
```

![Image 1](https://github.com/m19yurttutar/raspberry-pi-modem-communication/assets/76749251/c50ae5f7-66b3-4711-9d59-07c2d646dd55)

## Next Steps

Looking ahead, the focus will be on:

- **Improvements:** I will eliminate the deficiencies I noticed in the Python library I wrote by developing HTTP requests and integrating them into the modem.

## References

1. [Webhook.site](https://webhook.site)

2. Quectel_EC2x&EG9x&EG2x-G&EM05_Series_HTTP(S)_Application_Note_V1.2

3. Quectel_EC2xEG9xEG2x-GEM05_Series_AT_Commands_Manual_V2.0
