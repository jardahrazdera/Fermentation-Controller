import requests
import json

EVOK_BASE_URL = "http://192.168.2.77:8080/json"


class EvokClient:
    def __init__(self, base_url=EVOK_BASE_URL):
        self.base_url = base_url

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


# Test
if __name__ == "__main__":
    client = EvokClient()

    sensor_circuit = "2870F55704E13DC0"
    temp = client.get_temperature(sensor_circuit)
    print(f"Temperature for circuit {sensor_circuit}: {temp} °C")

    relay_circuit = "2_01"
    result = client.set_relay(relay_circuit, 1)
    print(f"Relay {relay_circuit} set to ON: {'Success' if result else 'Failed'}")