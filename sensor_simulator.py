import json
import random
import time

from awscrt import mqtt
from awsiot import mqtt_connection_builder

from config import (
    ENDPOINT,
    CERT_PATH,
    KEY_PATH,
    CA_PATH,
    CLIENT_ID,
    TOPIC,
)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    port=8883,
    cert_filepath=CERT_PATH,
    pri_key_filepath=KEY_PATH,
    ca_filepath=CA_PATH,
    client_id=CLIENT_ID,
)

print("Connecting...")
mqtt_connection.connect().result()

print("Connected. Publishing readings every 10 seconds.")

moisture = 25

try:
    while True:
        moisture += random.uniform(-8, 3)
        moisture = max(5, min(95, moisture))

        payload = {
            "device_id": CLIENT_ID,
            "moisture_pct": round(moisture, 1),
            "timestamp": int(time.time())
        }

        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(payload),
            qos=mqtt.QoS.AT_LEAST_ONCE,
        )

        print("Published:", payload)

        time.sleep(10)

except KeyboardInterrupt:
    print("\nDisconnecting...")
    mqtt_connection.disconnect().result()
    print("Disconnected.")