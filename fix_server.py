import socket
from simplefix import FixParser

class FixServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.parser = FixParser()

    def start(self):
        print("FIX Server listening on port 5000...")
        conn, addr = self.sock.accept()
        print(f"Connected to {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            self.parser.append_buffer(data)
            while True:
                msg = self.parser.get_message()
                if msg is None:
                    break
                print(f"Received FIX message: {msg}")
        conn.close()

if __name__ == "__main__":
    server = FixServer()
    server.start()