from flask import Flask, render_template_string, request
import socket
from simplefix import FixMessage

app = Flask(__name__)

# FIX Configuration
FIX_SERVER_HOST = 'localhost'
FIX_SERVER_PORT = 5000

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>FIX Trading GUI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: inline-block; width: 120px; }
        input, select { padding: 8px; width: 200px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>FIX Order Entry</h1>
    <form method="POST">
        <div class="form-group">
            <label for="symbol">Symbol:</label>
            <input type="text" id="symbol" name="symbol" value="AAPL" required>
        </div>
        <div class="form-group">
            <label for="side">Side:</label>
            <select id="side" name="side">
                <option value="1">Buy</option>
                <option value="2">Sell</option>
            </select>
        </div>
        <div class="form-group">
            <label for="quantity">Quantity:</label>
            <input type="number" id="quantity" name="quantity" value="100" required>
        </div>
        <div class="form-group">
            <label for="price">Price:</label>
            <input type="number" step="0.01" id="price" name="price" value="150.50" required>
        </div>
        <div class="form-group">
            <label for="order_type">Order Type:</label>
            <select id="order_type" name="order_type">
                <option value="1">Market</option>
                <option value="2" selected>Limit</option>
            </select>
        </div>
        <button type="submit">Send Order</button>
    </form>
    
    {% if message %}
    <h2>Last Order Sent:</h2>
    <pre>{{ message }}</pre>
    {% endif %}
</body>
</html>
"""

def send_fix_message(msg):
    """Send FIX message to server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((FIX_SERVER_HOST, FIX_SERVER_PORT))
        sock.sendall(msg.encode())

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        # Create FIX message
        fix_msg = FixMessage()
        fix_msg.append_pair(8, "FIX.4.4")
        fix_msg.append_pair(35, "D")  # New Order Single
        fix_msg.append_pair(55, request.form['symbol'])
        fix_msg.append_pair(54, request.form['side'])
        fix_msg.append_pair(38, request.form['quantity'])
        fix_msg.append_pair(44, request.form['price'])
        fix_msg.append_pair(40, request.form['order_type'])
        
        # Calculate checksum (simplified)
        msg_str = fix_msg.encode()
        checksum = sum(msg_str) % 256
        fix_msg.append_pair(10, f"{checksum:03d}")
        
        send_fix_message(fix_msg)
        message = fix_msg.encode().decode('ascii')

    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)