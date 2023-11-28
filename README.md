# UdL -> IoT Project
Practice 1 - Distributed Computing
## Overview
Welcome to the IoT Application, a robust solution for managing and processing data from Internet of Things (IoT) devices. This Python-based application utilizes the MQTT protocol for efficient communication between devices and a gateway. Data is further processed and distributed using the Apache Kafka messaging system for seamless integration with microservices, all wrapped in Docker containers for easy deployment.

## Features

- **MQTT Communication:** Devices communicate with the system using the MQTT protocol, ensuring lightweight and efficient data transfer.

- **Gateway Integration:** A Python-based gateway collects and aggregates data from multiple devices, acting as a bridge between the devices and the central processing system.

- **Kafka Integration:** Data received by the gateway is sent to a Kafka broker for reliable and scalable data streaming. This enables seamless integration with microservices and real-time data processing.

- **Microservices:** Leverage the power of microservices to process and analyze data in a modular and scalable manner.

- **Docker Containers:** Easily deploy and scale the application using Docker containers.
  
## Usage

1. Clone the project
   ```bash
    git clone https://github.com/aleex0309/EPS-COMPUDIST-IoT
    ```

2. Start the Dockers

    ```bash
    docker compose up --build
    ```

## Authors
- Marc Gaspà Joval - [@marcgj](https://github.com/marcgj)
- Alexandru Cristian Stoia - [@aleex0309](https://github.com/aleex0309)
