from opcua import Client
from azure.iot.device import IoTHubModuleClient, Message
import json
import time

# Azure IoT Hub connection string
CONNECTION_STRING = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=edgeDevive-opcua;SharedAccessKey=jiDsujbUvP2MySzcHAg+eDYEKf97zrh+YTqM6sGjkQU="

def send_to_iothub(data, edge_client, message):
    try:
        message = Message(json.dumps(data))
        edge_client.send_message_to_output(message, "modbusdata")
        print(f"Successfully sent data to IoT Hub: {data}")
    except Exception as e:
        print(f"Error sending data to IoT Hub: {str(e)}")

def collect_opcua_data(device_properties, edge_client, message):
    try:
        with Client(device_properties["connection"]["ipAddress"]) as client:
            client.connect()

            while True:
                for signal_name, signal_info in device_properties["signals"].items():
                    node_id = f"ns=2;s={signal_info['address']}"
                    value = client.get_node(node_id).get_value()

                    data_to_send = {
                        signal_name: value
                    }

                    send_to_iothub(data_to_send, edge_client, message)
                    time.sleep(int(signal_info["interval"]) / 1000)

    except KeyboardInterrupt:
        print("Closing OPC UA client...")

if __name__ == '__main__':
    try:
        module_client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)
        module_client.connect()

        message = Message()

        twin = {
            "properties": {
                "desired": {
                    "devices": {
                        "c2b2de33f8bf900fc795a323d2d3c13a": {
                            "connection": {
                                "ipAddress": "192.168.101.72",
                                "port": "502",
                                "slaveId": "1"
                            },
                            "signals": {
                                "current": {
                                    "address": "2",
                                    "interval": "1000",
                                    "length": "1",
                                    "name": "current",
                                    "unitId": "1"
                                },
                                "energy": {
                                    "address": "0",
                                    "interval": "1000",
                                    "length": "2",
                                    "name": "energy",
                                    "unitId": "1"
                                },
                                "power": {
                                    "address": "3",
                                    "interval": "1000",
                                    "length": "2",
                                    "name": "power",
                                    "unitId": "1"
                                },
                                "voltage": {
                                    "address": "1",
                                    "interval": "1000",
                                    "length": "1",
                                    "name": "voltage",
                                    "unitId": "1"
                                }
                            }
                        }
                    }
                }
            }
        }

        twin_properties = twin["properties"]["desired"]["devices"]["c2b2de33f8bf900fc795a323d2d3c13a"]
        if twin_properties:
            collect_opcua_data(twin_properties, module_client, message)
        else:
            print("No twin properties found.")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        module_client.disconnect()
