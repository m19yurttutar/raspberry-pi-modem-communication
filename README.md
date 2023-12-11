# Raspberry Pi - Modem Communication Project Timeline

![Gantt Schema](https://github.com/m19yurttutar/raspberry-pi-modem-communication/assets/76749251/12811205-9b87-4c26-bfeb-f14e1e910200)

## Week 1-2: Modem Communication Library

- ### Week 1:

  - **Task 1:** Conduct research and initial work on automatic detection of the serial port.
  - **Task 2:** Develop a basic library using `pySerial` or similar to establish communication via the serial port.
  - **Task 3:** Enable sending AT commands and processing responses from the modem.

- ### Week 2:

  - **Task 4:** Implement functionality for customizing serial port settings.
  - **Task 5:** Create sample code for testing the library, debugging, and refining the functionality.

## Week 3-4: HTTP Requests

- ### Week 3:

  - **Task 6:** Develop code snippets to send HTTP GET requests to a `webhook.site`.
  - **Task 7:** Create examples demonstrating how to send HTTP requests through the modem using the communication library.

- ### Week 4:

  - **Task 8:** Write code to send HTTP POST requests and integrate it with the communication library.
  - **Task 9:** Test the functionality, perform debugging, and refine the code.

## Week 5: MQTT Communication

- **Task 10:** Develop sample code to send messages to an MQTT broker.
- **Task 11:** Subscribe to an MQTT topic via the modem and ensure the ability to read incoming messages.

## Week 6: Raspberry Pi Internet Connection and Comparison

- **Task 12:** Establish internet connections using PPP, QMI/RMNET, and ECM protocols on the Raspberry Pi via the modem.
- **Task 13:** Measure connection speeds and conduct a comparative analysis of the protocols.
