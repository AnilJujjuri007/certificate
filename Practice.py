from opcua import Client
from opcua import ua

# Specify the OPC UA server endpoint
opcua_endpoint = "opc.tcp://BLRTSL00330.lnties.com:53530/OPCUA/SimulationServer"

# Function to determine the type of a node
def get_node_type(node):
    if node.get_node_class() == ua.NodeClass.Object:
        children = node.get_children()
        # print(children)

        print(f"{node.get_browse_name()} is an object following child nodes:")
        for child in children:
            node_type = get_node_type(child)
            # print(f"-{child.get_browse_name()} is a {node_type}")

    elif node.get_node_class() == ua.NodeClass.Variable:
        value = node.get_value()
        print(f"Node Name: {node.get_browse_name().Name}, NodeId: {node.nodeid}, Value: {value}")



with open('nodes.csv', 'r') as csvfile:
    for row in csvfile:
        node_id = row.strip()

        try:
            with Client(opcua_endpoint) as client:
                client.connect()
                node = client.get_node(node_id)

                node_type = get_node_type(node)
                print(f"{node_id} is a {node_type}")
        except Exception as e:
            print(f"Error reading node {node_id}: {str(e)}")


