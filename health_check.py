import time
import requests
import yaml
import logging
import sys
from urllib.parse import urlparse
from collections import defaultdict

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to load endpoints from YAML file
def load_endpoints(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

# Function to send a well-formed HTTP request based on the YAML entry
def send_request(endpoint):
    method = endpoint.get('method', 'GET').upper()  # Default to GET if method is missing
    url = endpoint['url']
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        # Measure response time
        start_time = time.time()

        # Sending GET or POST request based on the method
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=5)
        else:
            response = requests.request(method, url, headers=headers, data=body, timeout=5)

        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert latency to milliseconds

        # Check if response status is in the 2xx range and latency is under 500 ms
        if 200 <= response.status_code < 300 and latency < 500:
            return True, latency  # UP
        else:
            return False, latency  # DOWN

    except requests.RequestException:
        return False, None  # DOWN due to request failure

# Function to monitor the health of endpoints and calculate availability percentage per domain
def monitor_endpoints(endpoints):
    success_count_per_domain = defaultdict(int)
    total_count_per_domain = defaultdict(int)

    while True:
        for endpoint in endpoints:
            # Extract the domain name from the URL
            domain = urlparse(endpoint['url']).netloc

            total_count_per_domain[domain] += 1
            is_up, latency = send_request(endpoint)

            if is_up:
                success_count_per_domain[domain] += 1

        # After each cycle, calculate the availability percentage for each domain
        for domain in total_count_per_domain:
            success_count = success_count_per_domain[domain]
            total_count = total_count_per_domain[domain]
            availability_percentage = round((success_count / total_count) * 100)

            # Log domain availability
            logging.info(f"{domain} has {availability_percentage}% availability percentage")

        # Sleep for 15 seconds before the next test cycle
        time.sleep(15)

# Main function to read file path and start monitoring
def main(file_path):
    endpoints = load_endpoints(file_path)
    logging.info("Starting health check for the following domains:")
    for endpoint in endpoints:
        domain = urlparse(endpoint['url']).netloc
        logging.info(f"Domain: {domain}, Endpoint Name: {endpoint['name']}, URL: {endpoint['url']}")

    monitor_endpoints(endpoints)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python health_checker.py <path_to_yaml_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    main("endpoints.yaml")

