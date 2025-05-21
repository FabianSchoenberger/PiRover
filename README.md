# PiRover

**PiRover** is a Wi-Fi-controlled smart vehicle based on the [Freenove Three-Wheeled Smart Car Kit for Raspberry Pi](https://www.freenove.com/). We use the hardware from the kit but implement our own custom software.

## Features

- Control via a web UI built with **Svelte** and **TailwindCSS**
- Real-time communication using **MQTT** and **WebSockets**
- Live camera streaming to the browser
- Control of LEDs, buzzer, and motors via **Python scripts** on a **Raspberry Pi 4**

## Structure

```text
/
├── doc/         # LaTeX documentation
├── proposal/    # Project proposal (LaTeX)
├── rover/       # Python scripts for hardware control
├── web/         # Svelte frontend project