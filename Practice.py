from opcua import Client

# Specify the OPC UA server endpoint
opcua_endpoint = "opc.tcp://BLRTSL00330.lnties.com:53530/OPCUA/SimulationServer"

# Function to recursively explore and retrieve data from nodes
def retrieve_node_hierarchy(node, depth=0):
    print(node)
    try:
        # Connect to the OPC UA server
        with Client(opcua_endpoint) as client:
            client.connect()

            # Read the value of the current node
            value = node.get_value()
            print(f"{'  ' * depth}Node: {node.get_browse_name()}. Value: {value}")

            # If the node has children, explore them
            children = node.get_children()
            for child in children:
                retrieve_node_hierarchy(child, depth + 1)
    except Exception as e:
        print(f"Error: {str(e)}")

try:
    # Create a client connection
    client = Client(opcua_endpoint)
    client.connect()

    # Get the root node using the specified node ID
    root_node = "ns=0;i=85"
    retrieve_node_hierarchy(root_node)

except Exception as e:
    print(f"Error connecting to the OPC UA server: {str(e)}")

# Ensure to disconnect from the OPC UA server at the end
client.disconnect()

ns=0;i=85
Error: 'str' object has no attribute 'get_value'