# HTTP Endpoint Health Checker

This Python program monitors the health of a list of HTTP endpoints provided in a YAML configuration file. It checks the availability of each endpoint every 15 seconds and logs the availability percentage for each domain based on the health checks over time.

## Features

- Monitors multiple HTTP endpoints.
- Checks if the endpoint is UP (responds with a 2xx status code and latency < 500ms).
- Logs the availability percentage of each domain after every 15-second test cycle.
- Supports HTTP GET and POST methods, with customizable headers and request bodies.

## Requirements

- Python 3.x
- `requests` library (Install using `pip install requests`)
- `PyYAML` library (Install using `pip install pyyaml`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/krishamehta09/Fetch_SRE.git

## Navigate to the project directory

## Install the required dependencies:
pip install -r requirements.txt

## Prepare a YAML configuration file listing the HTTP endpoints to monitor.

## Run the Python script with the path to the YAML configuration file:
python health_check.py endpoints.yaml

You will see the output on the terminal.
