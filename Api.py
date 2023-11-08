from flask import Flask, request, jsonify
from flask import send_file
from opcua import Client
from opcua import ua
import tempfile
import os

app = Flask(__name)

# Specify the OPC UA server endpoint
opcua_endpoint = "opc.tcp://BLRTSL00330.lnties.com:53530/OPCUA/SimulationServer"

# Function to determine the type of a node
def get_node_type(node):
    if node.get_node_class() == ua.NodeClass.Object:
        children = node.get_children()
        node_info = {
            "node_name": node.get_browse_name().Name,
            "node_id": node.nodeid.to_string(),
            "node_type": "Object",
            "children": [get_node_type(child) for child in children]
        }
        return node_info

    elif node.get_node_class() == ua.NodeClass.Variable:
        value = node.get_value()
        node_info = {
            "node_name": node.get_browse_name().Name,
            "node_id": node.nodeid.to_string(),
            "node_type": "Variable",
            "value": value
        }
        return node_info

# API endpoint to upload and process a CSV file
@app.route('/process_csv', methods=['POST'])
def process_csv():
    try:
        file = request.files['csv_file']
        if file and file.filename.endswith('.csv'):
            # Create a temporary directory to save the uploaded file
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)

            with Client(opcua_endpoint) as client:
                client.connect()
                data = []

                with open(file_path, 'r') as csvfile:
                    for row in csvfile:
                        node_id = row.strip()
                        try:
                            node = client.get_node(node_id)
                            node_info = get_node_type(node)
                            data.append(node_info)
                        except Exception as e:
                            data.append({"error": f"Error reading node {node_id}: {str(e)}"})

            # Remove the temporary directory
            os.remove(file_path)
            os.rmdir(temp_dir)

            # Return the data as JSON
            return jsonify({"data": data})

        else:
            return jsonify({"error": "Invalid or missing CSV file"}), 400

    except Exception as e:
        return jsonify({"error": f"Error processing CSV file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
