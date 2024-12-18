import os
import django
import time

# Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FermentationController.settings")
django.setup()

from core.controllers import update_sensors, update_inputs_and_relays, regulate_temperature

def main():
    """
    Main function to run the fermentation controller in real-time.
    """
    print("Starting fermentation controller...")
    try:
        while True:
            print("Updating sensors...")
            update_sensors()

            print("Updating digital inputs and relays...")
            update_inputs_and_relays()

            print("Regulating temperature...")
            regulate_temperature()

            print("Cycle completed. Waiting for next cycle...")
            time.sleep(0.1)  # Wait for 1 seconds before the next cycle

    except KeyboardInterrupt:
        print("Shutting down safely...")

if __name__ == "__main__":
    main()