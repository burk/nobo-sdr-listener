from __future__ import annotations
import time
import argparse
from packets.packet import Packet
from paho.mqtt import client as mqtt_client

TOPIC = "nobo-test"
CLIENT_ID = "nobo-test"

def connect_mqtt(broker: str, port: int) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def main(filename: str, broker: str | None, port: int) -> None:
    client = None
    if broker is not None:
        client = connect_mqtt(broker, port)
        client.loop_start()
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if line is not None and line != "":
                tokens = line.split(",")
                data = tokens[2][5:]
                try:
                    packet = Packet.from_hex(data)
                except Exception:
                    continue
                print(packet)
                if client:
                    client.publish(f"{TOPIC}/{packet.type_str()}/{packet.from_addr()}", packet.to_json())
            else:
                time.sleep(0.2)
    if client:
        client.loop_stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, required=True)
    parser.add_argument("--mqtt-host", type=str, required=False)
    parser.add_argument("--mqtt-port", type=int, default=1883)
    args = parser.parse_args()
    main(args.filename, args.mqtt_host, args.mqtt_port)
