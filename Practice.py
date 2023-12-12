from azure.iot.device import IoTHubModuleClient, Message
from opcua import Client
import json
import time

# Azure IoT Hub connection string
CONNECTION_STRING = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=edgeDevive-opcua;SharedAccessKey=jiDsujbUvP2MySzcHAg+eDYEKf97zrh+YTqM6sGjkQU="

def send_to_iothub(data, edge_client, message):
    try:
        message = Message(json.dumps(data))
        edge_client.send_message_to_output(message, "opcua_data")
        print(f"Successfully sent OPC UA data to IoT Hub: {data}")
    except Exception as e:
        print(f"Error sending OPC UA data to IoT Hub: {str(e)}")

def collect_opcua_data(device_properties, edge_client, message, signal_addresses):
    try:
        with Client(device_properties["connection"]["serverUrl"]) as client:
            client.connect()

            while True:
                for signal_name, signal_info in device_properties["signals"].items():
                    node_id = signal_info["address"]
                    value = client.get_node(node_id).get_value()

                    data_to_send = {
                        signal_name: value
                    }

                    send_to_iothub(data_to_send, edge_client, message)
                    time.sleep(int(signal_info["interval"]) / 1000)

                # Update the set of signal addresses
                signal_addresses.update(signal_info['address'] for signal_info in device_properties["signals"].values())

    except KeyboardInterrupt:
        print("Closing OPC UA client...")

def get_twin_properties(module_client):
    twin_properties = module_client.get_twin()
    desired_properties = twin_properties["properties"]["desired"]
    return desired_properties.get("devices", {})

if __name__ == '__main__':
    try:
        module_client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)
        module_client.connect()

        message = Message()

        signal_addresses = set()

        while True:
            twin_properties = get_twin_properties(module_client)
            if twin_properties:
                for device_id, device_properties in twin_properties.items():
                    collect_opcua_data(device_properties, module_client, message, signal_addresses)
            else:
                print("No twin properties found.")

            print("All Signal Addresses:", signal_addresses)

            time.sleep(60)  # Poll every 60 seconds for twin updates

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        module_client.disconnect()
