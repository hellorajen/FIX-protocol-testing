# FIX-protocol-testing

# Build with correct tagging
docker build -t fix-protocol-testing .

# Run with volume mounting for development (recommended)
docker run -it -p 5000:5000 -v "$(pwd):/app" fix-protocol-testing
# OR
1. Make the Server Persistent
   Press Ctrl+C to stop the server. To keep it running in the background:

bash
docker run -d -p 5000:5000 --name fix-server -v "$(pwd):/app" fix-protocol-testing

2. Test with Multiple Clients
   Open a new terminal and send more orders:

bash
docker run -it --network host fix-protocol-testing python fix_client.py
