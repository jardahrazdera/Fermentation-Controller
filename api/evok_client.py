import requests
import json

EVOK_BASE_URL = "http://192.168.2.77:8080/json"


class EvokClient:
    def __init__(self, base_url=EVOK_BASE_URL):
        self.base_url = base_url

    def get_sensor_status(self, circuit):
        """
        Checks the status of the sensor, including the 'lost' attribute from EVOK API.
        :param circuit: The circuit ID of the sensor.
        :return: True if the sensor is 'lost', False otherwise.
        """
        url = f"{self.base_url}/temp/{circuit}"
        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            return data.get("lost", False)
        except requests.RequestException as e:
            print(f"Error fetching status for sensor {circuit}: {e}")
            return True  # Treat as 'lost' in case of an error

    def get_temperature(self, circuit):
        url = f"{self.base_url}/temp/{circuit}"
        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            return data.get("value")
        except (requests.RequestException, KeyError) as e:
            print(f"Error reading temperature for circuit {circuit}: {e}")
            return None

    def set_relay(self, circuit, value):
        url = f"{self.base_url}/ro/{circuit}"
        payload = {"value": value}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error setting relay {circuit} to {value}: {e}")
            return False

    def get_digital_input_state(self, circuit):
        """
        Reads the state of a digital input from EVOK API.
        :param circuit: The circuit ID of the digital input (e.g., '1_01').
        :return: True if active, False if inactive, or None on error.
        """
        url = f"{self.base_url}/di/{circuit}"
        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            return data.get("value", False)
        except requests.RequestException as e:
            print(f"Error reading digital input state for circuit {circuit}: {e}")
            return None

    def get_relay_state(self, circuit):
        """
        Reads the state of a relay from EVOK API.
        :param circuit: The circuit ID of the relay (e.g., '1_01').
        :return: True if active, False if inactive, or None on error.
        """
        url = f"{self.base_url}/ro/{circuit}"
        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            return data.get("value", False)
        except requests.RequestException as e:
            print(f"Error reading relay state for circuit {circuit}: {e}")
            return None


# Test
if __name__ == "__main__":
    client = EvokClient()

    # Test temperature reading
    sensor_circuit = "2870F55704E13DC0"
    temp = client.get_temperature(sensor_circuit)
    print(f"Temperature for circuit {sensor_circuit}: {temp} °C")

    # Test relay setting
    relay_circuit = "2_01"
    result = client.set_relay(relay_circuit, 1)
    print(f"Relay {relay_circuit} set to ON: {'Success' if result else 'Failed'}")