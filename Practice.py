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
