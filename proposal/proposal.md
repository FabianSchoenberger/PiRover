# Project Proposal - PiRover

Group 5

kxxxxxxxx, Olivotto Philipp \
kxxxxxxxx, Pichler Alexander \
k12308997, Schoenberger Fabian \
kxxxxxxxx, Siala Alexander

## Description

In this project, we aim to design and develop 'PiRover', a remote-controlled vehicle containing various sensors and actuators leveraging Raspberry Pi technology.
The goal is to control the vehicle in real-time, no matter the location, as long as it is connected to the internet.

### The vehicle

Although the technical basis of our project will be a Raspberry Pi, we will also need a vehicle to put it on top of. 
Since the hardware list does not contain such a vehicle, and we do not expect the institute to provide one, we will to order one as soon as our proposal gets approved. 
The specific model we have in mind is listed down below in our hardware list. 
The vehicle will have to be assembled by us with the help of a manual. 

### Actuators

The vehicle will have the following actuators:
- Two motors to drive the vehicle.
- A motor to turn the camera.
- Rear light(s) to indicate slowing down or driving backwards.
- Front light(s) to illuminate the path when it is dark.

### Sensors

For sensors, we plan for our PiRover to have a few:
- A camera to be able to see a live feed of what is in front of the vehicle.
- An ultrasonic sensor for measuring distances which will assist the driver when driving backwards. 
The application will display a warning if the vehicle is about to bump into anything.
- An accelerometer which can be used to display the current speed of the vehicle to the driver.
Its data can also be used to activate the rear light(s) when required.
- A brightness sensor to be able to automatically turn on the front light(s) of the vehicle when it gets too dark.

### Web Interface

The PiRover will be remotely controlled via a Web-Interface. 
The interface will show a live feed of the camera and allows for the control of the vehicle's acceleration and steering. 
Furthermore, the front lights can be overridden to be permanently on or off.
In addition, the driver will be given important information like speed, acceleration and information whether something is behind the vehicle.

The vehicle will be controlled via standard WASD + arrow keys controls and will optionally support a Gamepad.

It will be developed using Svelte.

### Sensor Data Processing with UI Interface for Data Exploration

As part of the project, we implement a Grafana-based user interface running on a Raspberry Pi, which connects to a local PostgreSQL database for data visualization. 
The data is continuously sent from the PiRover, which publishes sensor and actuator information — including motor status, ultrasonic distance readings, accelerometer data, and binary light sensor states (on/off). 
Additionally, the rover broadcasts a high-level status tag indicating its current mode (like idle, exploring, or obstacle detected). This data is structured into dedicated tables for each sensor and actuator, within the PostgreSQL database. 
With Grafana, users can interactively explore this historical data and identify behavioral patterns over time—for example, analyzing the correlation between ultrasonic sensor readings and the rover’s obstacle detection mode to assess its responsiveness and decision-making logic. 
Also, a total distance traveled by the rover can be calculated and displayed in the UI. This setup not only enhances the user experience but also provides valuable insights into the rover's performance and behavior.

## System Architecture

We are planning to have two devices communicating with each other.
- One will be responsible for reading sensor data and controlling actuators.
Additionally, it will publish relevant sensor data to the broker and subscribe to driving inputs.
- Another will be the MQTT broker and web server for the Web Interface.

Technically, a third point of contact is involved: the browser from which the application is opened.

![Architecture](img/architecture.png)

To ensure full mobility while still being connected to the internet, we are going to connect the vehicle's Raspberry Pi to Wi-Fi.

## Hardware List

| part              | further information                                                                                                                    | requested |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------|-----------|
| 2x Raspberry Pi   |                                                                                                                                        | yes       |
| vehicle           | [Freenove Three-Wheeled Smart Car Kit for Raspberry Pi](https://amzn.eu/d/hJ5U5ri) <br/> includes motors, camera and ultrasonic sensor | no        |
| battery pack      |                                                                                                                                        | yes       |
| lights            | at least 1x white and 1x red                                                                                                           | ?         |
| accelerometer     |                                                                                                                                        | yes       |
| brightness sensor |                                                                                                                                        | ?         |

## Fulfillment of Project Requirements

//TODO

## Timeline

//TODO
