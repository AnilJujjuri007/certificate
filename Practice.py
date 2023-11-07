from opcua import Client

# Specify the OPC UA server endpoint
<<<<<<< HEAD
opcua_endpoint = "opc.tcp://BLRTSL00330.lnties.com:53530/OPCUA/SimulationServer"

# Function to recursively explore and retrieve data from nodes
def retrieve_node_hierarchy(node, depth=0):
    print(node)
=======
opcua_endpoint = "opc.tcp://your_opcua_server_endpoint"

# Function to recursively explore and retrieve data from nodes
def retrieve_node_hierarchy(node, depth=0):
>>>>>>> 43529ee2a66665f72a35e0f466110d53cabc0a29
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
<<<<<<< HEAD
    root_node = "ns=0;i=85"
=======
    root_node = client.get_root_node()
>>>>>>> 43529ee2a66665f72a35e0f466110d53cabc0a29
    retrieve_node_hierarchy(root_node)

except Exception as e:
    print(f"Error connecting to the OPC UA server: {str(e)}")

# Ensure to disconnect from the OPC UA server at the end
client.disconnect()
<<<<<<< HEAD


ns=0;i=85
Error: 'str' object has no attribute 'get_value'
=======
#############

from opcua import Client

# Specify the OPC UA server endpoint
opcua_endpoint = "opc.tcp://your_opcua_server_endpoint"

# Function to check if a node has child nodes
def has_child_nodes(node):
    return len(node.get_children()) > 0

# Function to check if a node is an object
def is_object(node):
    return node.get_node_class() == "Object"

# Read nodes from the CSV file
with open('nodes.csv', 'r') as csvfile:
    for row in csvfile:
        node_id = row.strip()  # Assuming each line in the CSV contains a node ID

        try:
            with Client(opcua_endpoint) as client:
                client.connect()
                node = client.get_node(node_id)
                
                if has_child_nodes(node):
                    print(f"{node_id} has child nodes.")
                elif is_object(node):
                    print(f"{node_id} is an object.")
                else:
                    print(f"{node_id} is neither an object nor has child nodes.")
        except Exception as e:
            print(f"Error reading node {node_id}: {str(e)}")

>>>>>>> 43529ee2a66665f72a35e0f466110d53cabc0a29
