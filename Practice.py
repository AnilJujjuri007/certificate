import BAC0
import json
import time
from azure.iot.device import IoTHubDeviceClient, Message
import socket
# Azure IoT Hub connection information
iothub_connection_string = "Your Azure IoT Hub Connection String"
device_id = "Your Device ID"
data={}
hostname = socket.gethostname()    
ip_adr = socket.gethostbyname(hostname)
# create a BACnet connection to connect to the devices
bacnet = BAC0.lite(ip=ip_adr, port=47809)
 
def send_to_azure_iot_hub(data):
    try:
        # Create an Azure IoT Hub device client
        device_client = IoTHubDeviceClient.create_from_connection_string("HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=menderclient;SharedAccessKey=Sjr8fBZiUYQwksGYpyzlySO8WrnqkkartEbfTQhlo68=")
 
        # Connect to the Azure IoT Hub
        device_client.connect()
 
        # Convert BACnet data to JSON
        json_data = json.dumps(data)
 
        # Create a message to send to Azure IoT Hub
        message = Message(json_data)
 
        # Send the message to Azure IoT Hub
        device_client.send_message(message)
 
        print("Message sent to Azure IoT Hub:", json_data)
 
        # Disconnect from Azure IoT Hub
        device_client.disconnect()
 
    except Exception as e:
        print("Error sending message to Azure IoT Hub:", str(e))
 
def main():
    while True:
        # Reading 3 Objects from the Bacnet Simulator
        for x in range(0, 3):
            id = str(x)
            ip="192.168.0.105:49689"
            # Connect to the BACnet simulator using the IP address and port number
            value = bacnet.read(ip+" analogInput " + id + " presentValue")
            value = str(value)
            data["Analog_input" + id] = value
 
        # print(json.dumps(data, indent=2))
 
        # Send the BACnet data to Azure IoT Hub
        send_to_azure_iot_hub(data)
 
        time.sleep(5)
 
# RUN main
if __name__ == '__main__':
    main()
