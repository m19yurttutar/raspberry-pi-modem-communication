# Project Progress Report - Week 3

## Project Overview

This week, I made developments and improvements in the Python library that enables communication with the modem. In addition, I wrote simple code that sends HTTP GET and POST requests to [webhook.site](https://webhook.site). Here is a breakdown of the tasks performed:

## Tasks Completed

### 1. Improvements

- **Automatic Serial Port Recognition:** Serial port detection process has been improved by using `vid` and `pid` values instead of serial port description.

- **Values Returned from Functions:** The functions are set to return an object containing the values ​​`status`, `data`(for responses containing data only), `message`. This process was developed with the thought that it would be quite functional in data exchange during the continuation of the project. For details visit [main.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/main.py)

```
# Port and baudrate values must be entered for an unknown device
modem = Modem()

modem.send_command("AT")
response = modem.read_response()

print("Response:", response)
```

```
![main](https://github.com/m19yurttutar/raspberry-pi-modem-communication/assets/76749251/071fb788-83e1-42b8-b1ee-262ccb7061a7)
```

- **Syntax Improvements:** The syntax has been revised in a way that makes the naming more understandable and easier to read.

### 2. Functional Development

- **HTTP GET and POST Requests:** Simple HTTP GET and POST requests have been added to the application. As can be seen in the code below, an AT command was sent to the modem and the read response was sent to the webhook.site API address with a POST request. The modem's response was obtained by reading the data of the last request sent with the GET request. For details visit [service.py](https://github.com/m19yurttutar/raspberry-pi-modem-communication/blob/master/service.py)

```
def post_data(json):
    url = f"https://webhook.site/{env['API_KEY']}"
    headers = {"accept": "application/json", "api-key": env["API_KEY"]}

    response = requests.post(url, json=json, headers=headers)

    return response.json()


def get_last_posted_data():
    url = f"https://webhook.site/token/{env['API_KEY']}/request/latest/raw"
    headers = {"content-type": "application/json"}

    response = requests.get(url, headers=headers)

    return response.json()
```

```
![service](https://github.com/m19yurttutar/raspberry-pi-modem-communication/assets/76749251/4bc19fba-b58d-4984-9091-fea539ec81f6)
```

## Next Steps

Looking ahead, the focus will be on:

- **Improvements:** By developing HTTP requests and integrating them into the modem, I will better detect the deficiencies in the Python library I wrote and finalize the library.

## References

1. [Webhook.site](https://webhook.site)

2. [Requests Documantation](https://requests.readthedocs.io)


## Conclusion

This week marked significant advancements in the project's Python library for modem communication. Key improvements included enhanced serial port recognition, refined function returns for streamlined data exchange, and syntax enhancements for improved readability. The addition of HTTP GET and POST requests to interact with webhook.site showcased the practical application of these developments.
