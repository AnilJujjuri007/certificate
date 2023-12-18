from opcua import Client
from azure.iot.device import IoTHubModuleClient, Message
import json
import asyncio
import paho.mqtt.client as mqtt

# Define module-level variables
opcua_client = None
mqtt_client = None

async def send_to_iothub(data, edge_client, message):
    try:
        message = Message(json.dumps(data))
        await edge_client.send_message_to_output(message, "opcuadata")
        print(f"Successfully sent data to IoT Hub--->  {data}")
    except Exception as e:
        print("Error sending data to IoT Hub:", str(e))

async def collect(twin, edge_client, message):
    try:
        devices = twin['devices']
        for device_id, device_properties in devices.items():
            server_url = device_properties["connection"]["ipAddress"]
            signals = device_properties['signals']
            mqtt_broker_address = device_properties.get("mqttBrokerAddress", "")
            mqtt_topic = device_properties.get("mqttTopic", "")

        global opcua_client
        with Client(server_url) as opcua_client:
            opcua_client.connect()
            print("Connected to OPC UA server!")
            print(signals)

            for signal_name, signal_info in signals.items():
                node_id = signal_info["address"]
                value = opcua_client.get_node(node_id).get_value()

                data_to_send = {signal_name: value}
                await send_to_iothub(data_to_send, edge_client, message)

                # Publish data to MQTT broker
                global mqtt_client
                mqtt_payload = json.dumps(data_to_send)
                mqtt_client.publish(mqtt_topic, mqtt_payload)
                print(f"Published data to MQTT broker---> {data_to_send}")

                await asyncio.sleep(int(signal_info["interval"]) / 1000)

    except KeyboardInterrupt:
        print("Closing OPC UA client...")

def on_mqtt_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

def on_mqtt_disconnect(client, userdata, rc):
    print(f"Disconnected from MQTT broker with result code {rc}")

async def set_connection(twin_obj, edge_client, message):
    global opcua_client
    global mqtt_client

    my_edge_client = edge_client
    my_message = message
    global twin
    twin = twin_obj

    if twin:
        twin = twin_obj
        time.sleep(1)
        print("Starting data acquisition task")

        # MQTT Configuration
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_mqtt_connect
        mqtt_client.on_disconnect = on_mqtt_disconnect

        mqtt_broker_address = twin.get("mqttBrokerAddress", "")
        mqtt_broker_port = twin.get("mqttBrokerPort", 1883)
        mqtt_client.connect(mqtt_broker_address, mqtt_broker_port, 60)
        mqtt_client.loop_start()

        await collect(twin, my_edge_client, my_message)
    else:
        twin = twin_obj

    print("Updated twin")

# Other code...

# Close connections when the module is terminated
def module_termination_handler(signal, frame):
    global opcua_client
    global mqtt_client
    if opcua_client:
        opcua_client.disconnect()
    if mqtt_client:
        mqtt_client.disconnect()
    print("IoT Hub Client sample stopped by Edge")

# Set the Edge termination handler
signal.signal(signal.SIGTERM, module_termination_handler)

# Other code...
