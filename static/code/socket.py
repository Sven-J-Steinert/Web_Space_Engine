from websocket import WebSocket

socket = WebSocket('http://127.0.0.1:12345')
socket.on('connect', lambda: print('connected'))
socket.on('message', lambda msg: print(msg))
