import tkinter as tk
from tkinter import filedialog
from opcua import Client
from opcua import ua

# Specify the OPC UA server endpoint
opcua_endpoint = "opc.tcp://BLRTSL00330.lnties.com:53530/OPCUA/SimulationServer"

# Function to determine the type of a node
def get_node_type(node):
    if node.get_node_class() == ua.NodeClass.Object:
        children = node.get_children()
        print(f"{node.get_browse_name()} is an object having following child nodes:")
        for child in children:
            node_type = get_node_type(child)

    elif node.get_node_class() == ua.NodeClass.Variable:
        value = node.get_value()
        print(f"Node Name: {node.get_browse_name().Name}, NodeId: {node.nodeid}, Value: {value}")

# Function to upload and process a CSV file
def upload_and_process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            with Client(opcua_endpoint) as client:
                client.connect()
                with open(file_path, 'r') as csvfile:
                    for row in csvfile:
                        node_id = row.strip()
                        try:
                            node = client.get_node(node_id)
                            node_type = get_node_type(node)
                            print(f"{node_id} is a {node_type}")
                        except Exception as e:
                            print(f"Error reading node {node_id}: {str(e)}")
                # Disconnect the OPC UA client after processing
                client.disconnect()
        except Exception as e:
            print(f"Error connecting to the OPC UA server: {str(e)}")

# Create a Tkinter window
window = tk.Tk()
window.title("CSV File Upload and OPC UA Processing")

# Create a button to trigger the file upload and processing
upload_button = tk.Button(window, text="Upload CSV File and Process", command=upload_and_process_csv)
upload_button.pack()

# Start the Tkinter main loop
window.mainloop()