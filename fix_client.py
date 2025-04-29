import socket
from simplefix import FixMessage

class FixClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send_order(self):
        msg = FixMessage()
        msg.append_pair(8, "FIX.4.4")
        msg.append_pair(35, "D")  # New Order
        msg.append_pair(55, "AAPL")
        msg.append_pair(54, "1")  # Buy
        msg.append_pair(38, "100")  # Quantity
        msg.append_pair(44, "150.50")  # Price
        self.sock.sendall(msg.encode())
        print(f"Sent FIX message: {msg}")

if __name__ == "__main__":
    client = FixClient()
    client.send_order()