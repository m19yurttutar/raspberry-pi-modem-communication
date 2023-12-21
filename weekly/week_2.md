# Project Progress Report - Week 2

## Project Overview

This week I focused on setting up the necessary tools to develop efficient software on the Raspberry Pi platform. I added basic functions such as connection management, sending commands, reading responses and automatic serial port recognition. Here is a breakdown of the tasks performed:

## Tasks Completed

### 1. Setting up Version Control System, IDE, and Plugins

- **Version Control System:** Implemented Git for version control, ensuring a systematic approach to tracking changes in the project.

- **IDE Selection:** Utilized Geany as the primary Integrated Development Environment (IDE) due to its compatibility and built-in functionality for Raspberry Pi.

- **GeanyVC Plugin:** Integrated the GeanyVC plugin within Geany to streamline version control operations directly within the IDE.

### 2. Functional Development

- **Connection Management:** Established basic functions to manage connections effectively, facilitating seamless interaction with external devices or systems.

- **Command Transmission:** Implemented functionalities enabling the sending of commands to connected devices or systems from the Raspberry Pi.

- **Response Reading:** Developed mechanisms for reading and processing responses received from external devices or systems after command transmission.

- **Automatic Serial Port Recognition:** Implemented a method for automatic port discovery to identify and connect with serial ports without manual intervention.

### Ekstra: Automatic Port Discovery Explanation

To achieve automatic port discovery, I utilized Python's `PySerial` library. The process involves:

1. **Enumerating Available Ports:** The system scans through available serial ports using the `serial.tools.list_ports.comports()` function to identify connected devices.

2. **Port Recognition:** Utilizing specific attributes or characteristics (such as the device name, manufacturer, or other identifiable parameters), the system matches the desired port for connection.

3. **Dynamic Port Selection:** The system dynamically selects the appropriate port, ensuring seamless communication without the need for manual port specification.

This automated process enhances usability by eliminating the need for users to manually configure port settings, enhancing the overall user experience.

## Challenges Faced

- The primary challenge encountered during automatic port discovery was ensuring robust and reliable recognition across various device configurations. Fine-tuning the recognition mechanism to accommodate different setups was necessary for improved compatibility.

## Next Steps

Looking ahead, the focus will be on:

- **Refinement:** Refining the automatic port discovery mechanism to enhance its accuracy and reliability across diverse hardware setups.

- **Feature Expansion:** Adding additional functionalities for improved command handling and response processing, enhancing the project's capabilities.

## References

1. [Python PySerial Documentation](https://pyserial.readthedocs.io/en/latest/)

2. [Minicom Documantation](https://linux.die.net/man/1/minicom)

3. [Geany IDE Website](https://www.geany.org)

## Conclusion

This week marked significant progress in establishing a robust development environment for Raspberry Pi based projects. The integration of version control, IDE setup, and the implementation of essential functionalities lays a strong foundation for future developments.
