import datetime
import socket
from simplefix import FixParser

class FixServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.parser = FixParser()
        
    def log_message(self, msg):
        with open("fix_messages.log", "a") as f:
            f.write(f"{datetime.datetime.now()} | {msg}\n")
            
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
                self.log_message(msg)
                # Here you can add logic to process the FIX message
                # For example, you can send a response back to the client   
                
        conn.close()

if __name__ == "__main__":
    server = FixServer()
    server.start()