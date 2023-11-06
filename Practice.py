cryptography is not installed, use of crypto disabled
cryptography is not installed, use of crypto disabled
Error connecting to the OPC UA server: [Errno 11001] getaddrinfo failed
Traceback (most recent call last):
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\client.py", line 299, in disconnect
    self.close_secure_channel()
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\client.py", line 343, in close_secure_channel
    return self.uaclient.close_secure_channel()
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\ua_client.py", line 282, in close_secure_channel
    return self._uasocket.close_secure_channel()
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\ua_client.py", line 223, in close_secure_channel
    future = self._send_request(request, message_type=ua.MessageType.SecureClose)
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\ua_client.py", line 72, in _send_request
    self._socket.write(msg)
AttributeError: 'NoneType' object has no attribute 'write'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\40020507\OneDrive - LTTS\Autodiscovery\p2.py", line 39, in <module>
    client.disconnect()
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\client.py", line 301, in disconnect
    self.disconnect_socket()
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\client.py", line 310, in disconnect_socket
    self.uaclient.disconnect_socket()
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\ua_client.py", line 269, in disconnect_socket
    return self._uasocket.disconnect_socket()
  File "C:\Users\40020507\AppData\Roaming\Python\Python39\site-packages\opcua\client\ua_client.py", line 167, in disconnect_socket
    self._socket.socket.shutdown(socket.SHUT_RDWR)
AttributeError: 'NoneType' object has no attribute 'socket'
