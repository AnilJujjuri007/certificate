from opcua import Client
from opcua import ua

# Specify the OPC UA server endpoint
opcua_endpoint = "opc.tcp://BLRTSL00330.lnties.com:53530/OPCUA/SimulationServer"

# Function to determine the type of a node
def get_node_type(node):
    if node.get_node_class() == ua.NodeClass.Object:
        children = node.get_children()
        print(children)
        print(f"{node.get_browse_name()} is an object following child nodes:")
        for child in children:
            print(f"-{child.get_browse_name()}")
    elif node.get_node_class() == ua.NodeClass.Variable:
        value = node.get_value()
        #print(f"Node Name: {node.get_browse_name().Name}, NodeId: {node.nodeid}, Value: {value}")
        return "Variable"
    elif node.get_node_class() == ua.NodeClass.Folder:
        return "Folder"
    else:
        return "Unknown"  # You can extend this for other node types

# Read nodes from the CSV file
with open('nodes.csv', 'r') as csvfile:
    for row in csvfile:
        node_id = row.strip()  # Assuming each line in the CSV contains a node ID

        try:
            with Client(opcua_endpoint) as client:
                client.connect()
                node = client.get_node(node_id)

                node_type = get_node_type(node)
                print(f"{node_id} is a {node_type}")
        except Exception as e:
            print(f"Error reading node {node_id}: {str(e)}")
            
            
Error reading node Node: ('Error parsing string Node', ValueError('not enough values to unpack (expected 2, got 1)'))
ns=3;i=1001 is a Variable
ns=3;i=1002 is a Variable
ns=3;i=1003 is a Variable
ns=3;i=1004 is a Variable
ns=3;i=1005 is a Variable
ns=3;i=1006 is a Variable
ns=3;i=1007 is a Variable
[Node(FourByteNodeId(ns=3;i=1009)), Node(FourByteNodeId(ns=3;i=1010)), Node(FourByteNodeId(ns=3;i=1015))]
QualifiedName(3:energymeter) is an object following child nodes:
-QualifiedName(3:plc)
-QualifiedName(3:Data)
-QualifiedName(3:voltage)
ns=3;i=1008 is a None
Error reading node : Could not find identifier in string: 