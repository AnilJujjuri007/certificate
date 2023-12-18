from flask import Flask, request, jsonify, render_template
from opcua import Client
from opcua import ua
import os

app = Flask(__name__)

# Specify the OPC UA server endpoint
# opcua_endpoint = "opc.tcp://BLRTSL00330.lnties.com:53530/OPCUA/SimulationServer"

# Function to determine the type of a node and retrieve its value
def get_node_type_and_value(client, node):
    try:
        if node.get_node_class() == ua.NodeClass.Object:
            children = node.get_children()
            result = {"object": str(node.get_browse_name()), "children": []}
            for child in children:
                result["children"].append(get_node_type_and_value(client, child))
            return result
        elif node.get_node_class() == ua.NodeClass.Variable:
            value = node.get_value()
            result = {
                "node_name": node.get_browse_name().Name,
                "node_id": str(node.nodeid),
                "value": str(value) if value is not None else None,
            }
            return result
    except Exception as e:
        return("err",e)

# Function to process a CSV file
def process_csv(file_path):
    results = []
    try:
        with open(file_path, 'r') as csvfile:
            for row in csvfile:
                node_info = row.strip().split(',')
                if len(node_info) == 2:
                    node_id, connection_address = node_info
                    try:
                        with Client(connection_address) as client:
                            client.connect()
                            node = client.get_node(node_id)
                            result = get_node_type_and_value(client, node)
                            results.append(result)
                    except Exception as e:
                        error_msg = f"Error reading node {node_id} from {connection_address}: {str(e)}"
                        results.append({"error": error_msg})
    except Exception as e:
        error_msg = f"Error processing CSV file: {str(e)}"
        results.append({"error": error_msg})
    return results

# API endpoint to process CSV and retrieve OPC UA data
@app.route('/process_opcua_csv', methods=['POST'])
def process_opcua_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    file.save("uploaded_file.csv")
    csv_file_path = "uploaded_file.csv"
    results = process_csv(csv_file_path)
    return jsonify({"results": results})

# Route to render the file upload form
# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)